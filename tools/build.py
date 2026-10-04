#!/usr/bin/env python3
"""content/<slug>.html (本文の断片) と tools/lessons.json から、lessons/*.html と index.html を生成する。"""
import json, os, html
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
meta = json.load(open(os.path.join(root, 'tools/lessons.json'), encoding='utf8'))
BASE = 'https://studio.blender.org/training/blender-fundamentals-45-lts/'
done = [l for l in meta['lessons'] if os.path.exists(f"{root}/content/{l['slug']}.html")]
order = [l['slug'] for l in done]
os.makedirs(f'{root}/lessons', exist_ok=True)
for i, l in enumerate(done):
    body = open(f"{root}/content/{l['slug']}.html", encoding='utf8').read()
    prev = f'<a href="{done[i-1]["slug"]}.html">← {done[i-1]["ja"]}</a>' if i else '<span></span>'
    nxt = f'<a href="{done[i+1]["slug"]}.html">{done[i+1]["ja"]} →</a>' if i + 1 < len(done) else '<span></span>'
    open(f"{root}/lessons/{l['slug']}.html", 'w', encoding='utf8').write(f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{l['ja']} - Blender基礎 4.5 LTS 日本語ガイド</title>
<link rel="stylesheet" href="../style.css"></head><body><main>
<p><a href="../index.html">← 目次へ</a></p>
<h1>{l['ja']}</h1>
<p class="note">Blender Studio「Blender Fundamentals 4.5 LTS」の無料レッスンを、日本語で要点をまとめた非公式の学習ガイドです(逐語訳ではありません)。原文: <a href="{BASE}{l['url']}/">{html.escape(l['en'])}</a></p>
{body}
<nav class="pager">{prev}{nxt}</nav>
</main></body></html>
''')
out = ['''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Blender基礎 4.5 LTS 日本語ガイド</title>
<link rel="stylesheet" href="style.css"></head><body><main>
<h1>Blender基礎 4.5 LTS 日本語ガイド</h1>
<p class="note">Blender Studio の無料コース <a href="https://studio.blender.org/training/blender-fundamentals-45-lts/">Blender Fundamentals 4.5 LTS</a> の Free レッスンを日本語でまとめた非公式の学習ガイドです。内容は要点の言い換えで、詳細は原文を参照してください。</p>
<h2>目次(Free レッスン)</h2>''']
chap = None
n = 0
for l in meta['lessons']:
    if l['chapter'] != chap:
        if chap: out.append('</ol>')
        chap = l['chapter']; out.append(f'<h3>{meta["chapters"][str(chap)]}</h3><ol class="toc" start="{n+1}">')
    n += 1
    if l['slug'] in order: out.append(f'<li><a href="lessons/{l["slug"]}.html">{l["ja"]}</a></li>')
    else: out.append(f'<li class="todo">{l["ja"]}(準備中)</li>')
out.append('</ol></main></body></html>\n')
open(f'{root}/index.html', 'w', encoding='utf8').write('\n'.join(out))
print(len(done), '/', len(meta['lessons']))
