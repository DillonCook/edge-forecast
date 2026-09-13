"""Static public-site checks. No network or private build files required."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,re,zipfile
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
class Page(HTMLParser):
    def __init__(self):super().__init__();self.nodes=[]
    def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))
page=Page();html=(DOCS/'index.html').read_text(encoding='utf-8');page.feed(html)
ids=[attrs['id'] for _,attrs in page.nodes if 'id' in attrs];assert len(ids)==len(set(ids))
for tag,a in page.nodes:
    if tag=='img':assert a.get('alt')
    if a.get('target')=='_blank':assert {'noopener','noreferrer'}<=set(a.get('rel','').split())
    for key in ('href','src','poster'):
        value=a.get(key)
        if not value:continue
        url=urlsplit(value)
        if url.scheme:
            assert url.scheme=='https'
            continue
        if not url.path:
            assert not url.fragment or url.fragment in ids
            continue
        p=(DOCS/unquote(url.path)).resolve();assert p.is_relative_to(DOCS.resolve()) and p.is_file(),value
    if tag=='script':assert a.get('src') and not urlsplit(a['src']).scheme
    if tag=='video':assert 'controls' in a and 'autoplay' not in a
release=json.loads((DOCS/'release.json').read_text());apk=ROOT/release['artifact']
assert release['version']=='1.5.21' and release['physicalDeviceVerified'] is False
assert release['downloadUrl']=='https://github.com/DillonCook/edge-forecast/releases/download/v1.5.21/'+release['file']
assert next(a['href'] for t,a in page.nodes if a.get('id')=='apk-download')==release['downloadUrl']
assert 'download-stats' in ids and 'download-count' in ids
assert not any(DOCS.rglob('*.apk')), 'Do not serve a parallel uncounted APK link'
assert apk.stat().st_size==release['bytes'] and hashlib.sha256(apk.read_bytes()).hexdigest()==release['sha256']
assert release['sha256'] in html and release['sha256'] in (DOCS/'downloads/SHA256SUMS.txt').read_text()
assert f"{release['bytes']/1000000:.2f} MB" in html
assert 'Watch Face Format 5' in html and 'Wear OS 7' in html and 'on-watch validation is incomplete' in html
assert 'not watch footage' in html and '10× speed' in html and 'Custom APK' in html
assert {a.get('data-style') for t,a in page.nodes if 'data-style' in a}==set('abcdef')
for s in 'abcdef':
    for mode in ('following','fixed'):assert (DOCS/'assets'/f'{s}-{mode}.webp').is_file()
assert (DOCS/'.nojekyll').exists() and not (DOCS/'CNAME').exists()
for p in DOCS.rglob('*'):
    if not p.is_file():continue
    assert p.suffix in {'.html','.css','.js','.webp','.jpg','.svg','.mp4','.apk','.json','.txt','.xml'} or p.name=='.nojekyll',p
    if p.suffix in {'.html','.css','.js','.json','.txt','.xml','.svg'}:
        text=p.read_text(encoding='utf-8')
        assert not re.search(r'(?:[A-Z]:[\\/]Users[\\/]|gh[pousr]_[A-Za-z0-9]{20}|BEGIN (?:RSA |OPENSSH )?PRIVATE KEY|@gmail\.com)',text),p
with zipfile.ZipFile(apk) as z:
    assert not any(n.endswith(('.jks','.keystore','.env')) for n in z.namelist())
print('PASS: links, progressive HTML, local assets, all six styles/two modes, compatibility/testing disclosures, exact APK fingerprint, publication scope and no custom domain.')
