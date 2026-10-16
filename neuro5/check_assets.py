"""Check every source image and byte-for-byte preservation of supplied PDFs."""
from pathlib import Path
import json, hashlib
from PIL import Image
root=Path(__file__).resolve().parent
source=Path('C:/Users/Theo/Documents/Med School Resources/Neuro1')
decks=json.loads((root/'slides.json').read_text(encoding='utf8'))
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
n=0
for d in decks:
    assert digest(source/d['source'])==digest(root/f"lecture-{d['id']}.pdf"),d['id']
    for p in d['pages']:
        with Image.open(root/p['image']) as im:
            assert im.size==(p['width'],p['height']);im.verify()
        n+=1
assert n==78
print(f'PASS: {n} PNG files decode with expected dimensions; all three PDF copies match original SHA-256 digests.')
