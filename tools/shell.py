"""The header and footer every inner page shares with the homepage.

tools/build-services.py writes them into the service pages, and tools/apply-shell.py
writes them into the hand-built pages (Dr. Talley, the blog posts, the ad landing page)
between <!-- shell:... --> markers. Styles: assets/shell.css. Behaviour: assets/shell.js.
"""

# English service slug -> Spanish slug, in footer order. Same pairs as build-services.py.
FOOT_SERVICES = [
    ('couples-coaching', 'Couples Coaching', 'coaching-para-parejas', 'Coaching para parejas'),
    ('marriage-restoration', 'Marriage Restoration', 'restauracion-matrimonial', 'Restauración matrimonial'),
    ('spiritual-direction', 'Spiritual Direction', 'direccion-espiritual', 'Dirección espiritual'),
    ('premarital-guidance', 'Premarital Guidance', 'orientacion-prematrimonial', 'Orientación prematrimonial'),
    ('rebuilding-after-divorce', 'Rebuilding After Divorce', 'reconstruccion-tras-el-divorcio', 'Reconstrucción tras el divorcio'),
    ('coaching-for-ministers-and-leaders', 'Coaching for Ministers &amp; Leaders', 'coaching-para-ministros-y-lideres', 'Coaching para ministros y líderes'),
    ('online-christian-marriage-coaching', 'Online Coaching', 'coaching-matrimonial-cristiano-en-linea', 'Coaching en línea'),
    ('coach-training', 'Coach Training', 'formacion-de-coaches', 'Formación de coaches'),
]

T = {
    'en': {
        'home': '/', 'aria': 'Waymark Inc. — Marking the way back',
        'nav': [('#about', 'Our Story'), ('#services', 'Coaching'), ('#training', 'Training'),
                ('#books', 'Resources'), ('#blog', 'Blog')],
        'cta': 'Begin the journey', 'menu': 'Open menu', 'other': 'Español', 'other_code': 'es',
        'brand_p': 'Helping couples and individuals find the path home — through coaching and guidance rooted in five decades of relationship restoration. Continuing the legacy of Dr. Jim Talley.',
        'explore': 'Explore', 'coaching': 'Coaching', 'connect': 'Connect', 'contact': 'Contact',
        'rights': 'All rights reserved. · In loving memory of Dr. Jim Talley.',
        'fb': 'https://www.facebook.com/waymarkinc', 'ig': 'https://www.instagram.com/waymarkinc/',
        'on': 'Waymark on', 'wa': 'Message Waymark on WhatsApp', 'yv': 'Waymark on the YouVersion Bible App',
    },
    'es': {
        'home': '/es/', 'aria': 'Waymark Inc. — Marcando el camino de regreso',
        'nav': [('#about', 'Nuestra Historia'), ('#services', 'Coaching'), ('#training', 'Formación'),
                ('#books', 'Recursos'), ('#blog', 'Blog')],
        'cta': 'Comienza el camino', 'menu': 'Abrir menú', 'other': 'English', 'other_code': 'en',
        'brand_p': 'Ayudando a parejas y personas a encontrar el camino a casa, a través del coaching y el acompañamiento arraigados en cinco décadas de restauración de relaciones. Continuando el legado del Dr. Jim Talley.',
        'explore': 'Explorar', 'coaching': 'Coaching', 'connect': 'Comunícate', 'contact': 'Contacto',
        'rights': 'Todos los derechos reservados. · En memoria del Dr. Jim Talley.',
        'fb': 'https://www.facebook.com/waymarkespanol', 'ig': 'https://www.instagram.com/waymarkespanol/',
        'on': 'Waymark en', 'wa': 'Escribe a Waymark por WhatsApp', 'yv': 'Waymark en la app de la Biblia YouVersion',
    },
}

HEAD_ASSETS = ('<link rel="stylesheet" href="/assets/shell.css" />\n'
               '<script src="/assets/pre.js"></script>')
FOOT_SCRIPT = '<script src="/assets/shell.js" defer></script>'


