# 檢查 A：內容檢查（產生簡報之前）
import json, re, sys, os
W = '../wiki'
slides = json.load(open(sys.argv[1]))['slides']
FORBID = ['延後回饋', 'delayed feedback']
def page_text(p):
    t = open(f'{W}/concepts/{p}.md', encoding='utf-8').read()
    t = re.sub(r'\[S\d\]', '', t)
    t = re.sub(r'\(\.\./sources/[^)]*\)|\([a-z\-]+\.md\)', '', t)
    return t
def tags_in_page(p):
    return set(re.findall(r'\[S\d\]', open(f'{W}/concepts/{p}.md', encoding='utf-8').read()))
problems = []
for s in slides:
    for b in s['bullets']:
        txt = b['text']
        tags = re.findall(r'\[S\d\]', txt)
        loc = f"第{s['id']}頁「{s['title']}」"
        if not tags:
            problems.append((loc, txt, '句尾沒有 [S#] 來源標記'))
        for p in b['pages']:
            if not os.path.exists(f'{W}/concepts/{p}.md'):
                problems.append((loc, txt, f'引用的 Wiki 頁不存在：{p}'))
                continue
            pt = tags_in_page(p)
        # 標記必須出現在至少一個引用頁
        for t in tags:
            if not any(t in tags_in_page(p) for p in b['pages'] if os.path.exists(f'{W}/concepts/{p}.md')):
                problems.append((loc, txt, f'{t} 沒有出現在所引用的 Wiki 頁'))
        # 數字必須出現在引用頁
        body = re.sub(r'\[S\d\]', '', txt)
        nums = re.findall(r'\d+(?:\.\d+)?', body)
        ptxt = ' '.join(page_text(p) for p in b['pages'] if os.path.exists(f'{W}/concepts/{p}.md'))
        ptoks = set(re.findall(r'\d+(?:\.\d+)?', ptxt))
        for n in nums:
            if n not in ptoks:
                problems.append((loc, txt, f'數字 {n} 沒有出現在所引用的 Wiki 頁'))
        for f in FORBID:
            if f in txt:
                problems.append((loc, txt, f'含有不得使用的內容：{f}'))
print(f'檢查 {sum(len(s["bullets"]) for s in slides)} 條，發現 {len(problems)} 個問題')
for loc, txt, why in problems:
    print(f'- {loc}：{why}\n    {txt}')
