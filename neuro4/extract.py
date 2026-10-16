"""Extract and render the user-specified lecture for question coverage checks."""
from pathlib import Path
import json, shutil, subprocess
import pdfplumber
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parent
src=next(Path('C:/Users/Theo/Documents/Med School Resources/Neuro1').glob('NNN 4.1 *'))
(root/'slides').mkdir(parents=True,exist_ok=True)
temp=root.parent/'tmp-neuro4';temp.mkdir(exist_ok=True)
shutil.copyfile(src,root/'lecture.pdf')
with pdfplumber.open(src) as pdf:
    pages=[{'page':i+1,'text':p.extract_text(layout=False) or '', 'image':f'slides/{i+1:03}.png'} for i,p in enumerate(pdf.pages)]
poppler='C:/Users/Theo/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe'
subprocess.run([poppler,'-png','-r','150',str(src),str(root/'slides'/'render')],check=True)
for p in pages:
    actual=root/'slides'/f"render-{str(p['page']).zfill(len(str(len(pages))))}.png";actual.rename(root/p['image'])
    with Image.open(root/p['image']) as im:p['width'],p['height']=im.size
(root/'slides.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf8')
(temp/'lecture-text.txt').write_text('\n\n'.join(f"=== SLIDE {p['page']} ===\n{p['text']}" for p in pages),encoding='utf8')
for k in range(0,len(pages),12):
    canvas=Image.new('RGB',(1600,1050),'white');draw=ImageDraw.Draw(canvas)
    for j,p in enumerate(pages[k:k+12]):
        im=Image.open(root/p['image']);im.thumbnail((390,310));x=(j%4)*400;y=(j//4)*350
        canvas.paste(im,(x,y+25));draw.text((x+5,y+3),f"Slide {p['page']}",fill='black')
    canvas.save(temp/f'contact-{k//12}.jpg')
print('Pages:',len(pages))