def header(lang: str, other_href: str) -> str:
    """other_href: the same page in the other language."""
    t = T[lang]
    home = t['home']
    links = '\n      '.join('<a class="navlink" href="%s%s">%s</a>' % (home, h, label) for h, label in t['nav'])
    mlinks = '\n  '.join('<a href="%s%s">%s</a>' % (home, h, label) for h, label in t['nav'])
    lang_link = '<a class="wm-lang" href="%s" hreflang="%s">%s</a>' % (other_href, t['other_code'], t['other'])
    return f'''<div class="wm-head" id="wmHead" role="banner">
  <div class="wm-nav">
    <a href="{home}" class="wm-brand" aria-label="{t['aria']}">
      <img class="neg" src="/assets/waymark-logo-horizontal-negative.svg" alt="{t['aria']}" />
      <img class="lockup" src="/assets/waymark-logo-horizontal.svg" alt="" />
      <img class="symbol" src="/assets/waymark-logo-mobile.svg" alt="" />
    </a>
    <nav class="wm-links" aria-label="Primary">
      {links}
      <a class="wm-btn gold" href="{home}#contact">{t['cta']} <span aria-hidden="true">→</span></a>
      {lang_link}
    </nav>
    <div class="wm-actions">
      {lang_link}
      <button class="wm-menu-btn" id="wmMenuBtn" aria-label="{t['menu']}" aria-expanded="false">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>
</div>
<div class="wm-mobile" id="wmMobile">
  {mlinks}
  <a class="wm-btn gold" href="{home}#contact">{t['cta']}</a>
</div>'''


def footer(lang: str, other_href: str) -> str:
    t = T[lang]
    home = t['home']
    explore = '\n        '.join('<a href="%s%s">%s</a>' % (home, h, label) for h, label in t['nav'])
    if lang == 'en':
        services = '\n        '.join('<a href="/%s/">%s</a>' % (s[0], s[1]) for s in FOOT_SERVICES)
    else:
        services = '\n        '.join('<a href="/es/%s/">%s</a>' % (s[2], s[3]) for s in FOOT_SERVICES)
    return f'''<div class="wm-foot" role="contentinfo">
  <div class="wm-foot-in">
    <div class="wm-foot-grid">
      <div>
        <img class="lockup" src="/assets/waymark-logo-horizontal-negative.svg" alt="{t['aria']}" width="252" height="70" loading="lazy" />
        <p class="brand-p">{t['brand_p']}</p>
      </div>
      <div class="wm-foot-col">
        <h4>{t['explore']}</h4>
        {explore}
        <a href="{home}#contact">{t['contact']}</a>
        <a href="{other_href}" hreflang="{t['other_code']}">{t['other']}</a>
      </div>
      <div class="wm-foot-col">
        <h4>{t['coaching']}</h4>
        {services}
      </div>
      <div class="wm-foot-col">
        <h4>{t['connect']}</h4>
        <a href="tel:14058228300">(405) 822-8300</a>
        <a href="mailto:coaching@waymarkinc.com">coaching@waymarkinc.com</a>
        <span class="li">19223 Charleston Pointe<br />Shawnee, OK 74801</span>
      </div>
    </div>
    <div class="wm-foot-bottom">
      <span>© <span id="wmYear">2026</span> Waymark Inc. {t['rights']}</span>
      <div class="socials">
        <a href="{t['fb']}" target="_blank" rel="noopener" aria-label="{t['on']} Facebook"><img src="/assets/waymark-facebook-icon.png" alt="" width="38" height="38" loading="lazy" /></a>
        <a href="{t['ig']}" target="_blank" rel="noopener" aria-label="{t['on']} Instagram"><img src="/assets/waymark-instagram-icon.png" alt="" width="38" height="38" loading="lazy" /></a>
        <a href="https://www.youtube.com/@WaymarkInc" target="_blank" rel="noopener" aria-label="{t['on']} YouTube"><img src="/assets/waymark-youtube-icon.png" alt="" width="38" height="38" loading="lazy" /></a>
        <a href="https://wa.me/14058228300" target="_blank" rel="noopener" aria-label="{t['wa']}"><img src="/assets/waymark-whatsapp-icon.png" alt="" width="38" height="38" loading="lazy" /></a>
        <a href="https://www.bible.com/organizations/9590a5f6-7857-48f0-a82e-61268c694a67" target="_blank" rel="noopener" aria-label="{t['yv']}"><img src="/assets/waymark-youversion-icon.png" alt="" width="38" height="38" loading="lazy" /></a>
      </div>
    </div>
  </div>
</div>'''
