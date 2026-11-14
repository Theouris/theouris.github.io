import test from 'node:test';
import assert from 'node:assert/strict';
import { inflateSync } from 'node:zlib';
import { Blob as NodeBlob } from 'node:buffer';
import { TextEncoder as NodeTextEncoder, TextDecoder as NodeTextDecoder } from 'node:util';
import { createProject, createReview, calculate, validate, parseProject, populateText, addGroupRow, removeGroupRow, COUNT_PATTERN, MODES } from './model.js';
import { buildScene, sceneToSVG, COLORS } from './diagram.js';
import { canvasToPNG, canvasToPDF, rasterize } from './export.js';

export const results = [];
// Some embedded Node test hosts omit these standard browser-compatible globals.
globalThis.Blob ??= NodeBlob;
globalThis.TextEncoder ??= NodeTextEncoder;
globalThis.TextDecoder ??= NodeTextDecoder;
const failures = [];
async function check(name, fn) {
  await test(name, async () => { try { await fn(); results.push(name); } catch(error) { failures.push(`${name}: ${error.message}`); throw error; } });
}

await check('An untouched reference keeps all counts blank', () => {
  const r = createReview();
  assert.equal(calculate(r).values.screened, null);
  assert.equal(calculate(r).values.includedReports, null);
  assert.deepEqual(validate(r), []);
  assert.equal(populateText(r.texts.screened, ['screened'], calculate(r).values), 'Records screened\n(n = )');
});

await check('Independent database and other-methods routes reconcile at inclusion', () => {
  const r = createReview();
  r.values = {databases:1000,registers:100,duplicates:100,automation:10,removedOther:5,excluded:900,notRetrieved:5,dbReason1:30,dbReason2:10,dbReason3:5,websites:30,organisations:10,citations:5,otherNotRetrieved:5,otherReason1:10,studies:60};
  const c = calculate(r);
  assert.equal(c.values.screened, 985);
  assert.equal(c.values.sought, 85);
  assert.equal(c.values.assessed, 80);
  assert.equal(c.values.otherSought, 45);
  assert.equal(c.values.otherAssessed, 40);
  assert.equal(c.values.includedReports, 65);
  assert.deepEqual(validate(r), []);
});

await check('Overrides survive upstream changes and feed later calculations', () => {
  const r = createReview();
  r.values = {databases:100,duplicates:10,screened:70,excluded:20};
  assert.equal(calculate(r).values.sought, 50);
  r.values.databases = 200;
  assert.equal(calculate(r).values.screened, 70);
  assert.equal(calculate(r).values.sought, 50);
  delete r.values.screened;
  assert.equal(calculate(r).values.sought, 170);
});

await check('Hiding the other-methods route excludes it without deleting its draft', () => {
  const r = createReview(); r.values = {databases:100,websites:20};
  assert.equal(calculate(r).values.includedReports, 120);
  r.showOther = false;
  assert.equal(calculate(r).values.includedReports, 100);
  assert.equal(r.values.websites, 20);
});

await check('Narrative sources pool before deduplication; scoping retains both routes', () => {
  const r = createReview('narrative');
  r.values = {databases:100,narrativeOther:20,duplicates:10,excluded:90,notRetrieved:2,dbReason1:5};
  assert.equal(calculate(r).values.includedReports, 13);
  assert.equal(r.showOther, false);
  const scoping = createReview('scoping'); scoping.values = {databases:10,citations:2};
  assert.equal(calculate(scoping).values.includedReports, 12);
  assert.match(scoping.texts.included, /Sources of evidence/);
});

await check('Unique studies are entered independently of the calculated report count', () => {
  const r = createReview(); r.values.databases = 20;
  assert.equal(calculate(r).values.studies, null);
  assert.ok(validate(r).some(n => n.text.includes('unique included studies')));
  r.values.studies = 5;
  assert.equal(calculate(r).values.includedReports, 20);
  assert.equal(calculate(r).values.studies, 5);
});

await check('Impossible deductions are errors and inconsistent overrides are notices', () => {
  const r = createReview(); r.values = {databases:10,duplicates:20};
  assert.ok(validate(r).some(n => n.level === 'error'));
  r.values.screened = 5;
  assert.ok(validate(r).some(n => n.text.includes('manually set')));
});

await check('Reason rows keep counts, text markers, and downstream totals aligned', () => {
  const r = createReview(); addGroupRow(r,'dbReasons');
  const key = r.groups.dbReasons.at(-1); r.values = {databases:50,[key]:5};
  assert.equal(calculate(r).values.includedReports,45);
  assert.equal((r.texts.dbReasons.match(COUNT_PATTERN)||[]).length,4);
  removeGroupRow(r,'dbReasons',3);
  assert.equal(calculate(r).values.includedReports,50);
  assert.equal((r.texts.dbReasons.match(COUNT_PATTERN)||[]).length,3);
  r.texts.dbReasons = 'Custom wording with no count markers';
  assert.ok(validate(r).some(n => n.text.includes('count markers')));
});

