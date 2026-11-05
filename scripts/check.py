"""Check generated pages and assets without third-party dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re

root=Path(__file__).resolve().parents[1]/'dist'
info=json.loads((root/'build-info.json').read_text())
base=info['basePath']
errors=[]
titles=set()
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.h1=0; self.refs=[]; self.ids=[]; self.description=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='h1':self.h1+=1
        if 'id' in a:self.ids.append(a['id'])
        if tag=='meta' and a.get('name')=='description':self.description=a.get('content')
        for key in ('href','src','data-full'):
            if a.get(key):self.refs.append(a[key])
        if a.get('srcset'):self.refs.extend(x.strip().split()[0] for x in a['srcset'].split(','))
        if tag=='img' and a.get('src'):
            assert a.get('alt'), 'Missing meaningful image alt'
            assert a.get('width') and a.get('height'), 'Missing image dimensions'

files=list(root.rglob('*.html'))
for f in files:
    source=f.read_text(); p=Page(); p.feed(source)
    assert p.h1==1, f'{f}: expected one h1'
    assert p.description, f'{f}: missing description'
    assert len(p.ids)==len(set(p.ids)), f'{f}: duplicate IDs'
    title=re.search(r'<title>(.*?)</title>',source).group(1)
    assert title not in titles, f'Duplicate title: {title}'
    titles.add(title)
    for script in re.findall(r'<script type="application/ld\+json">(.*?)</script>',source):json.loads(script)
    for ref in p.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        path=unquote(u.path)
        if not path:target=f
        elif path.startswith('/'):
            assert not base or path.startswith(base+'/'), f'Incorrect base path: {ref}'
            target=root/path[len(base):].lstrip('/')
        else:target=f.parent/path
        if target.is_dir():target=target/'index.html'
        if not target.exists():errors.append(f'{f.relative_to(root)}: missing {ref}')
        if u.fragment and target.exists() and target.suffix=='.html':
            assert f'id="{u.fragment}"' in target.read_text(), f'Broken anchor: {ref}'
    if info['publishReady']:
        assert 'DESIGN PREVIEW' not in source
        assert 'Placeholder testimonial' not in source
        assert '<link rel="canonical"' in source
    else:assert 'noindex,follow' in source
assert not errors, '\n'.join(errors)
assert len(files)==info['pages'], 'Unexpected generated pages'
for css in (root/'assets').glob('*.css'):
    for asset in re.findall(r'url\([\'"]?([^\)\'\"]+)',css.read_text()):
        assert (css.parent/asset).exists(), f'Missing CSS asset: {asset}'
print(f'PASS: {len(files)} pages; links, assets, image metadata, titles, headings, structured data and publication mode.')
