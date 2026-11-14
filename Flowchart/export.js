// Dependency-free downloads. PNG includes actual pHYs (DPI) metadata.
// PDF uses lossless RGB image data; SVG remains fully vector and editable.
export function downloadBlob(blob, name) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url; link.download = name;
  document.body.append(link); link.click(); link.remove();
  setTimeout(()=>URL.revokeObjectURL(url),30000);
}

export async function rasterize(svg, width, height) {
  if (width*height > 32_000_000 || width>12000 || height>12000) throw new Error('Use dimensions up to 12,000 px and 32 million pixels in total.');
  const url = URL.createObjectURL(new Blob([svg],{type:'image/svg+xml;charset=utf-8'}));
  try {
    const image = new Image();
    image.src = url;
    await image.decode();
    const canvas = document.createElement('canvas');
    canvas.width = width; canvas.height = height;
    const context = canvas.getContext('2d');
    if (!context) throw new Error('Your browser could not allocate the image. Try a smaller export.');
    context.fillStyle = '#ffffff'; context.fillRect(0,0,width,height);
    context.drawImage(image,0,0,width,height);
    return canvas;
  } finally { URL.revokeObjectURL(url); }
}

const crcTable = Array.from({length:256},(_,n)=>{
  let c=n; for(let k=0;k<8;k++) c=(c&1)?0xedb88320^(c>>>1):c>>>1;
  return c>>>0;
});
function crc32(bytes) { let c=0xffffffff; for(const b of bytes)c=crcTable[(c^b)&255]^(c>>>8);return(c^0xffffffff)>>>0; }
function chunk(type,data) {
  const bytes=new Uint8Array(12+data.length); const view=new DataView(bytes.buffer);
  view.setUint32(0,data.length); bytes.set(new TextEncoder().encode(type),4);bytes.set(data,8);
  view.setUint32(bytes.length-4,crc32(bytes.subarray(4,bytes.length-4)));
  return bytes;
}

export async function canvasToPNG(canvas,dpi) {
  const blob=await new Promise((resolve,reject)=>canvas.toBlob(b=>b?resolve(b):reject(new Error('PNG encoding failed. Try a smaller image.')),'image/png'));
  const original=new Uint8Array(await blob.arrayBuffer());
  const pixelsPerMeter=Math.round(dpi/0.0254);
  const density=new Uint8Array(9);const densityView=new DataView(density.buffer);
  densityView.setUint32(0,pixelsPerMeter);densityView.setUint32(4,pixelsPerMeter);density[8]=1;
  const parts=[original.subarray(0,8)];
  // Replace any existing density chunk, inserting the requested one after IHDR.
  for(let offset=8;offset<original.length;) {
    const length=new DataView(original.buffer,original.byteOffset+offset,4).getUint32(0);
    const end=offset+12+length;
    const type=new TextDecoder().decode(original.subarray(offset+4,offset+8));
    if(type!=='pHYs')parts.push(original.subarray(offset,end));
    if(type==='IHDR')parts.push(chunk('pHYs',density));
    offset=end;
  }
  return new Blob(parts,{type:'image/png'});
}

export async function canvasToPDF(canvas,dpi) {
  const width=canvas.width,height=canvas.height;
  const rgba=canvas.getContext('2d').getImageData(0,0,width,height).data;
  const rgb=new Uint8Array(width*height*3);
  for(let from=0,to=0;from<rgba.length;from+=4) {rgb[to++]=rgba[from];rgb[to++]=rgba[from+1];rgb[to++]=rgba[from+2];}
  let data=rgb,filter='';
  if(typeof CompressionStream!=='undefined') {
    const stream=new Blob([rgb]).stream().pipeThrough(new CompressionStream('deflate'));
    data=new Uint8Array(await new Response(stream).arrayBuffer());filter='/Filter /FlateDecode ';
  }
  const pageWidth=width*72/dpi,pageHeight=height*72/dpi;
  if(pageWidth>14400||pageHeight>14400)throw new Error('This PDF exceeds the maximum page size. Increase the DPI or reduce the pixel dimensions.');
  const encoder=new TextEncoder(), parts=[], offsets=[0];let length=0;
  const append=part=>{const bytes=typeof part==='string'?encoder.encode(part):part;parts.push(bytes);length+=bytes.length;};
  const object=(id,body)=>{offsets[id]=length;append(`${id} 0 obj\n${body}\nendobj\n`);};
  append('%PDF-1.4\n%\u00e2\u00e3\u00cf\u00d3\n');
  object(1,'<< /Type /Catalog /Pages 2 0 R >>');
  object(2,'<< /Type /Pages /Kids [3 0 R] /Count 1 >>');
  object(3,`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${pageWidth.toFixed(4)} ${pageHeight.toFixed(4)}] /Resources << /XObject << /Im0 4 0 R >> >> /Contents 5 0 R >>`);
  offsets[4]=length;
  append(`4 0 obj\n<< /Type /XObject /Subtype /Image /Width ${width} /Height ${height} /ColorSpace /DeviceRGB /BitsPerComponent 8 ${filter}/Length ${data.length} >>\nstream\n`);
  append(data);append('\nendstream\nendobj\n');
  const content=`q\n${pageWidth.toFixed(4)} 0 0 ${pageHeight.toFixed(4)} 0 0 cm\n/Im0 Do\nQ\n`;
  object(5,`<< /Length ${encoder.encode(content).length} >>\nstream\n${content}endstream`);
  object(6,'<< /Producer (PRISMA Flowchart) /Title (Review flowchart) >>');
  const xref=length;
  append('xref\n0 7\n0000000000 65535 f \n');
  for(let id=1;id<=6;id++)append(`${String(offsets[id]).padStart(10,'0')} 00000 n \n`);
  append(`trailer\n<< /Size 7 /Root 1 0 R /Info 6 0 R >>\nstartxref\n${xref}\n%%EOF\n`);
  return new Blob(parts,{type:'application/pdf'});
}
