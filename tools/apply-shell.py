#!/usr/bin/env python3
"""Put the shared header and footer (tools/shell.py) into the hand-built pages.

    python3 tools/apply-shell.py

Safe to run again: the header and footer sit between <!-- shell:... --> markers and are
rewritten in place, so a change to the navigation reaches every page. The first run also
moved each page's title block into the dark hero and wrapped the rest in the cream body.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shell  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# file, language, the same page in the other language
PAGES = [
    ('dr-jim-talley/index.html', 'en', '/es/dr-jim-talley/'),
    ('es/dr-jim-talley/index.html', 'es', '/dr-jim-talley/'),
    ('blog/your-worth-does-not-depend-on-your-performance.html', 'en', '/blog/tu-valor-no-depende-de-tu-rendimiento.html'),
    ('blog/tu-valor-no-depende-de-tu-rendimiento.html', 'es', '/blog/your-worth-does-not-depend-on-your-performance.html'),
    ('es/coaching-matrimonial/index.html', 'es', '/'),
]


def block(name: str, body: str) -> str:
    return '<!-- shell:%s -->\n%s\n<!-- /shell:%s -->' % (name, body, name)


def put(s: str, name: str, body: str, first_time: str) -> str:
    """Replace the marked block, or on the first run the pattern it takes the place of."""
    marked = re.compile(r'<!-- shell:%s -->.*?<!-- /shell:%s -->' % (name, name), re.S)
    if marked.search(s):
        return marked.sub(lambda m: block(name, body), s, count=1)
    old = re.compile(first_time, re.S)
    if not old.search(s):
        raise SystemExit('cannot place shell:%s' % name)
    return old.sub(lambda m: block(name, body), s, count=1)


def main() -> int:
    for rel, lang, other in PAGES:
        p = os.path.join(ROOT, rel)
        s = open(p, encoding='utf-8').read()
        if '<!-- shell:head -->' not in s:
            s = s.replace('</style>', '</style>\n' + block('head', shell.HEAD_ASSETS), 1)
        else:
            s = put(s, 'head', shell.HEAD_ASSETS, r'$^')
        s = put(s, 'header', shell.header(lang, other), r'<header class="bar">.*?</header>')
        s = put(s, 'footer', shell.footer(lang, other) + '\n' + shell.FOOT_SCRIPT, r'<footer>.*?</footer>')
        open(p, 'w', encoding='utf-8').write(s)
        print('shell applied to', rel)
    return 0


if __name__ == '__main__':
    sys.exit(main())
