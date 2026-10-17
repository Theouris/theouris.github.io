from pathlib import Path
import pypdfium2 as pdf,json,shutil
from PIL import Image,ImageDraw
r=Path(__file__).parent; (r/'images').mkdir(exist_ok=True); (r/'review').mkdir(exist_ok=True)
base=Path('C:/Users/Theo/Documents/Med School Resources/Neuro1')
files=[('av','2026 Auditory and Vestibular UNLV Med.pdf'),('oph','Ophthalmics student 2025.pdf'),('va','Visual and Auditory  Systems_Lecture Slides 10.14.2026b.pdf')]
ds=[]
for code,name in files:
 local=r/f'lecture-{code}.pdf'
 if not local.exists():shutil.copyfile(base/name,local)
 doc=pdf.PdfDocument(str(local)); d={'id':code,'source':name,'pages':[]}
 for i,p in enumerate(doc):
  path=f'images/{code}-{i+1:03}.jpg'; im=p.render(scale=1.6).to_pil().convert('RGB'); im.save(r/path,quality=86)
  d['pages'].append({'page':i+1,'text':p.get_textpage().get_text_range(),'image':path})
 for start in range(0,len(doc),12):
  sheet=Image.new('RGB',(1800,1320),'#ddd'); draw=ImageDraw.Draw(sheet)
  for j in range(start,min(start+12,len(doc))):
   im=Image.open(r/d['pages'][j]['image']);im.thumbnail((590,300));x=(j-start)%3*600;y=(j-start)//3*330
   sheet.paste(im,(x,y+25));draw.text((x+5,y+5),f'{code}-{j+1}',fill='black')
  sheet.save(r/f'review/{code}-{start+1}.jpg')
 ds.append(d)
(r/'slides.json').write_text(json.dumps(ds,ensure_ascii=False,indent=2),encoding='utf8')
(r/'slides.txt').write_text('\n'.join('=== '+d['id']+'-'+str(p['page'])+' ===\n'+p['text'] for d in ds for p in d['pages']),encoding='utf8')
print([(d['id'],len(d['pages'])) for d in ds])
