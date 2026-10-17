from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
r=Path('neuro7').resolve()
class Links(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]; self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for k in ['src','href']:
   if k in a:self.links.append(a[k])
pages={}
for name in ['index.html','coverage.html']:
 p=Links();p.feed((r/name).read_text(encoding='utf8'));pages[name]=p
for name,p in pages.items():
 for raw in p.links:
  u=urlsplit(raw)
  if u.scheme or u.netloc:continue
  path=(r/unquote(u.path)).resolve() if u.path else r/name
  assert path.exists(),(name,raw)
  if u.fragment and path.name in pages:assert u.fragment in pages[path.name].ids,(name,raw)
print('All local HTML links, assets, and slide anchors valid.')
