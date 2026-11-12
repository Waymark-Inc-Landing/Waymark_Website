// Runs before the first paint, so the page never flashes from one state to another.
//   motion — the visitor has not asked their device to reduce motion: scroll effects are on.
//   seen   — the opening screen has already played in this browser session: skip it.
// Append ?motion=on to a page URL to see the animated version on a device that has
// Reduce Motion switched on, or ?motion=off to see the still version (either is remembered
// in that browser); ?motion=auto goes back to following the device setting.
(function () {
  var d = document.documentElement, c = ' js', force = null;
  try {
    var q = /[?&]motion=(on|off|auto)\b/.exec(location.search);
    if (q) { if (q[1] === 'auto') localStorage.removeItem('wm-motion'); else localStorage.setItem('wm-motion', q[1]); }
    force = localStorage.getItem('wm-motion');
  } catch (e) {}
  var reduce = false;
  try { reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}
  if (force === 'on' || (!reduce && force !== 'off')) c += ' motion';
  try {
    if (sessionStorage.getItem('wm-seen')) c += ' seen'; else sessionStorage.setItem('wm-seen', '1');
  } catch (e) {}
  d.className += c;
})();
