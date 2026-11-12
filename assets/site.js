(function () {
  // Mobiles Menü schließen, wenn ein Link darin angeklickt wird
  document.querySelectorAll('.gnav-sheet a').forEach(function (a) {
    a.addEventListener('click', function () { var d = a.closest('details'); if (d) d.open = false; });
  });

  // Sanftes Einblenden beim Scrollen. Ohne JS oder bei „Bewegung reduzieren“ bleibt alles sofort sichtbar.
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Videos: nur abspielen, solange sie sichtbar sind. Bei „Bewegung reduzieren“ kein Autostart, dafür Bedienelemente.
  var videos = document.querySelectorAll('video[data-auto]');
  if (reduce || !('IntersectionObserver' in window)) {
    videos.forEach(function (v) { v.controls = true; });
    return;
  }
  var vio = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { var p = en.target.play(); if (p && p.catch) p.catch(function () { en.target.controls = true; }); }
      else en.target.pause();
    });
  }, { threshold: 0.35 });
  videos.forEach(function (v) { vio.observe(v); });

  document.documentElement.classList.add('js');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
})();
