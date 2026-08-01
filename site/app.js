// Catalog search/filter + copy-to-clipboard. No dependencies.

(function () {
  var q = document.getElementById('q');
  var cards = [].slice.call(document.querySelectorAll('.card'));
  var chips = [].slice.call(document.querySelectorAll('.chip'));
  var empty = document.querySelector('.empty');
  var cat = 'all';

  function apply() {
    var term = (q && q.value || '').trim().toLowerCase();
    var words = term ? term.split(/\s+/) : [];
    var shown = 0;

    cards.forEach(function (card) {
      var hay = card.dataset.search;
      var ok =
        (cat === 'all' || card.dataset.cat === cat) &&
        words.every(function (w) { return hay.indexOf(w) !== -1; });
      card.hidden = !ok;
      if (ok) shown++;
    });

    if (empty) empty.hidden = shown !== 0;
  }

  if (q) {
    q.addEventListener('input', apply);
    // "/" focuses search, Escape clears it.
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && document.activeElement !== q) {
        e.preventDefault();
        q.focus();
      } else if (e.key === 'Escape' && document.activeElement === q) {
        q.value = '';
        apply();
        q.blur();
      }
    });
  }

  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      chips.forEach(function (c) { c.classList.remove('active'); });
      chip.classList.add('active');
      cat = chip.dataset.cat;
      apply();
    });
  });

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.copy');
    if (!btn) return;
    e.preventDefault();
    var text = btn.dataset.copy;
    var done = function () {
      var label = btn.textContent;
      btn.textContent = 'Copied';
      btn.classList.add('done');
      setTimeout(function () {
        btn.textContent = label;
        btn.classList.remove('done');
      }, 1600);
    };

    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else {
      fallback();
    }

    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); done(); } catch (err) { /* no-op */ }
      document.body.removeChild(ta);
    }
  });
})();
