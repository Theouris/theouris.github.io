import pypdfium2 as pdf, json
from pathlib import Path
from PIL import Image, ImageDraw
r=Path('neuro6'); (r/'images').mkdir(exist_ok=True); (r/'review').mkdir(exist_ok=True)
ds=json.loads((r/'slides.json').read_text(encoding='utf8'))
for d in ds:
 doc=pdf.PdfDocument(str(r/f"lecture-{d['id']}.pdf"))
 for i,p in enumerate(doc):
  im=p.render(scale=1.8).to_pil().convert('RGB'); path=f"images/{d['id']}-{i+1:02}.jpg"; im.save(r/path,quality=88)
  d['pages'][i]['image']=path
  d['pages'][i]['text']=p.get_textpage().get_text_range()
 for start in range(0,len(doc),12):
  sheet=Image.new('RGB',(1600,4*310),'#dddddd'); draw=ImageDraw.Draw(sheet)
  for j in range(start,min(start+12,len(doc))):
   im=Image.open(r/d['pages'][j]['image']); im.thumbnail((520,278)); x=(j-start)%3*533; y=(j-start)//3*310; sheet.paste(im,(x,y+24)); draw.text((x+8,y+4),f"{d['id']}-{j+1}",fill='black')
  sheet.save(r/f"review/{d['id']}-{start+1}.jpg")
(r/'slides.json').write_text(json.dumps(ds,ensure_ascii=False,indent=2),encoding='utf8')
