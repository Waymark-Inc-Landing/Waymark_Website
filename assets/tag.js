/* Google tag for Waymark Inc.
 *
 * FILL IN the four values below once the Google Ads account exists. Until AW_ID is
 * set, this file loads nothing, sends nothing, and logs nothing — it is safe to ship
 * empty. wmTrack() always exists so the rest of the site never has to check.
 *
 *   AW_ID        Google Ads → Admin → Account settings. Looks like AW-1234567890.
 *   CONVERSIONS  Goals → Conversions → open the action → Tag setup → "Use Google tag".
 *                Copy the whole send_to string, e.g. AW-1234567890/AbC-D_efGhIjKlM
 */
(function () {
  var AW_ID = '';
  var CONVERSIONS = {
    lead: '',     // contact form submitted
    call: '',     // tapped the phone number
    booking: ''   // clicked through to the booking page
  };

  window.wmTrack = function () {};
  if (!AW_ID) return;

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  // waymarkcoach.com hosts the booking flow, so measurement has to survive the hop.
  gtag('config', AW_ID, { linker: { domains: ['waymarkinc.com', 'waymarkcoach.com'] } });

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(AW_ID);
  document.head.appendChild(s);

  window.wmTrack = function (name, params) {
    var label = CONVERSIONS[name];
    if (!label) return;
    var data = { send_to: label };
    if (params) { for (var k in params) { data[k] = params[k]; } }
    gtag('event', 'conversion', data);
  };
})();
