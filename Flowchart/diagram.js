import { boxesFor, calculate, populateText } from './model.js';

// Colors are taken directly from the supplied Word document's theme and shapes.
export const COLORS = { text: '#000000', box: '#ffffff', header: '#ffc000', headerBorder: '#7f5f00', phase: '#9cc2e5' };
export const escapeXML = value => String(value).replace(/[<>&"']/g, char => ({ '<':'&lt;', '>':'&gt;', '&':'&amp;', '"':'&quot;', "'":'&apos;' }[char]));

export function wrapText(text, maxWidth, size, measure = (s, f) => s.length * f * .52) {
  const lines = [];
  for (const paragraph of text.split('\n')) {
    if (!paragraph) { lines.push(''); continue; }
    let line = '';
    const tokens = paragraph.match(/\S+\s*|\s+/g) || [''];
    for (let token of tokens) {
      if (line && measure((line + token).trimEnd(), size) > maxWidth) {
        lines.push(line.trimEnd()); line = '';
      }
      // Very long unbroken words (including URLs) must not overflow the diagram.
      while (measure(token.trimEnd(), size) > maxWidth) {
        let take = 1;
        while (take < token.length && measure(token.slice(0, take + 1), size) <= maxWidth) take++;
        if (line) { lines.push(line.trimEnd()); line = ''; }
        lines.push(token.slice(0, take)); token = token.slice(take);
      }
      line += token;
    }
    lines.push(line.trimEnd());
  }
  return lines;
}

export function buildScene(review, measure) {
  const result = calculate(review);
  const boxes = boxesFor(review);
  const size = review.fontSize;
  const lineHeight = size * 1.25;
  const padding = 17;
  const colWidth = 282;
  const gap = 66;
  const xs = [94, 94 + colWidth + gap, 94 + 2 * (colWidth + gap), 94 + 3 * (colWidth + gap)];
  const twoRoutes = review.showOther && review.mode !== 'narrative';
  const width = twoRoutes ? xs[3] + colWidth + 38 : xs[1] + colWidth + 38;
  const elements = [];
  const nodes = {};
  const linesFor = (id, boxWidth = colWidth) => wrapText(populateText(review.texts[id], boxes[id]?.keys || [], result.values), boxWidth - 2 * padding, size, measure);
  const heightFor = id => Math.max(74, linesFor(id).length * lineHeight + padding * 2);
  function label(lines, x, y, fontSize = size, align = 'start', bold = false, rotation = null) {
    elements.push({ type:'text', lines, x, y, fontSize, lineHeight:fontSize * 1.25, align, bold, rotation, fill:COLORS.text });
  }
  function rect(x, y, w, h, fill = COLORS.box, stroke = COLORS.text, radius = 0) {
    elements.push({ type:'rect', x, y, w, h, fill, stroke, radius, strokeWidth:1.2 });
  }
  function node(id, column, y, fixedHeight) {
    const x = xs[column];
    const lines = linesFor(id);
    const h = fixedHeight ?? heightFor(id);
    nodes[id] = { x, y, w:colWidth, h, cx:x + colWidth/2, cy:y + h/2 };
    rect(x,y,colWidth,h);
    label(lines,x + padding,y + (h - lines.length * lineHeight)/2 + size);
    return nodes[id];
  }
  function arrow(points) {
    elements.push({type:'path', points, stroke:COLORS.text, strokeWidth:1.5});
    const end = points.at(-1), previous = points.at(-2);
    const angle = Math.atan2(end[1]-previous[1],end[0]-previous[0]);
    const a = 8;
    elements.push({type:'polygon', points:[end,[end[0]-a*Math.cos(angle-.4),end[1]-a*Math.sin(angle-.4)],[end[0]-a*Math.cos(angle+.4),end[1]-a*Math.sin(angle+.4)]],fill:COLORS.text});
  }
  function down(from, to) { arrow([[nodes[from].cx,nodes[from].y+nodes[from].h],[nodes[to].cx,nodes[to].y-2]]); }
  function across(from, to) { arrow([[nodes[from].x+nodes[from].w,nodes[from].cy],[nodes[to].x-2,nodes[from].cy]]); }
  function phase(id, y, h) {
    rect(28,y,30,h,COLORS.phase,COLORS.text,8);
    const cx = 43, cy = y+h/2;
    const text = review.texts[id].replace(/\n/g, ' ');
    const measured = (measure || ((s,f)=>s.length*f*.52))(text,size);
    const phaseSize = Math.min(size, size*(h-22)/Math.max(1,measured));
    label([text],cx,cy+phaseSize*.32,phaseSize,'middle',true,{x:cx,y:cy,angle:-90});
  }
  const headerWidth = 2*colWidth+gap;
  const mainHeader = wrapText(review.texts.dbHeader,headerWidth-24,size,measure);
  const otherHeader = twoRoutes ? wrapText(review.texts.otherHeader,headerWidth-24,size,measure) : [];
  const headerHeight = Math.max(42,Math.max(mainHeader.length,otherHeader.length)*lineHeight+16);
  rect(xs[0],30,headerWidth,headerHeight,COLORS.header,COLORS.headerBorder,9);
  label(mainHeader,xs[0]+headerWidth/2,30+(headerHeight-mainHeader.length*lineHeight)/2+size,size,'middle',true);
  if (twoRoutes) {
    rect(xs[2],30,headerWidth,headerHeight,COLORS.header,COLORS.headerBorder,9);
    label(otherHeader,xs[2]+headerWidth/2,30+(headerHeight-otherHeader.length*lineHeight)/2+size,size,'middle',true);
  }
  const firstY = 30+headerHeight+30;
  const firstH = Math.max(heightFor('dbSources'),heightFor('removed'),twoRoutes?heightFor('otherSources'):0);
  node('dbSources',0,firstY,firstH); node('removed',1,firstY,firstH);
  if (twoRoutes) node('otherSources',2,firstY,firstH);
  across('dbSources','removed');
  phase('phaseIdentification',firstY,firstH);

  const screeningY = firstY+firstH+45;
  const screeningH = Math.max(heightFor('screened'),heightFor('excluded'));
  node('screened',0,screeningY,screeningH); node('excluded',1,screeningY,screeningH);
  down('dbSources','screened'); across('screened','excluded');
  const retrievalY = screeningY+screeningH+45;
  const retrievalIds = ['sought','notRetrieved',...(twoRoutes?['otherSought','otherNotRetrieved']:[])];
  const retrievalH = Math.max(...retrievalIds.map(heightFor));
  node('sought',0,retrievalY,retrievalH); node('notRetrieved',1,retrievalY,retrievalH);
  down('screened','sought'); across('sought','notRetrieved');
  if (twoRoutes) {
    node('otherSought',2,retrievalY,retrievalH); node('otherNotRetrieved',3,retrievalY,retrievalH);
    down('otherSources','otherSought'); across('otherSought','otherNotRetrieved');
  }
  const eligibilityY = retrievalY+retrievalH+45;
  const assessedH = Math.max(heightFor('assessed'),twoRoutes?heightFor('otherAssessed'):0);
  node('assessed',0,eligibilityY,assessedH); node('dbReasons',1,eligibilityY);
  down('sought','assessed'); across('assessed','dbReasons');
  if (twoRoutes) {
    node('otherAssessed',2,eligibilityY,assessedH); node('otherReasons',3,eligibilityY);
    down('otherSought','otherAssessed'); across('otherAssessed','otherReasons');
  }
  const eligibilityBottom = Math.max(...['assessed','dbReasons',...(twoRoutes?['otherAssessed','otherReasons']:[])].map(id=>nodes[id].y+nodes[id].h));
  phase('phaseScreening',screeningY,eligibilityBottom-screeningY);
  const includedY = eligibilityBottom+70;
  node('included',0,includedY);
  down('assessed','included');
  if (twoRoutes) arrow([[nodes.otherAssessed.cx,nodes.otherAssessed.y+nodes.otherAssessed.h],[nodes.otherAssessed.cx,nodes.included.cy],[nodes.included.x+nodes.included.w+2,nodes.included.cy]]);
  phase('phaseIncluded',includedY,nodes.included.h);

  const footSize = Math.max(10.5,size*.66);
  const footLines = wrapText(review.texts.footnotes,width-76,footSize,measure);
  const footY = includedY+nodes.included.h+40;
  label(footLines,38,footY+footSize,footSize);
  const height = Math.ceil(footY+footLines.length*footSize*1.25+30);
  return { width, height, elements, nodes, mode:review.mode };
}

export function sceneToSVG(scene, { width = scene.width, height = scene.height, dpi = 96, accessible = false } = {}) {
  const parts = [`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${width}" height="${height}" viewBox="0 0 ${scene.width} ${scene.height}"${accessible ? ' role="img" aria-labelledby="diagram-title"' : ''}>`,
    `<title id="diagram-title">${escapeXML(scene.mode[0].toUpperCase()+scene.mode.slice(1))} review flowchart</title>`,
    `<metadata>PRISMA Flowchart; review=${scene.mode}; dpi=${dpi}; pixel-width=${width}; pixel-height=${height}</metadata>`,
    `<rect width="${scene.width}" height="${scene.height}" fill="#ffffff"/>`];
  for (const e of scene.elements) {
    if (e.type==='rect') parts.push(`<rect x="${e.x}" y="${e.y}" width="${e.w}" height="${e.h}" rx="${e.radius}" fill="${e.fill}" stroke="${e.stroke}" stroke-width="${e.strokeWidth}"/>`);
    if (e.type==='path') parts.push(`<path d="${e.points.map((p,i)=>(i?'L':'M')+p.join(' ')).join(' ')}" fill="none" stroke="${e.stroke}" stroke-width="${e.strokeWidth}"/>`);
    if (e.type==='polygon') parts.push(`<polygon points="${e.points.map(p=>p.join(',')).join(' ')}" fill="${e.fill}"/>`);
    if (e.type==='text') {
      const transform = e.rotation ? ` transform="rotate(${e.rotation.angle} ${e.rotation.x} ${e.rotation.y})"` : '';
      parts.push(`<text x="${e.x}" y="${e.y}" font-family="Arial, Helvetica, sans-serif" font-size="${e.fontSize}" font-weight="${e.bold?'700':'400'}" text-anchor="${e.align}" fill="${e.fill}" xml:space="preserve"${transform}>${e.lines.map((line,index)=>`<tspan x="${e.x}" y="${e.y+index*e.lineHeight}">${escapeXML(line)}</tspan>`).join('')}</text>`);
    }
  }
  parts.push('</svg>');
  return parts.join('');
}
