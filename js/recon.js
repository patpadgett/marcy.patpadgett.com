/* M4RCY — a reconstruction in five exposures
   Scroll drives the gate: which plate is loaded into it, what the counter reads,
   and how far the exposure has travelled. Text reveals itself once, on entry. */
(function () {
  'use strict';

  var doc = document.documentElement;
  var gate = document.querySelector('.gate');
  if (!gate) return;

  var plates = Array.prototype.slice.call(document.querySelectorAll('.plate'));
  var cols = Array.prototype.slice.call(document.querySelectorAll('.col'));
  var sections = Array.prototype.slice.call(document.querySelectorAll('[data-act]'));
  var hudAct = document.getElementById('hudAct');
  var hudTC = document.getElementById('hudTC');
  var hudWord = document.getElementById('hudWord');
  var railFill = document.querySelector('.rail i');

  var WORDS = ['1999 \u00b7 node 47', 'the record', 'the machine', 'the night', 'the object', '04% recovered'];
  var TOTAL_TC = 4 * 3600 + 12 * 60; /* 04:12:00 of recovered material */
  var current = -1;
  var ticking = false;

  /* reveal once, then forget the observer: nothing re-animates on the way back up */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: '-12% 0px -18% 0px', threshold: 0.15 });
    sections.forEach(function (s) { io.observe(s); });
  } else {
    sections.forEach(function (s) { s.classList.add('in'); });
  }

  function timecode(progress) {
    var t = Math.max(0, Math.min(1, progress)) * TOTAL_TC;
    var h = Math.floor(t / 3600);
    var m = Math.floor((t % 3600) / 60);
    var s = Math.floor(t % 60);
    var f = Math.floor((t * 24) % 24);
    var p = function (n) { return (n < 10 ? '0' : '') + n; };
    return p(h) + ':' + p(m) + ':' + p(s) + ':' + p(f);
  }

  function setAct(i) {
    if (i === current) return;
    current = i;
    plates.forEach(function (p, n) {
      p.classList.toggle('is-on', n === Math.min(i, plates.length - 1));
    });
    if (hudAct) hudAct.textContent = ('0' + Math.min(i + 1, 5)).slice(-2);
    if (hudWord) hudWord.textContent = WORDS[Math.min(i, WORDS.length - 1)] || 'scroll';
    document.body.setAttribute('data-act', String(i));
  }

  function frame() {
    ticking = false;
    var vh = window.innerHeight;
    var y = window.scrollY || doc.scrollTop;
    var max = Math.max(1, doc.scrollHeight - vh);
    var progress = Math.min(1, y / max);

    /* which exposure is in the gate: the section whose middle is nearest the fold */
    var best = 0, bestD = Infinity;
    for (var i = 0; i < sections.length; i++) {
      var r = sections[i].getBoundingClientRect();
      var mid = r.top + r.height * 0.42;
      var d = Math.abs(mid - vh * 0.52);
      if (d < bestD) { bestD = d; best = i; }
    }
    setAct(best);

    /* the plate drifts against the scroll: a slow parallax inside the gate */
    for (var j = 0; j < plates.length; j++) {
      var pr = plates[j].getBoundingClientRect();
      var local = (vh * 0.5 - (pr.top + pr.height * 0.5)) / vh;
      plates[j].style.setProperty('--py', (local * 26).toFixed(2) + 'px');
    }

    /* one voice at a time: a column fades out once the eye has left it */
    for (var c = 0; c < cols.length; c++) {
      var cr = cols[c].getBoundingClientRect();
      var eye = vh * 0.52;
      var o = 1;
      if (eye < cr.top) o = 1 - (cr.top - eye) / (vh * 0.42);
      else if (eye > cr.bottom) o = 1 - (eye - cr.bottom) / (vh * 0.42);
      o = Math.max(0, Math.min(1, o));
      cols[c].style.opacity = o.toFixed(3);
      cols[c].style.transform = 'translate3d(0,' + ((1 - o) * (eye < cr.top ? 18 : -18)).toFixed(1) + 'px,0)';
    }

    if (railFill) railFill.style.transform = 'scaleY(' + progress.toFixed(4) + ')';
    if (hudTC) hudTC.textContent = timecode(progress);

    /* the first screen has no scroll yet; mark it live immediately */
    if (y < 8) sections[0].classList.add('in');
  }

  function onScroll() {
    if (!ticking) { ticking = true; requestAnimationFrame(frame); }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  frame();
  setTimeout(frame, 60);
  setTimeout(frame, 400);
})();
