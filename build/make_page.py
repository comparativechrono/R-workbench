"""Write ../index.html: the page shell (template.html) with the chapters of the practical (chapters.py) in it, and the
list of the files that a new user finds in ~/data (everything in ../data, except its PROVENANCE.md).
Run:  python3 build/make_page.py"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import chapters  # noqa: E402

# the starter files: data/ of the site → ~/data/ of the user (data/penguins.csv → ~/data/penguins.csv)
STARTERS_VERSION = 1
starters = []
for root, dirs, files in os.walk(os.path.join(SITE, 'data')):
    dirs.sort()
    for f in sorted(files):
        rel = os.path.relpath(os.path.join(root, f), os.path.join(SITE, 'data')).replace(os.sep, '/')
        if rel in ('PROVENANCE.md',):
            continue
        starters.append({'p': rel, 's': os.path.getsize(os.path.join(root, f))})

html = '\n'.join(chapters.ALL())
# the first chapter is visible when the page loads
html = html.replace(' hidden>', '>', 1)
shell = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
a = shell.index('<!--CHAPTERS-->') + len('<!--CHAPTERS-->')
b = shell.index('<!--/CHAPTERS-->')
page = shell[:a] + '\n' + html + shell[b:]
page = page.replace('<!--STARTERS-->', '<script>window.RWB_STARTERS = ' + json.dumps(starters, separators=(',', ':')) +
                    f';\nwindow.RWB_STARTERS_VERSION = {STARTERS_VERSION};</script>')
open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(page)
# every task and question needs its own name
bad = False
for what, pat in (('task', r'data-task="([^"]+)"'), ('question', r'data-q="([^"]+)"'), ('heading', r'<h2 id="([^"]+)"')):
    ids = re.findall(pat, html)
    dup = sorted({x for x in ids if ids.count(x) > 1})
    print(f'{len(ids)} {what}s' + (f' – used twice: {dup}' if dup else ''))
    bad = bad or bool(dup)
print(len(html), 'bytes of chapters;', len(starters), 'starter files')
sys.exit(1 if bad else 0)
