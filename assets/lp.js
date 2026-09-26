/* Landing-page behaviour: the contact form, and the three conversions worth counting. */
(function () {
  var form = document.getElementById('lpForm');

  // A tapped phone number and a click through to booking are both real intent.
  document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
    a.addEventListener('click', function () { window.wmTrack('call'); });
  });
  document.querySelectorAll('a[data-booking]').forEach(function (a) {
    a.addEventListener('click', function () { window.wmTrack('booking'); });
  });

  var year = document.getElementById('lpYear');
  if (year) { year.textContent = String(new Date().getFullYear()); }

  if (!form) { return; }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var btn = form.querySelector('button[type="submit"]');
    var status = form.querySelector('.form-status');
    if (!form.checkValidity()) { form.reportValidity(); return; }

    var orig = btn.innerHTML;
    btn.disabled = true;
    btn.textContent = 'Enviando…';
    status.style.display = 'none';

    var payload = {};
    new FormData(form).forEach(function (v, k) { payload[k] = v; });

    // Create the Lead in the Waymark platform too. Fire-and-forget, and
    // form-urlencoded so there is no CORS preflight to wait on.
    try {
      var lead = new URLSearchParams();
      ['name', 'email', 'phone', 'service', 'message', '_honey'].forEach(function (k) {
        lead.append(k, payload[k] || '');
      });
      fetch('https://waymarkcoach.com/wp-json/lms/v1/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: lead.toString()
      }).catch(function () {});
    } catch (err) {}

    fetch('https://formsubmit.co/ajax/coaching@waymarkinc.com', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (j.success === true || j.success === 'true') {
          status.className = 'form-status ok';
          status.textContent = '¡Gracias! Recibimos tu mensaje y te responderemos muy pronto.';
          status.style.display = 'block';
          form.reset();
          window.wmTrack('lead');
        } else {
          throw new Error('rejected');
        }
      })
      .catch(function () {
        status.className = 'form-status err';
        status.innerHTML = 'No pudimos enviar el mensaje. Escríbenos a '
          + '<a href="mailto:coaching@waymarkinc.com">coaching@waymarkinc.com</a> '
          + 'o llámanos al <a href="tel:14058228300">(405) 822-8300</a>.';
        status.style.display = 'block';
      })
      .then(function () {
        btn.disabled = false;
        btn.innerHTML = orig;
      });
  });
})();
