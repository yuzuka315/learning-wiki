import json, re, html, sys
src = sys.argv[1]
d = json.load(open(src, encoding='utf-8'))
W = '../wiki/concepts/'
def ptitle(p):
    return re.match(r'# (.+)', open(f'{W}{p}.md', encoding='utf-8').read()).group(1)
CURVE = '''<figure class="fig"><svg class="curve" viewBox="0 0 360 170" role="img" aria-label="遺忘曲線示意圖：不複習會下降，每次複習後下降變慢">
<line x1="30" y1="140" x2="350" y2="140" class="ax"/><line x1="30" y1="15" x2="30" y2="140" class="ax"/>
<path d="M30 25 C 70 90, 110 118, 190 128" class="c1"/>
<path d="M30 25 C 55 70, 80 85, 110 88 L110 40 C 140 70, 175 80, 215 84 L215 40 C 250 60, 290 68, 345 72" class="c2"/>
<text x="195" y="124" class="lb">不複習</text><text x="222" y="30" class="lb2">複習後曲線變平</text>
<text x="34" y="12" class="lb">記憶保留</text><text x="300" y="158" class="lb">時間 →</text></svg>
<p class="cap">示意圖（非實測數據）：不複習會下降；每次複習後，下降變慢。</p></figure>'''
slides = []
for s in d['slides']:
    cls = 'slide title' if s.get('kind') == 'title' else 'slide'
    lis = ''.join(f'<li>{html.escape(b["text"])}</li>' for b in s['bullets'])
    if s['id'] == 1:
        body = f'<h1>{html.escape(s["title"])}</h1><p class="sub">給第一次接觸這個主題的人</p><ul class="src">{lis}</ul>'
    else:
        extra = CURVE if s['id'] == 4 else ''
        body = f'<h2>{html.escape(s["title"])}</h2><div class="cols"><ul>{lis}</ul>{extra}</div>'
    pages = []
    for b in s['bullets']:
        for p in b['pages']:
            if p not in pages: pages.append(p)
    foot = '本頁依據 Wiki：' + '、'.join(f'<a href="../wiki/concepts/{p}.html">{html.escape(ptitle(p))}</a>' for p in pages)
    if s['id'] == 1:
        foot = '本簡報內容全部取自 <a href="../wiki/index.html">高效學習法 Wiki</a>'
    slides.append(f'<section class="{cls}" data-n="{s["id"]}">{body}<footer>{foot}</footer></section>')
CSS = '''
:root{--bg:#f6f4ee;--fg:#1f2430;--mut:#5d6575;--ac:#1d5c63;--ac2:#c2562b;--card:#fffdf8;--ln:#d9d3c4}
@media(prefers-color-scheme:dark){:root{--bg:#171a20;--fg:#ecebe6;--mut:#a3a9b6;--ac:#6cc4cc;--ac2:#f09a73;--card:#20242c;--ln:#363c48}}
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{background:var(--bg);color:var(--fg);font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;overflow:hidden}
.deck{height:100%;position:relative}
.slide{position:absolute;inset:0;display:none;flex-direction:column;justify-content:center;padding:6vh 8vw 9vh;gap:3vh}
.slide.on{display:flex}
h1{font-size:clamp(2rem,5.4vw,4rem);margin:0;line-height:1.2;color:var(--ac)}
h2{font-size:clamp(1.5rem,3.4vw,2.5rem);margin:0;padding-bottom:1.4vh;border-bottom:3px solid var(--ac2);width:fit-content;max-width:100%}
.sub{font-size:clamp(1rem,2vw,1.5rem);color:var(--mut);margin:0}
.cols{display:flex;gap:4vw;align-items:center;flex-wrap:wrap}
ul{margin:0;padding-left:1.3em;flex:1 1 360px;font-size:clamp(1.05rem,2.1vw,1.6rem);line-height:1.65}
li{margin:.55em 0}li::marker{color:var(--ac2)}
ul.src{font-size:clamp(.9rem,1.5vw,1.15rem);color:var(--mut);flex:none}
.curve{flex:0 1 380px;width:100%;max-width:380px;background:var(--card);border:1px solid var(--ln);border-radius:10px;padding:8px}
.curve .ax{stroke:var(--mut);stroke-width:1.5}.curve .c1{fill:none;stroke:var(--ac2);stroke-width:3}.curve .c2{fill:none;stroke:var(--ac);stroke-width:3}
.curve text{font-size:11px;fill:var(--fg)}
.fig{flex:0 1 380px;margin:0}.fig .curve{max-width:none}.cap{font-size:.85rem;color:var(--mut);margin:.6em 0 0}
footer{position:absolute;left:8vw;right:8vw;bottom:4.5vh;font-size:clamp(.75rem,1.2vw,.95rem);color:var(--mut);border-top:1px solid var(--ln);padding-top:1vh}
footer a{color:var(--ac)}
nav{position:fixed;right:2vw;bottom:1.2vh;display:flex;gap:8px;align-items:center;font-size:.85rem;color:var(--mut)}
nav a{color:var(--ac);margin-right:6px}nav button{background:var(--card);color:var(--fg);border:1px solid var(--ln);border-radius:6px;padding:4px 12px;cursor:pointer;font-size:1rem}
.bar{position:fixed;left:0;top:0;height:4px;background:var(--ac2);transition:width .2s}
@media print{body{overflow:visible}.slide{display:flex!important;position:relative;height:100vh;page-break-after:always}nav,.bar{display:none}}
'''
JS = '''
(function(){var s=[].slice.call(document.querySelectorAll(".slide")),i=0,c=document.getElementById("c"),b=document.querySelector(".bar");
function go(n){i=Math.max(0,Math.min(s.length-1,n));s.forEach(function(e,k){e.classList.toggle("on",k===i)});c.textContent=(i+1)+" / "+s.length;b.style.width=((i+1)/s.length*100)+"%";try{history.replaceState(null,"","#"+(i+1))}catch(e){}}
document.getElementById("p").onclick=function(){go(i-1)};document.getElementById("n").onclick=function(){go(i+1)};
document.addEventListener("keydown",function(e){if(e.key==="ArrowRight"||e.key===" "||e.key==="PageDown")go(i+1);if(e.key==="ArrowLeft"||e.key==="PageUp")go(i-1)});
var h=parseInt(location.hash.slice(1),10);go(h?h-1:0)})();
'''
out = f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(d["title"])}</title><style>{CSS}</style></head>
<body><div class="bar"></div><div class="deck">{''.join(slides)}</div>
<nav><a href="../index.html">首頁</a><button id="p" aria-label="上一頁">←</button><span id="c"></span><button id="n" aria-label="下一頁">→</button></nav>
<script>{JS}</script></body></html>'''
open('../slides/index.html', 'w', encoding='utf-8').write(out)
print('slides:', len(slides))
