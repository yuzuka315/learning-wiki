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
d = json.load(open('draft_v2.json', encoding='utf-8'))
import html as H
for s in d['slides']:
    for bl in s['bullets']:
        if H.escape(bl['text']) not in html: probs.append(('text', s['id'], '簡報文字與稿件不一致'))
print(f'發現 {len(probs)} 個問題')
for pr in probs: print('-', pr)
