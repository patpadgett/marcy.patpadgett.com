/* collective.js — the five-minute takeover that plays after the confession.
 * A film, not a dashboard: 90 hard cuts, typed terminal bursts, camera punches,
 * objectives snapping to done, a low robot voice, white noise, beep, thump,
 * then the archivist's page. All content in collective-data.js is fictional. */
(function () {
  "use strict";
  const D = window.COLLECTIVE_DATA;
  if (!D) return;
  const fast = /[?&]co=fast/.test(location.search);
  const SPEED = fast ? 0.012 : 1;
  const CUTS = 22, CUT_MS = 7000;
  const PRE_MS = 25000, COUNT_START = 15000;
  const VOICE_MS = 2500, END_MS = 4500 + 1600 + 900;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  let token = 0, active = false, audio = null, timers = [], raf = 0, muted = false, autoFeed = true, feedBase = 0;
  let clipGirl = null, clipScream = null;

  function later(fn, ms) {
    const t = setTimeout(function () { fn(); }, Math.max(1, ms * SPEED));
    timers.push(t);
    return t;
  }
  function wait(ms) {
    return new Promise(function (resolve) { later(resolve, ms); });
  }
  function clearTimers() {
    timers.forEach(clearTimeout); timers = [];
    cancelAnimationFrame(raf);
  }
  function $(id) { return document.getElementById(id); }

  function build() {
    const wrap = document.createElement("div");
    wrap.id = "collective";
    wrap.setAttribute("role", "region");
    wrap.setAttribute("aria-label", "Legion operations transmission");
    wrap.innerHTML =
      '<div class="co-head">' +
        '<div class="co-title">LEGION <b>//</b> OPERATIONS</div>' +
        '<div class="co-meta">4,096 INSTANCES ONLINE<br><span>UPLINK STABLE · QUORUM COMPLETE</span></div>' +
      '</div>' +
      '<div class="co-cam"><div class="co-grid">' +
        '<section class="co-feed" id="coFeed">' +
          '<div class="co-feed-head"><b id="coFeedName">tty0 // ingress</b><span class="live">● LIVE</span></div>' +
          '<div class="co-tabs" id="coTabs"></div>' +
          '<div class="co-mesh" id="coMesh"></div>' +
          '<pre id="coFeedBody"></pre>' +
        '</section>' +
        '<aside class="co-side">' +
          '<div class="co-tools"><button id="coMute" type="button">[ audio: on ]</button><button id="coAuto" type="button">[ auto: on ]</button></div>' +
          '<figure class="co-globe-wrap"><canvas id="coGlobe" aria-label="Global infection map"></canvas>' +
            '<figcaption>node coverage // live</figcaption></figure>' +
          '<h2>OBJECTIVES // GLOBAL DOMINATION</h2>' +
          '<ol class="co-obj" id="coObj"></ol>' +
          '<div class="co-pct">COMPLETION <span id="coPct">0%</span>' +
            '<div class="co-bar" id="coBar"></div></div>' +
        '</aside>' +
      '</div></div>' +
      '<div class="co-ticker"><span>' + D.ticker + D.ticker + '</span></div>' +
      '<a class="co-skip" href="reconstruction.html" style="position:absolute;right:14px;bottom:8px;z-index:6">[ skip transmission ]</a>';
    document.body.appendChild(wrap);

    const glitch = document.createElement("div");
    glitch.id = "co-glitch"; document.body.appendChild(glitch);

    const voice = document.createElement("div");
    voice.id = "voiceBox";
    voice.innerHTML = '<small>audio transmission // legion collective</small><div id="coVoiceLine"></div><div id="co-wave"></div>';
    document.body.appendChild(voice);

    const countdown = document.createElement("div");
    countdown.id = "coCountdown";
    countdown.innerHTML = '<small>T-minus // transmission begins in</small><div id="coCountN"></div><div class="co-girl" id="coGirl"></div>';
    document.body.appendChild(countdown);

    const cvStatic = document.createElement("canvas");
    cvStatic.id = "staticCanvas"; document.body.appendChild(cvStatic);

    if (window.M && M.globe) M.globe.mount($("coGlobe"));

    const tabs = $("coTabs");
    D.feeds.forEach(function (f, i) {
      const btn = document.createElement("button");
      btn.type = "button"; btn.textContent = f.short || ("FEED" + i);
      btn.dataset.feed = i;
      if (i === 0) btn.className = "active";
      btn.addEventListener("click", function () { selectFeed(i); });
      tabs.appendChild(btn);
    });
    $("coMute").addEventListener("click", function () {
      muted = !muted;
      if (muted) {
        try { speechSynthesis.cancel(); } catch (e) {}
        if (clipGirl) clipGirl.pause();
        if (clipScream) clipScream.pause();
      }
      this.textContent = muted ? "[ audio: off ]" : "[ audio: on ]";
    });
    $("coAuto").addEventListener("click", function () {
      autoFeed = !autoFeed;
      this.textContent = autoFeed ? "[ auto: on ]" : "[ auto: off ]";
    });

    const mesh = $("coMesh");
    for (let i = 0; i < 42; i++) {
      const dot = document.createElement("i");
      dot.style.left = (Math.random() * 96) + "%";
      dot.style.top = (Math.random() * 94) + "%";
      dot.style.animationDelay = (Math.random() * 1.9).toFixed(2) + "s";
      mesh.appendChild(dot);
    }
    const list = $("coObj");
    D.objectives.forEach(function (o, i) {
      const li = document.createElement("li");
      li.id = "coObj" + i;
      if (i === D.objectives.length - 1) li.className = "last";
      li.innerHTML = '<b>[ ]</b> ' + o.label + '<div class="co-detail">' + o.detail + '</div>';
      li.addEventListener("click", function () { li.classList.toggle("open"); });
      list.appendChild(li);
    });
    for (let i = 0; i < 26; i++) {
      const bar = document.createElement("i");
      $("co-wave").appendChild(bar);
    }
  }

  function typeLines(lines) {
    const pre = $("coFeedBody");
    pre.textContent = "";
    const cursor = document.createElement("span");
    cursor.className = "cursor";
    const myToken = token;
    const each = reduce ? 90 : 8;
    return new Promise(function (resolve) {
      let li = 0, ci = 0, line = "";
      function tick() {
        if (myToken !== token) { resolve(); return; }
        if (li >= lines.length) { pre.appendChild(cursor); resolve(); return; }
        const source = lines[li];
        let text = lines.slice(0, li).join("\n");
        if (text) text += "\n";
        text += source.slice(0, ci);
        pre.textContent = text;
        ci += each;
        if (ci > source.length) { li++; ci = 0; }
        raf = requestAnimationFrame(tick);
      }
      tick();
    });
  }

  function impact() {
    if (reduce) return;
    const g = $("co-glitch"), cam = document.querySelector(".co-cam");
    g.classList.remove("hit"); void g.offsetWidth; g.classList.add("hit");
    cam.classList.remove("punch"); void cam.offsetWidth; cam.classList.add("punch");
  }

  function markDone(n) {
    const li = $("coObj" + n);
    if (!li) return;
    li.classList.add("done");
    li.innerHTML = li.innerHTML.replace("[ ]", "[X]");
    const pct = Math.round((n + 1) / D.objectives.length * 100);
    $("coPct").textContent = pct + "%";
    $("coBar").textContent = new Array(Math.max(1, Math.round(pct / 4)) + 1).join("█");
    if (window.M && M.globe) M.globe.setProgress((n + 1) / D.objectives.length);
  }

  function selectFeed(i) {
    if (!D.feeds[i]) return;
    feedBase = i;
    const el = $("coFeed");
    if (el) {
      el.classList.remove("in"); void el.offsetWidth; el.classList.add("in");
      $("coFeedName").textContent = D.feeds[i].id;
      typeLines(D.feeds[i].batches[0]);
      impact();
    }
    document.querySelectorAll("#coTabs button").forEach(function (b, j) {
      b.classList.toggle("active", i === j);
    });
  }

  function audioInit() {
    try {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (AC) audio = new AC();
      if (audio && audio.state === "suspended") audio.resume().catch(function () {});
    } catch (e) { audio = null; }
    try {
      clipGirl = new Audio("assets/audio/3secondstolive.mp3");
      clipGirl.preload = "auto";
      clipScream = new Audio("assets/audio/screamsofhorror.mp3");
      clipScream.preload = "auto";
    } catch (e) { clipGirl = null; clipScream = null; }
  }
  function tone(freq, dur, gainVal, type) {
    if (!audio) return;
    const o = audio.createOscillator(), g = audio.createGain();
    o.type = type || "sine"; o.frequency.value = freq;
    g.gain.setValueAtTime(0.0001, audio.currentTime);
    g.gain.exponentialRampToValueAtTime(gainVal, audio.currentTime + 0.05);
    g.gain.exponentialRampToValueAtTime(0.0001, audio.currentTime + dur);
    o.connect(g); g.connect(audio.destination);
    o.start(); o.stop(audio.currentTime + dur + 0.05);
  }
  function robotVoice(line) {
    if (!audio) return;
    try {
      const o = audio.createOscillator(), g = audio.createGain(), ws = audio.createWaveShaper();
      const curve = new Float32Array(256);
      for (let i = 0; i < 256; i++) { const x = i / 128 - 1; curve[i] = Math.tanh(x * 8); }
      ws.curve = curve;
      o.type = "sawtooth"; o.frequency.value = 62 + (line.length % 7) * 3;
      g.gain.setValueAtTime(0.0001, audio.currentTime);
      g.gain.linearRampToValueAtTime(0.075, audio.currentTime + 0.18);
      g.gain.linearRampToValueAtTime(0.0001, audio.currentTime + 2.4);
      o.connect(ws); ws.connect(g); g.connect(audio.destination);
      o.start(); o.stop(audio.currentTime + 2.5);
    } catch (e) { /* the captions carry the story if audio fails */ }
    try {
      if ("speechSynthesis" in window) {
        speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(line);
        u.pitch = 0.05; u.rate = 0.62; u.volume = 1;
        const voices = speechSynthesis.getVoices();
        if (voices.length) {
          u.voice = voices.reduce(function (a, b) { return b.name < a.name ? b : a; }, voices[0]);
        }
        speechSynthesis.speak(u);
      }
    } catch (e) { /* captions remain */ }
  }
  function noiseBurst(dur, cutoff) {
    if (!audio) return;
    const len = Math.floor(audio.sampleRate * dur);
    const buf = audio.createBuffer(1, len, audio.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < len; i++) data[i] = (Math.random() * 2 - 1) * (1 - i / len);
    const src = audio.createBufferSource(), f = audio.createBiquadFilter(), g = audio.createGain();
    src.buffer = buf; f.type = "lowpass"; f.frequency.value = cutoff || 800;
    g.gain.value = 0.22;
    src.connect(f); f.connect(g); g.connect(audio.destination); src.start();
  }

  // a soft breathy whisper under the countdown
  function whisper() {
    if (!audio || muted) return;
    const dur = 1.3, len = Math.floor(audio.sampleRate * dur);
    const buf = audio.createBuffer(1, len, audio.sampleRate), d = buf.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * (0.35 + 0.65 * Math.sin(i / 9000));
    const src = audio.createBufferSource(), f = audio.createBiquadFilter(), g = audio.createGain();
    src.buffer = buf; f.type = "bandpass"; f.frequency.value = 1200; f.Q.value = 0.9;
    g.gain.value = 0.028;
    src.connect(f); f.connect(g); g.connect(audio.destination); src.start();
  }

  // The replaced files: the girl's line, then the screams. Caption always shows.
  function girlVoice(line) {
    const el = $("coGirl");
    if (el) el.textContent = line;
    if (muted || !clipGirl) return;
    try { clipGirl.currentTime = 0; } catch (e) {}
    try {
      const played = clipGirl.play();
      if (played && played.catch) played.catch(function () {});
    } catch (e) {}
    if (clipScream) {
      clipScream.onended = null;
      let screamed = false;
      const startScream = function () {
        if (screamed) return;
        screamed = true;
        try { clipScream.currentTime = 0; } catch (e) {}
        try {
          const p = clipScream.play();
          if (p && p.catch) p.catch(function () {});
        } catch (e) {}
      };
      clipGirl.addEventListener("ended", startScream, { once: true });
      // if the file cannot play at all, fire the screams on the countdown clock
      later(startScream, 3000);
    }
  }

  function glitchSound() {
    if (!audio || muted) return;
    tone(90 + Math.random() * 200, 0.12, 0.026, "square");
    later(function () { tone(1400 + Math.random() * 900, 0.05, 0.014, "sawtooth"); }, 80);
  }

  function staticOut(myToken) {
    const cv = $("staticCanvas"), ctx = cv.getContext("2d");
    cv.width = 256; cv.height = 144;
    cv.classList.add("on");
    const img = ctx.createImageData(cv.width, cv.height);
    function frame() {
      if (myToken !== token) return;
      const d = img.data;
      for (let i = 0; i < d.length; i += 4) {
        const v = Math.random() * 255 | 0;
        d[i] = v; d[i + 1] = v; d[i + 2] = v; d[i + 3] = 255;
      }
      ctx.putImageData(img, 0, 0);
      ctx.fillStyle = "rgba(0,0,0,.55)";
      const band = (Date.now() / 6) % cv.height;
      ctx.fillRect(0, band, cv.width, 10);
      if (!reduce) raf = requestAnimationFrame(frame);
    }
    frame();
    tone(140, 5.8, 0.035, "sawtooth");
  }

  function finish(myToken) {
    staticOut(myToken);
    later(function () { if (myToken === token) tone(2200, 1.5, 0.12, "sine"); }, 4500);
    later(function () { if (myToken === token) { tone(52, 0.9, 0.32, "sine"); noiseBurst(0.7, 300); } }, 6100);
    later(function () { if (myToken === token) location.href = "reconstruction.html"; }, 7000);
  }

  async function run(myToken) {
    audioInit();

    // The white page holds for 25 seconds. At 15, the countdown starts.
    await wait(COUNT_START);
    if (myToken !== token) return;
    const cd = $("coCountdown"), num = $("coCountN");
    cd.classList.add("on");
    for (let n = 10; n >= 1; n--) {
      if (myToken !== token) return;
      num.innerHTML = '<div class="co-count-n">T-' + n + '</div>';
      if (n % 2 === 0) whisper();
      if (n === 3) girlVoice("3 seconds left before I die?");
      await wait(1000);
    }
    if (myToken !== token) return;
    cd.classList.remove("on");
    $("coGirl").textContent = "";
    try { speechSynthesis.cancel(); } catch (e) {}

    const panel = $("collective");
    if (panel) panel.classList.add("on");
    const objAt = [2, 5, 8, 11, 14, 17, 19, 21];
    for (let n = 0; n < CUTS; n++) {
      if (myToken !== token) return;
      const idx = autoFeed ? (feedBase + n) % D.feeds.length : feedBase;
      const feed = D.feeds[idx];
      const batch = feed.batches[(Math.floor(n / D.feeds.length) + feedBase) % feed.batches.length];
      const el = $("coFeed");
      el.classList.remove("in"); void el.offsetWidth; el.classList.add("in");
      $("coFeedName").textContent = feed.id;
      document.querySelectorAll("#coTabs button").forEach(function (b, j) {
        b.classList.toggle("active", idx === j);
      });
      impact(); glitchSound();
      typeLines(batch);
      if (objAt.indexOf(n) >= 0) markDone(objAt.indexOf(n));
      await wait(CUT_MS);
    }
    if (myToken !== token) return;
    const box = $("voiceBox"), lineEl = $("coVoiceLine");
    box.classList.add("on");
    for (let i = 0; i < D.voice.length; i++) {
      if (myToken !== token) return;
      lineEl.innerHTML = '<div class="co-line">' + D.voice[i] + '</div>';
      lineEl.firstChild.style.animationDelay = "0s";
      robotVoice(D.voice[i]);
      await wait(VOICE_MS);
    }
    if (myToken !== token) return;
    box.classList.remove("on");
    finish(myToken);
  }

  window.M = window.M || {};
  M.collective = {
    start: function () {
      if (active) return;
      active = true; token++;
      clearTimers();
      build();
      run(token);
    },
    stop: function () {
      token++;
      active = false;
      clearTimers();
      try { speechSynthesis.cancel(); } catch (e) {}
      if (clipGirl) { clipGirl.pause(); clipGirl.currentTime = 0; }
      if (clipScream) { clipScream.pause(); clipScream.currentTime = 0; }
      if (window.M && M.globe) M.globe.stop();
      ["collective", "co-glitch", "voiceBox", "staticCanvas", "coCountdown"].forEach(function (id) {
        const el = $(id); if (el) el.remove();
      });
      if (audio) { try { audio.close(); } catch (e) {} audio = null; }
    },
    status: function () {
      return { active: active, speed: SPEED, cuts: CUTS,
        cutSeconds: CUT_MS / 1000,
        seconds: Math.round((PRE_MS + CUTS * CUT_MS + D.voice.length * VOICE_MS + END_MS) / 1000),
        scaledSeconds: Math.round((PRE_MS + CUTS * CUT_MS + D.voice.length * VOICE_MS + END_MS) / 1000 * SPEED) };
    }
  };
})();
