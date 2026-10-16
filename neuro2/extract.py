"""Extract the two user-specified source PDFs into complete slide images/text."""
from pathlib import Path
import pdfplumber, json, subprocess, shutil
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parent
source=Path('C:/Users/Theo/Documents/Med School Resources/Neuro1')
(root/'slides').mkdir(parents=True,exist_ok=True)
temp=root.parent/'tmp-neuro2';temp.mkdir(exist_ok=True)
poppler='C:/Users/Theo/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe'
decks=[]
for code,pattern,title in [('sig','Alexander_Neural Signaling*','Neural Signaling'),('cord','NNN 2 *','Spinal Cord')]:
    src=next(source.glob(pattern));shutil.copyfile(src,root/f'lecture-{code}.pdf')
    with pdfplumber.open(src) as pdf:
        pages=[{'page':i+1,'text':p.extract_text(layout=False) or '', 'image':f'slides/{code}-{i+1:03}.png'} for i,p in enumerate(pdf.pages)]
    subprocess.run([poppler,'-png','-r','140',str(src),str(root/'slides'/code)],check=True)
    for i,p in enumerate(pages):
        actual=root/'slides'/f'{code}-{str(i+1).zfill(len(str(len(pages))))}.png'
        expected=root/p['image']
        if actual!=expected:actual.rename(expected)
        with Image.open(expected) as im:p['width'],p['height']=im.size
    decks.append({'id':code,'title':title,'source':src.name,'pages':pages})
(root/'slides.json').write_text(json.dumps(decks,ensure_ascii=False,indent=2),encoding='utf-8')
(temp/'lecture-text.txt').write_text('\n\n'.join(f"=== {d['id']} SLIDE {p['page']} ===\n{p['text']}" for d in decks for p in d['pages']),encoding='utf-8')
files=[root/p['image'] for d in decks for p in d['pages']]
for k in range(0,len(files),12):
    canvas=Image.new('RGB',(1600,1050),'white');draw=ImageDraw.Draw(canvas)
    for j,f in enumerate(files[k:k+12]):
        im=Image.open(f);im.thumbnail((390,310));x=(j%4)*400;y=(j//4)*350
        canvas.paste(im,(x,y+25));draw.text((x+5,y+3),f.stem,fill='black')
    canvas.save(temp/f'contact-{k//12}.jpg')
print([(d['id'],len(d['pages'])) for d in decks])
