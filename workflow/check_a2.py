# 檢查 A2：貼近度。每條稿件句子，和所引用 Wiki 頁中「最接近的一句」比對字元 bigram 重疊率，偏低的列出來人工看
import json, re, sys
W = '../wiki/concepts/'
slides = json.load(open(sys.argv[1], encoding='utf-8'))['slides']
def bg(s):
    s = re.sub(r'\[S\d\]|[\s，。、；：「」（）()\-–·]', '', s)
    return {s[i:i+2] for i in range(len(s)-1)}
res = []
for s in slides:
    for b in s['bullets']:
        lines = []
        for p in b['pages']:
            lines += [re.sub(r'\[S\d\]', '', l) for l in open(W+p+'.md', encoding='utf-8').read().split('\n') if l.startswith(('- ', '> '))]
        a = bg(b['text'])
        best = max((len(a & bg(l)) / max(1, len(a)) for l in lines), default=0)
        res.append((best, s['id'], b['text']))
res.sort()
for r, i, t in res[:8]:
    print(f'{r:.2f}  第{i}頁  {t}')
