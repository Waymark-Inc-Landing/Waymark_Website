#!/usr/bin/env python3
"""Generate es/index.html (the Spanish homepage) from index.html + the ES dictionary in assets/app.js.

Run this after ANY change to index.html or to the ES dictionary:

    python3 tools/build-es.py

Both languages then stay one source of truth: the English markup and the ES strings.
"""
import os
import re
import sys

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'index.html')
APP = os.path.join(ROOT, 'assets', 'app.js')
OUT = os.path.join(ROOT, 'es', 'index.html')

ES_TITLE = 'Waymark Inc. | Coaching cristiano para parejas y matrimonios | Shawnee, OK'
ES_DESC = ('Coaching de parejas basado en la fe, restauración matrimonial y dirección espiritual '
           'en Shawnee, OK y en línea, en español e inglés. Con más de 50 años de acompañamiento '
           'del Dr. Jim Talley. Llama al (405) 822-8300.')


def es_dictionary(js: str) -> dict:
    """Pull the ES object literal out of app.js. Each entry is one line: 'key':'value',"""
    start = js.index('var ES = {')
    end = js.index('\n  };', start)
    out = {}
    for line in js[start:end].split('\n'):
        m = re.match(r"\s*'([A-Za-z0-9_-]+)'\s*:\s*'(.*?)',?\s*$", line)
        if m:
            out[m.group(1)] = m.group(2).replace("\\'", "'")
    return out


def absolutise(soup: BeautifulSoup) -> None:
    """The Spanish page lives one level down, so relative paths need a leading slash."""
    for tag, attr in (('img', 'src'), ('script', 'src'), ('link', 'href'), ('a', 'href'),
                      ('video', 'src'), ('video', 'poster'), ('source', 'src')):
        for el in soup.find_all(tag):
            v = el.get(attr)
            if v and not v.startswith(('/', '#', 'http', 'mailto:', 'tel:', 'data:')):
                el[attr] = '/' + v


def main() -> int:
    html = open(SRC, encoding='utf-8').read()
    ES = es_dictionary(open(APP, encoding='utf-8').read())
    if len(ES) < 100:
        print('ES dictionary looks too small (%d keys) — aborting' % len(ES))
        return 1

    soup = BeautifulSoup(html, 'html.parser')

    missing = []
    for el in soup.select('[data-i18n]'):
        key = el['data-i18n']
        if key in ES:
            el.clear()
            el.append(BeautifulSoup(ES[key], 'html.parser'))
        else:
            missing.append(key)
    if missing:
        print('WARNING: no Spanish for %s' % ', '.join(sorted(set(missing))))

    absolutise(soup)

    soup.html['lang'] = 'es'
    soup.html['data-static-lang'] = 'es'

    soup.title.string = ES_TITLE
    for sel, attr, val in (
        ('meta[name="description"]', 'content', ES_DESC),
        ('meta[property="og:title"]', 'content', ES_TITLE),
        ('meta[property="og:description"]', 'content', ES_DESC),
        ('meta[property="og:url"]', 'content', 'https://www.waymarkinc.com/es/'),
        ('meta[property="og:locale"]', 'content', 'es_US'),
        ('meta[name="twitter:title"]', 'content', ES_TITLE),
        ('meta[name="twitter:description"]', 'content', ES_DESC),
        ('link[rel="canonical"]', 'href', 'https://www.waymarkinc.com/es/'),
    ):
        el = soup.select_one(sel)
        if el:
            el[attr] = val

    # language pairing
    for el in soup.select('link[rel="alternate"]'):
        el.decompose()
    head = soup.head
    for lang, href in (('es', 'https://www.waymarkinc.com/es/'),
                       ('en', 'https://www.waymarkinc.com/'),
                       ('x-default', 'https://www.waymarkinc.com/')):
        link = soup.new_tag('link', rel='alternate', href=href)
        link['hreflang'] = lang
        head.append(link)

    # language-dependent links, baked in rather than swapped by script
    for el in soup.select('a[data-fb]'):
        el['href'] = 'https://www.facebook.com/waymarkespanol'
    for el in soup.select('a[data-ig]'):
        el['href'] = 'https://www.instagram.com/waymarkespanol/'
    for el in soup.select('a[href="/dr-jim-talley/"]'):
        el['href'] = '/es/dr-jim-talley/'

    for b in soup.select('.lang-toggle button'):
        b['class'] = [c for c in b.get('class', []) if c != 'active'] + (
            ['active'] if b.get('data-lang') == 'es' else [])

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(str(soup))
    print('wrote %s (%d Spanish strings applied)' % (os.path.relpath(OUT, ROOT), len(ES)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
