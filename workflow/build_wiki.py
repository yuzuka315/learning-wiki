import markdown, re, glob, os, html
W = '../wiki'
CSS = '''body{max-width:760px;margin:0 auto;padding:24px 16px 64px;font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;line-height:1.75;color:#1f2430;background:#f6f4ee}
a{color:#1d5c63}h1{color:#1d5c63}blockquote{margin:0 0 1em;padding:.4em 1em;border-left:4px solid #c2562b;background:#fffdf8}
code{background:#ebe6d8;padding:1px 4px;border-radius:3px}.top{font-size:.9rem;margin-bottom:1.5rem}
@media(prefers-color-scheme:dark){body{background:#171a20;color:#ecebe6}a{color:#6cc4cc}h1{color:#6cc4cc}blockquote{background:#20242c}code{background:#2a2f39}}'''
for f in glob.glob(f'{W}/**/*.md', recursive=True):
    t = open(f, encoding='utf-8').read()
    t = re.sub(r'\]\(([^)]+?)\.md\)', r'](\1.html)', t)
    body = markdown.markdown(t)
    rel = os.path.relpath(W, os.path.dirname(f))
    title = re.match(r'# (.+)', t).group(1)
    home = rel + '/../index.html'
    if f.endswith('wiki/index.md'):
        top = f'<p class="top"><a href="{home}">首頁</a> / Wiki 目錄</p>'
    else:
        cur = '操作紀錄' if f.endswith('log.md') else html.escape(title)
        top = f'<p class="top"><a href="{home}">首頁</a> / <a href="{rel}/index.html">Wiki 目錄</a> / {cur}</p>'
    open(f[:-3] + '.html', 'w', encoding='utf-8').write(
      f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}｜高效學習法 Wiki</title><style>{CSS}</style></head><body>{top}{body}</body></html>')
print('ok')
