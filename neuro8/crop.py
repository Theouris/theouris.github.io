from pathlib import Path
from PIL import Image
R=Path(__file__).parent
for n,box in [(4,(.373,.066,.661,.552)),(25,(.568,.245,.905,.873))]:
 im=Image.open(R/f'images/inf-{n:03}.jpg');w,h=im.size
 im.crop(tuple(int(v*(w if i%2==0 else h)) for i,v in enumerate(box))).save(R/f'images/figure-{n:02}.jpg',quality=93)
