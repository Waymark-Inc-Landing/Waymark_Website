/* Landing-page behaviour: the contact form, and the three conversions worth counting. */
(function () {
  var form = document.getElementById('lpForm');

  // A tapped phone number and a click through to booking are both real intent.
  // A tapped number and a WhatsApp message are both someone reaching out.
  // Phone and WhatsApp are different channels and were sharing one label, so a
  // zero on each was the same zero counted twice. They report separately now.
  document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
    a.addEventListener('click', function () { window.wmTrack('call'); });
  });
  document.querySelectorAll('a[href*="wa.me"]').forEach(function (a) {
    a.addEventListener('click', function () { window.wmTrack('whatsapp'); });
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

    // The inquiry goes two ways at once: to the Waymark platform, which records the
    // lead and emails us, and to the mail service. Either one arriving is a success,
    // so the visitor is not left waiting on whichever is slow or down.
    var settled = false, pending = 2, timer = null;
    function finish(ok) {
      if (settled) { return; }
      if (ok) {
        status.className = 'form-status ok';
        status.textContent = '¡Gracias! Recibimos tu mensaje y te responderemos muy pronto.';
        form.reset();
        window.wmTrack('lead');
      } else if (--pending > 0) {
        return;
      } else {
        status.className = 'form-status err';
        status.innerHTML = 'No pudimos enviar el mensaje. Escríbenos a '
          + '<a href="mailto:coaching@waymarkinc.com">coaching@waymarkinc.com</a> '
          + 'o llámanos al <a href="tel:14058228300">(405) 822-8300</a>.';
      }
      settled = true;
      status.style.display = 'block';
      if (timer) { clearTimeout(timer); }
      btn.disabled = false;
      btn.innerHTML = orig;
    }

    // Both get 15 seconds, then the visitor sees the email address and phone number.
    var ctl = window.AbortController ? new AbortController() : null;
    timer = ctl ? setTimeout(function () { ctl.abort(); }, 15000) : null;
    var signal = ctl ? ctl.signal : undefined;

    try {
      var lead = new URLSearchParams();
      ['name', 'email', 'phone', 'service', 'message', '_honey'].forEach(function (k) {
        lead.append(k, payload[k] || '');
      });
      // form-urlencoded, so there is no CORS preflight to wait on.
      fetch('https://waymarkcoach.com/wp-json/lms/v1/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: lead.toString(),
        signal: signal
      }).then(function (r) { finish(r.ok); }).catch(function () { finish(false); });
    } catch (err) { finish(false); }

    fetch('https://formsubmit.co/ajax/coaching@waymarkinc.com', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(payload),
      signal: signal
    })
      .then(function (r) { return r.json(); })
      .then(function (j) { finish(j.success === true || j.success === 'true'); })
      .catch(function () { finish(false); });
  });
})();
