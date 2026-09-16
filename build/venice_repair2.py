import json, re, os, sys, subprocess, html
from urllib.parse import urljoin
D = sys.argv[1]; OUT = f"{D}/in-time-assets"; os.makedirs(OUT, exist_ok=True)
pool = json.load(open('/tmp/venice_pool.json')); cases, adds = pool['cases'], pool['adds']
data = json.load(open('/tmp/venice_images.json')); results = data['results']
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
ACC = "Accept: image/avif,image/webp,image/apng,image/*,*/*;q=0.8"
def get(url, ref=None, t=20):
    cmd = ["curl","-sL","--max-time",str(t),"-A",UA,"-H",ACC]
    if ref: cmd += ["-e", ref]
    try: r = subprocess.run(cmd+[url], capture_output=True, timeout=t+5); return r.stdout if r.returncode==0 else b""
    except Exception: return b""
def is_img(b):
    return b[:3]==b'\xff\xd8\xff' or b[:8]==b'\x89PNG\r\n\x1a\n' or (b[:4]==b'RIFF' and b[8:12]==b'WEBP') or b[:6] in (b'GIF87a',b'GIF89a')
def width(p):
    r = subprocess.run(["sips","-g","pixelWidth",p], capture_output=True, text=True)
    m = re.search(r'pixelWidth:\s*(\d+)', r.stdout); return int(m.group(1)) if m else 0
def save(b, key):
    if len(b) < 4000 or not is_img(b): return ""
    tmp = f"{OUT}/{key}.tmp"; open(tmp,'wb').write(b)
    out = f"{OUT}/{key}.jpg"
    r = subprocess.run(["sips","-s","format","jpeg","-s","formatOptions","88",tmp,"--out",out], capture_output=True)
    os.remove(tmp)
    if r.returncode!=0 or not os.path.exists(out): return ""
    if width(out) < 300: os.remove(out); return ""
    return os.path.basename(out)
BAD = ['logo','icon','avatar','sprite','emoji','.svg','pixel','blank','1x1','no-result','qrcode','wechat','weixin','dayin','triangle','share','button','banner-bg']
def page_imgs(page, base):
    seen=[]; 
    for pat in [r'property=["\']og:image(?::secure_url)?["\'][^>]+content=["\']([^"\']+)', r'name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)']:
        for m in re.finditer(pat, page, re.I): seen.append(urljoin(base, html.unescape(m.group(1))))
    for s in re.findall(r'<img[^>]+(?:data-src|data-original|data-lazy-src|src)=["\']([^"\']+)', page, re.I):
        u = urljoin(base, html.unescape(s)); sl=u.lower()
        if any(b in sl for b in BAD): continue
        if re.search(r'\.(jpe?g|png|webp)(\?|$)', sl) or 'upload' in sl or '/image' in sl or 'img' in sl: seen.append(u)
    out=[]; [out.append(x) for x in seen if x not in out]; return out
def links_for(k):
    if k.isdigit(): return [u for u,_ in cases[k]['links']]
    if k in adds: return [u for u,_ in adds[k]['links']]
    return [results[k].get('url','')]
extra = {"ART_LIUCHUANG":["https://www.antenna-space.com/en/artists/liu-chuang","https://www.e-flux.com/announcements/188868/liu-chuang/"],
         "ART_LIAMYOUNG":["https://www.liamyoung.org/projects/planet-city"]}
fixed=0
for k, r in results.items():
    if r.get('img') and os.path.exists(f"{OUT}/{r['img']}"): continue
    r['img']=""
    tried_urls = []
    if r.get('img_src') and 'no-result' not in r['img_src']: tried_urls.append((r['img_src'], r.get('url')))
    for pg_url in (extra.get(k) or links_for(k)):
        if not pg_url or pg_url.lower().endswith('.pdf'): continue
        page = get(pg_url, ref=pg_url).decode('utf-8','ignore')
        for c in page_imgs(page, pg_url)[:6]: tried_urls.append((c, pg_url))
    got=False
    for iu, ref in tried_urls:
        b = get(iu, ref=ref); fn = save(b, k)
        if fn: r['img']=fn; r['img_src']=iu; r['note']='ok'; fixed+=1; print(k,'OK',iu[:70],flush=True); got=True; break
    if not got: r['note']='no retrievable image (hotlink-blocked or none)'; print(k,'MISSING',(r.get('url') or '')[:60],flush=True)
json.dump(data, open('/tmp/venice_images.json','w'), ensure_ascii=False, indent=1)
ok = sum(1 for r in results.values() if r['img']); print(f"REPAIR2 DONE: {ok}/{len(results)} images")
