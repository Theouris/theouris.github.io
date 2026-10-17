from pathlib import Path
from PIL import Image
R=Path(__file__).parent
# Fractions selected from inspected source pages; exclude answer-bearing slide headings.
crops={
 'figure-effusion':('av',3,(.37,.46,.65,.95)),
 'figure-schwannoma':('av',9,(.49,.01,.99,.99)),
 'figure-asymmetric':('av',8,(.49,.10,.95,.91)),
 'figure-wax':('av',39,(.67,.63,.99,.99)),
 'figure-tube':('av',4,(.56,.29,.88,.87)),
 'figure-balloon':('av',5,(.10,.32,.59,.84)),
 'figure-normal':('av',29,(.36,.10,.98,.94)),
 'figure-sensorineural':('av',30,(.43,.145,.88,.93)),
 'figure-conductive':('av',31,(.41,.22,.78,.87)),
 'figure-mixed':('av',32,(.43,.145,.88,.93)),
 'figure-vascular-mass':('av',57,(.24,.26,.79,.94)),
 'figure-dix':('av',88,(.47,.14,.95,.95)),
 'figure-epley':('av',89,(.35,.26,.65,.91)),
 'figure-hydrops':('av',93,(.24,.31,.73,.84)),
 'figure-intratympanic':('av',103,(.23,.24,.79,.92)),
 'figure-gaze':('av',110,(.28,.28,.73,.75)),
 'figure-bitot':('va',14,(.634,.13,.86,.463)),
}
for name,(deck,n,box) in crops.items():
 im=Image.open(R/f'images/{deck}-{n:03}.jpg');w,h=im.size
 im.crop(tuple(int(v*(w if i%2==0 else h)) for i,v in enumerate(box))).save(R/f'images/{name}.jpg',quality=93)