await check('Projects preserve separate modes, Unicode text, counts, and overrides', () => {
  const p = createProject(); p.activeMode = 'scoping';
  p.reviews.scoping.values = {databases:200,screened:123};
  p.reviews.scoping.texts.screened = 'Études <screen> & 日本語\n(n = )';
  assert.deepEqual(parseProject(JSON.stringify(p)),p);
  assert.throws(() => parseProject('{}'));
  p.reviews.scoping.values.databases = -10;
  assert.equal(parseProject(JSON.stringify(p)).reviews.scoping.values.databases,undefined);
});

await check('Imported source IDs cannot collide with deduction or calculated fields', () => {
  const p = createProject(); p.reviews.systematic.groups.dbSources = ['duplicates'];
  const clean = parseProject(JSON.stringify(p));
  assert.deepEqual(clean.reviews.systematic.groups.dbSources,['databases','registers']);
});

await check('SVG preserves the reference palette and safely escapes editable text', () => {
  const r = createReview(); r.texts.screened = '<script>alert(1)</script> & text\n(n = )';
  const svg = sceneToSVG(buildScene(r),{width:2400,height:1800,dpi:300});
  assert.ok(svg.includes('&lt;script&gt;')); assert.ok(!svg.includes('<script>'));
  for (const color of Object.values(COLORS)) assert.ok(svg.includes(color));
  assert.match(svg,/pixel-width=2400; pixel-height=1800/);
  assert.match(svg,/dpi=300/); assert.ok(!svg.includes('foreignObject'));
});

await check('All modes expand boxes and move inclusion below long exclusion text', () => {
  for(const mode of MODES) {
    const r = createReview(mode), before = buildScene(r);
    r.texts.dbReasons = 'Long exclusion reason with additional explanation '.repeat(15)+'\n(n = )';
    const after = buildScene(r);
    assert.ok(after.height>before.height);
    assert.ok(after.nodes.included.y>after.nodes.dbReasons.y+after.nodes.dbReasons.h);
  }
});

await check('PNG export writes one CRC-valid pHYs chunk at the requested DPI', async () => {
  const original = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aT1sAAAAASUVORK5CYII=','base64');
  const canvas = {toBlob:callback=>callback(new Blob([original],{type:'image/png'}))};
  const png = Buffer.from(await (await canvasToPNG(canvas,300)).arrayBuffer());
  let found = 0;
  for(let offset=8;offset<png.length;) {
    const length=png.readUInt32BE(offset), type=png.toString('ascii',offset+4,offset+8);
    if(type==='pHYs') {
      found++; assert.equal(png.readUInt32BE(offset+8),11811);assert.equal(png.readUInt32BE(offset+12),11811);assert.equal(png[offset+16],1);
      let crc=0xffffffff;
      for(const b of png.subarray(offset+4,offset+8+length)) {crc^=b;for(let i=0;i<8;i++)crc=(crc&1)?(crc>>>1)^0xedb88320:crc>>>1;}
      assert.equal((crc^0xffffffff)>>>0,png.readUInt32BE(offset+8+length));
    }
    offset+=length+12;
  }
  assert.equal(found,1);
});

await check('PDF export preserves image colors, DPI page size, and cross-reference offsets', async () => {
  const rgba = new Uint8ClampedArray([255,192,0,255,156,194,229,255,0,0,0,255,255,255,255,255]);
  const canvas = {width:2,height:2,getContext:()=>({getImageData:()=>({data:rgba})})};
  const pdf = Buffer.from(await (await canvasToPDF(canvas,300)).arrayBuffer());
  const text = pdf.toString('latin1');
  assert.match(text,/\/MediaBox \[0 0 0\.4800 0\.4800\]/);
  const imageObject=text.indexOf('4 0 obj'),start=text.indexOf('stream\n',imageObject)+7;
  const length=Number(text.slice(imageObject,start).match(/\/Length (\d+)/)[1]);
  const image=pdf.subarray(start,start+length);
  const rgb=text.slice(imageObject,start).includes('/FlateDecode')?inflateSync(image):image;
  assert.deepEqual([...rgb],[255,192,0,156,194,229,0,0,0,255,255,255]);
  const xref=Number(text.match(/startxref\n(\d+)/)[1]);
  assert.equal(text.slice(xref,xref+4),'xref');
  const entries=text.slice(xref).split('\n').slice(3,9);
  entries.forEach((entry,index)=>{const offset=Number(entry.slice(0,10));assert.equal(text.slice(offset,offset+7),`${index+1} 0 obj`);});
});

await check('Oversized raster export fails before allocating a canvas', async () => {
  await assert.rejects(()=>rasterize('<svg/>',12000,12000),/32 million/);
});

assert.equal(failures.length,0,failures.join('\n'));
assert.equal(results.length,15,'Every check must complete successfully.');
