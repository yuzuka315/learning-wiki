# 檢查 B：成品檢查（產生簡報之後）
import os, re, json
from playwright.sync_api import sync_playwright
root = os.path.abspath('..')
url = 'file://' + root + '/slides/index.html'
probs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, vp in [('desk', (1280, 720)), ('phone', (390, 844))]:
        pg = b.new_page(viewport={'width': vp[0], 'height': vp[1]}, device_scale_factor=1)
        errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.goto(url)
        n = pg.evaluate('document.querySelectorAll(".slide").length')
        for i in range(n):
            pg.goto(url + f'#{i+1}'); pg.reload()
            r = pg.evaluate('''()=>{const s=document.querySelector(".slide.on");const f=s.querySelector("footer").getBoundingClientRect();
              let low=0;[...s.children].forEach(e=>{if(e.tagName!=="FOOTER"){const r=e.getBoundingClientRect();low=Math.max(low,r.bottom)}});
              const top=Math.min(...[...s.children].filter(e=>e.tagName!=="FOOTER").map(e=>e.getBoundingClientRect().top));
              return {contentBottom:low,contentTop:top,footTop:f.top,links:[...s.querySelectorAll("footer a")].length,vh:innerHeight}}''')
            if r['contentBottom'] > r['footTop'] - 4: probs.append((name, i+1, f'內容與頁尾重疊（內容底 {r["contentBottom"]:.0f} > 頁尾頂 {r["footTop"]:.0f}）'))
            if r['contentTop'] < 0: probs.append((name, i+1, '內容超出畫面上緣'))
            if r['links'] == 0: probs.append((name, i+1, '頁尾沒有 Wiki 引用'))
            if name == 'desk' or i in (3, 7): pg.screenshot(path=f'shots/{name}-{i+1:02d}.png')
        if errs: probs.append((name, 0, 'console 錯誤：' + '; '.join(errs)))
    b.close()
# 頁尾連結都要指到存在的檔案
html = open(root + '/slides/index.html', encoding='utf-8').read()
for l in sorted(set(re.findall(r'href="\.\./([^"]+)"', html))):
    if not os.path.exists(os.path.join(root, l)): probs.append(('link', 0, f'失效連結 {l}'))
# 簡報文字與 JSON 一致
d = json.load(open('draft_v3.json', encoding='utf-8'))
import html as H
for s in d['slides']:
    for bl in s['bullets']:
        if H.escape(bl['text']) not in html: probs.append(('text', s['id'], '簡報文字與稿件不一致'))
print(f'發現 {len(probs)} 個問題')
for pr in probs: print('-', pr)

# 導覽檢查：每一頁都走得回首頁、沒有連到自己、沒有失效連結
import glob
probs2 = []
for f in glob.glob(root + '/**/*.html', recursive=True):
    txt = open(f, encoding='utf-8').read()
    d = os.path.dirname(f)
    targets = [os.path.normpath(os.path.join(d, l)) for l in re.findall(r'href="([^"#]+)"', txt) if not l.startswith('http')]
    for l in re.findall(r'href="([^"#]+)"', txt):
        if not l.startswith('http') and not os.path.exists(os.path.join(d, l)): probs2.append((f[len(root):], f'失效連結 {l}'))
    if f != root + '/index.html':
        if root + '/index.html' not in targets: probs2.append((f[len(root):], '沒有連回首頁'))
        if f in targets: probs2.append((f[len(root):], '連到自己'))
print(f'導覽檢查：發現 {len(probs2)} 個問題')
for p in probs2: print('-', p)

# 教學結構檢查：除了封面與學習地圖，每一頁上方都要標出所屬部分
h = open(root + '/slides/index.html', encoding='utf-8').read()
secs = re.findall(r'<section class="([^"]*)"', h)
nochip = [i + 1 for i, s in enumerate(re.findall(r'<section class="[^"]*".*?</section>', h, re.S)) if 'title' not in secs[i] and 'agenda' not in secs[i] and 'class="chip"' not in s]
print('教學結構檢查：每頁都標示所屬部分' if not nochip else f'教學結構檢查：這些頁沒有標示所屬部分 {nochip}')
