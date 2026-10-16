"""Render every page of the user-specified cranial nerves lecture."""
from pathlib import Path
import json, shutil, subprocess
import pdfplumber
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parent
src=next(Path('C:/Users/Theo/Documents/Med School Resources/Neuro1').glob('NNN 3 *'))
(root/'slides').mkdir(parents=True,exist_ok=True)
temp=root.parent/'tmp-neuro3';temp.mkdir(exist_ok=True)
shutil.copyfile(src,root/'lecture-cn.pdf')
with pdfplumber.open(src) as pdf:
    pages=[{'page':i+1,'text':p.extract_text(layout=False) or '', 'image':f'slides/cn-{i+1:03}.png'} for i,p in enumerate(pdf.pages)]
poppler='C:/Users/Theo/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe'
subprocess.run([poppler,'-png','-r','150',str(src),str(root/'slides'/'cn')],check=True)
for p in pages:
    actual=root/'slides'/f"cn-{str(p['page']).zfill(len(str(len(pages))))}.png";expected=root/p['image']
    if actual!=expected:actual.rename(expected)
    with Image.open(expected) as im:p['width'],p['height']=im.size
decks=[{'id':'cn','title':'Cranial Nerves I','source':src.name,'pages':pages}]
(root/'slides.json').write_text(json.dumps(decks,ensure_ascii=False,indent=2),encoding='utf8')
(temp/'lecture-text.txt').write_text('\n\n'.join(f"=== CN SLIDE {p['page']} ===\n{p['text']}" for p in pages),encoding='utf8')
for k in range(0,len(pages),12):
    canvas=Image.new('RGB',(1600,1050),'white');draw=ImageDraw.Draw(canvas)
    for j,p in enumerate(pages[k:k+12]):
        im=Image.open(root/p['image']);im.thumbnail((390,310));x=(j%4)*400;y=(j//4)*350
        canvas.paste(im,(x,y+25));draw.text((x+5,y+3),f"CN {p['page']}",fill='black')
    canvas.save(temp/f'contact-{k//12}.jpg')
print('Pages:',len(pages))
