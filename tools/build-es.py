#!/usr/bin/env python3
"""Generate es/index.html (the Spanish homepage) from index.html + the ES dictionary in assets/app.js.

Run this after ANY change to index.html or to the ES dictionary:

    python3 tools/build-es.py

Both languages then stay one source of truth: the English markup and the ES strings.
"""
import json
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


# JSON-LD is machine-readable text, and the data-i18n pass never touches it — it only
# rewrites elements carrying a data-i18n attribute. So the Spanish page was shipping English
# structured data: an English LocalBusiness description and five English FAQ questions, on the
# page a Spanish speaker's AI assistant actually reads. These are the strings we own.
LD_ES = {
    'Faith-based Christian marriage coaching ministry offering couples coaching, marriage '
    'restoration, spiritual direction, boundary coaching, premarital guidance, and coach '
    'training \u2014 in English and Spanish, in person and online.':
        'Coaching matrimonial cristiano basado en la fe: coaching para parejas, restauraci\u00f3n '
        'matrimonial, direcci\u00f3n espiritual, coaching de l\u00edmites, orientaci\u00f3n prematrimonial y '
        'formaci\u00f3n de coaches \u2014 en espa\u00f1ol e ingl\u00e9s, en persona y en l\u00ednea.',

    '$100 per session': '$100 por sesi\u00f3n',

    'Couples Coaching': 'Coaching para parejas',
    'Marriage Restoration Coaching': 'Coaching de restauraci\u00f3n matrimonial',
    'Spiritual Direction': 'Direcci\u00f3n espiritual',
    'Boundary Coaching': 'Coaching de l\u00edmites',
    'Premarital Guidance': 'Orientaci\u00f3n prematrimonial',
    'Coach Training': 'Formaci\u00f3n de coaches',

    'What kind of help does Waymark provide?': '\u00bfQu\u00e9 tipo de ayuda ofrece Waymark?',
    'Waymark provides faith-based marriage coaching, not counseling or therapy. Coaching here '
    'means structured, practical work on a marriage: a clear plan worked through session by '
    "session, built on Dr. Jim Talley's decades of relationship work. We are coaches \u2014 not "
    'licensed counselors or therapists. We do not diagnose and we do not treat mental health '
    'conditions. If licensed care is what you need, we will say so plainly and help you find it.':
        'Waymark ofrece coaching matrimonial basado en la fe, no consejer\u00eda ni terapia. Aqu\u00ed el '
        'coaching significa trabajo pr\u00e1ctico y estructurado sobre el matrimonio: un plan claro que '
        'se recorre sesi\u00f3n por sesi\u00f3n, apoyado en las d\u00e9cadas de trabajo con parejas del Dr. Jim '
        'Talley. Somos coaches, no consejeros licenciados ni terapeutas. No hacemos diagn\u00f3sticos y '
        'no tratamos condiciones de salud mental. Si lo que necesitan es un profesional licenciado, '
        'se lo diremos con claridad y les ayudaremos a buscarlo.',

    'Do you work with couples outside Oklahoma?': '\u00bfTrabajan con parejas fuera de Oklahoma?',
    'Yes. Most sessions happen by phone or video, so we walk with couples and individuals anywhere '
    'in the United States. In-person sessions are available in Shawnee, OK.':
        'S\u00ed. La mayor\u00eda de las sesiones son por tel\u00e9fono o video, as\u00ed que acompa\u00f1amos a parejas y '
        'personas en cualquier parte de Estados Unidos. Tambi\u00e9n hay sesiones en persona en Shawnee, OK.',

    'Do you offer sessions in Spanish?': '\u00bfOfrecen sesiones en espa\u00f1ol?',
    'Yes. Coaching is available in English and Spanish, and so is this entire site.':
        'S\u00ed. El coaching est\u00e1 disponible en espa\u00f1ol e ingl\u00e9s, y este sitio completo tambi\u00e9n.',

    'What happens in the first conversation?': '\u00bfQu\u00e9 pasa en la primera conversaci\u00f3n?',
    'A straightforward conversation about where things stand and what the next honest step is, '
    'with no pressure and no judgment. You can book one online or call (405) 822-8300.':
        'Una conversaci\u00f3n directa sobre c\u00f3mo est\u00e1n las cosas y cu\u00e1l es el siguiente paso honesto, '
        'sin presi\u00f3n y sin juicio. Pueden agendarla en l\u00ednea o llamar al (405) 822-8300.',

    'What is marriage restoration?': '\u00bfQu\u00e9 es la restauraci\u00f3n matrimonial?',
    'An intensive, guided path for marriages on the brink: nine sessions of proven steps that move '
    'a couple from separation back toward a lasting covenant. It is more structured than general '
    'couples coaching.':
        'Un camino intensivo y guiado para matrimonios al borde de la ruptura: nueve sesiones de '
        'pasos comprobados que llevan a una pareja de la separaci\u00f3n de regreso hacia un pacto '
        'duradero. Es m\u00e1s estructurado que el coaching general de parejas.',
}


def translate_jsonld(soup: BeautifulSoup) -> int:
    """Swap the English strings in every JSON-LD block for their Spanish counterparts."""
    hits = [0]

    def walk(node):
        if isinstance(node, str):
            if node in LD_ES:
                hits[0] += 1
                return LD_ES[node]
            return node
        if isinstance(node, dict):
            return {k: walk(v) for k, v in node.items()}
        if isinstance(node, list):
            return [walk(x) for x in node]
        return node

    for el in soup.select('script[type="application/ld+json"]'):
        try:
            data = json.loads(el.string or '')
        except (TypeError, ValueError):
            continue
        el.string = json.dumps(walk(data), ensure_ascii=False, indent=2)
    return hits[0]


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

    translated = translate_jsonld(soup)
    if translated < 15:
        print('ERROR: only %d JSON-LD strings translated — index.html wording drifted '
              'away from LD_ES in this script. Fix the table before shipping.' % translated)
        return 1
    print('translated %d JSON-LD strings' % translated)

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
    # The booking flow speaks Spanish, but only when asked: CLCM_I18n::current_lang()
    # reads a logged-in user's meta or the clcm_lang cookie, and a cold visitor has
    # neither. Without this the Spanish pages hand Spanish speakers an English form.
    for el in soup.select('a[href^="https://waymarkcoach.com/book"]'):
        el['href'] = 'https://waymarkcoach.com/book/?clcm_lang=es'

    for b in soup.select('.lang-toggle button'):
        b['class'] = [c for c in b.get('class', []) if c != 'active'] + (
            ['active'] if b.get('data-lang') == 'es' else [])

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(str(soup))
    print('wrote %s (%d Spanish strings applied)' % (os.path.relpath(OUT, ROOT), len(ES)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
