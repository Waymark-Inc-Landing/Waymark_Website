/* Behaviour for the shared header on inner pages (markup from tools/shell.py):
   the header turns solid once the hero has scrolled away, the phone menu opens and
   closes, and .reveal elements fade in as they come into view. */
(function () {
  var root = document.documentElement;
  var motion = root.classList.contains('motion');   // set before first paint by assets/pre.js
  var header = document.getElementById('wmHead');
  var hero = document.querySelector('.wm-hero');
  var menu = document.getElementById('wmMobile');
  var btn = document.getElementById('wmMenuBtn');
  if (!header) { return; }

  var lastY = 0;
  var onScroll = function () {
    var y = window.scrollY || 0;
    var edge = hero ? Math.max(24, hero.offsetHeight - 120) : 24;
    header.classList.toggle('scrolled', y > edge);
    if (motion) {
      var open = menu && menu.classList.contains('open');
      header.classList.toggle('hide', y > edge + 200 && y > lastY + 2 && !open);
      if (Math.abs(y - lastY) > 2) { lastY = y; }
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (btn && menu) {
    var setMenu = function (open) {
      menu.classList.toggle('open', open);
      header.classList.toggle('menu-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    };
    btn.addEventListener('click', function () { setMenu(!menu.classList.contains('open')); });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
  }

  var items = document.querySelectorAll('.reveal');
  if (motion && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Whatever happened to the entrance animations, the hero text ends up visible.
  setTimeout(function () { root.classList.add('shown'); }, 2600);

  var year = document.getElementById('wmYear');
  if (year) { year.textContent = String(new Date().getFullYear()); }
})();
