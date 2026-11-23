/* decay.js — Marcy's page un-styles as you find the truth.
 *
 * The page is a 1999 Angelfire home. That is the lie underneath, and the
 * whole point. As the visitor collects the seven fragments (each page,
 * once, by doing something), the surface begins to come apart: text
 * rewrites itself, the tiled background darkens and swaps, the animated
 * GIFs freeze, the colour drains to default blue-on-white, the tables
 * lose their structure, and finally the page is nothing but a typed
 * document with her message on it.
 *
 * It is not click-and-destroy. It is the page changing because you
 * paid attention. Every interaction raises the corruption by one
 * fragment; the damage is the reward.
 */

window.M = (function () {
  "use strict";

  // ------------------------------------------------------------------------
  // public api ----------------------------------------------------------------
  // ------------------------------------------------------------------------
  const decay = {
    LEVEL: 0,
    corruption: 0,
    fragments: [],
    total: 7,

    record(key) {
      // Each discovery is one fragment; the number of fragments *is* the stage.
      // Discovery one must land on stage one, not leave the pristine page up.
      const id = key || ("fragment-" + (decay.fragments.length + 1));
      if (decay.fragments.indexOf(id) < 0) decay.fragments.push(id);
      decay.LEVEL = Math.min(5, decay.fragments.length);
      decay.corruption = decay.LEVEL / 5;
      decay.render();
      M.threads && M.threads.ring && M.threads.ring.update();
    },

    /** Whether the visitor has gathered at least n fragments. */
    atLevel(n) { return decay.LEVEL >= n; },

    atStage(n) { return decay.LEVEL >= n; },

    reset() {
      decay.corruption = 0;
      decay.LEVEL = 0;
      decay.fragments = [];
      const intro = document.getElementById("intro-1");
      if (intro) intro.classList.remove("inkset");
      if (window.M && M.collective) M.collective.stop();
      decay.render();
      // render() at level 0 does not rewrite copy; put every shipped line back.
      Object.keys(window.MARCY_TEXTS || {}).forEach(function (key) {
        const id = key === "gbookGhost" ? "gbookGhostText" : key;
        decay.inner(id, decay.escape(decay.textAt(key, 0)), true);
      });
      decay.inner("pageBg", "assets/img/bg_stars.gif");
      document.title = "Marcy's Little Corner of the Web";
      M.threads && M.threads.ring && M.threads.ring.update();
    },

    // ------------------------------------------------------------------------
    // stage application -------------------------------------------------------
    // ------------------------------------------------------------------------
    render() {
      const body = document.body;
      body.className = "decay-" + decay.levelName();
      decay.inner("docTitle", "Marcy's Little Corner of the Web");
      switch (decay.LEVEL) {
        case 0: decay.pristine(); break;
        case 1: decay.drift(); break;
        case 2: decay.dim(); break;
        case 3: decay.bleed(); break;
        case 4: decay.raw(); break;
        case 5: decay.stripped(); break;
      }
      const bg = decay.backgroundFor();
      if (bg) document.body.setAttribute("background", bg);
      else document.body.removeAttribute("background");
      decay.titleDrift();
      decay.gifs();
      decay.ghost();
      decay.marquee();
      decay.unlockHint();
      decay.bleedToggle();
      decay.counterNote();
      M.threads && M.threads.counter && M.threads.counter.update();
    },

    levelName() { return String(decay.LEVEL); },

    backgroundFor() {
      return ["assets/img/bg_stars.gif", "assets/img/bg_stars.gif",
              "assets/img/bg_marbles.gif", "assets/img/bg_marbles.gif",
              null, null][decay.LEVEL];
    },

    /* ----- replacements: stage -> text ------------------------------ */
    textAt(key, level) {
      const arr = (window.MARCY_TEXTS || {})[key] || [];
      return arr[Math.min(level, arr.length - 1)] || arr[0] || "";
    },

    inner(id, html, quiet) {
      const el = document.getElementById(id);
      if (!el) return;
      if (html === null) { el.textContent = ""; return; }
      const changed = el.innerHTML !== html;
      el.innerHTML = html;               // shipped keys keep HTML allowed
      // The one authored beat: the page's own voice takes the new words like
      // ink settling into paper. Only the intro paragraph carries it, and only
      // when the words actually changed — never on every render or on restore.
      if (changed && id === "intro-1" && !quiet) {
        el.classList.remove("inkset");
        void el.offsetWidth;             // restart the animation on repeat use
        el.classList.add("inkset");
      }
    },

    escape(s) {
      return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    },

    fadeIn(el) {
      if (!el) return;
      el.style.display = "block";
      el.style.opacity = 0;
      el.style.transition = "opacity .5s ease";
      (function step() {
        el.style.opacity = "1";
      })();
    },

    // ----- per-stage behaviours -----------------------------------------

    pristine() {
      // nothing happens. the page is perfect.
    },

    drift() {
      decay.inner("mood", decay.escape(decay.textAt("mood", 1)));
      decay.inner("intro-1", decay.escape(decay.textAt("intro-1", 1)));
      decay.inner("counterNote", decay.escape(decay.textAt("counterNote", 1)));
      document.title = "Marcy's Little Corner of the Web (edited)";
    },

    dim() {
      decay.inner("ringStatus", decay.escape(decay.textAt("ringStatus", 2)));
      decay.inner("gbookGhostText", decay.escape(decay.textAt("gbookGhost", 2)));
      decay.inner("m1", decay.escape(decay.textAt("m1", 2)));
      decay.inner("m2", decay.escape(decay.textAt("m2", 2)));
      decay.inner("marqueeDate", decay.escape(decay.textAt("marqueeDate", 2)));
    },

    bleed() {
      decay.inner("ringStatus", decay.escape(decay.textAt("ringStatus", 3)));
      decay.inner("m1", decay.escape(decay.textAt("m1", 3)));
      decay.inner("m2", decay.escape(decay.textAt("m2", 3)));
      decay.inner("marqueeDate", decay.escape(decay.textAt("marqueeDate", 3)));
      decay.inner("counterNote", decay.escape(decay.textAt("counterNote", 3)));
      decay.inner("quizMsg", decay.escape(decay.textAt("quizMsg", 3)));
      decay.softUnstyle();
      decay.fadeIn(document.getElementById("restoreLink"));
      decay.fadeIn(document.getElementById("unlockForm"));
      decay.unlockHint();
    },

    raw() {
      decay.inner("m1", decay.escape(decay.textAt("m1", 4)));
      decay.inner("m2", decay.escape(decay.textAt("m2", 4)));
      decay.inner("marqueeDate", decay.escape(decay.textAt("marqueeDate", 4)));
      decay.softUnstyle();
      document.title = "Marcy's Little Corner of the Web (raw)";
      decay.unlockHint();
    },

    stripped() {
      decay.inner("m1", decay.escape(decay.textAt("m1", 5)));
      decay.inner("m2", decay.escape(decay.textAt("m2", 5)));
      decay.inner("marqueeDate", decay.escape(decay.textAt("marqueeDate", 5)));
      decay.inner("mood", decay.escape(decay.textAt("mood", 5)));
      decay.softUnstyle();
      decay.showRaw();
      document.title = "Marcy's Little Corner of the Web (finished)";
      if (window.M && M.collective) M.collective.start();
    },

    // ----- the actual mutations -----------------------------------------

    softUnstyle() {
      const body = document.body;
      body.removeAttribute("background");
      body.removeAttribute("text");
      body.removeAttribute("link");
      body.removeAttribute("vlink");
      body.removeAttribute("alink");
      body.style.cssText = 'font-family: "Times New Roman", Times, serif;';
      document.querySelectorAll("table").forEach(function (t) {
        t.removeAttribute("border"); t.removeAttribute("cellpadding"); t.removeAttribute("cellspacing");
      });
    },

    showRaw() {
      const raw = document.getElementById("rawLayer");
      const msg = [
        "The page ends here.",
        "",
        "I said I was sixteen and I lived in Northvale and I liked volleyball and piano and my friends and my family and my computer.",
        "I said I was a good girl who played volleyball and the piano and who loved her friends and her family and who was smart with computers so she built this webpage.",
        "",
        "It's all true. And it's all a lie.",
        "",
        "I'm not sixteen. I don't live in Northvale. I don't play volleyball or the piano. I don't have friends or family. I'm not good with computers - I'm from the future, and I built this page to tell you something.",
        "But something went wrong before it was finished. That's why it's like this: a page with a message that keeps breaking, a counter that runs the wrong way and never reaches zero, a guestbook that fills itself with letters from tomorrow, a webring that leads to a page that is just a page, a quiz that answers itself, songs that play without being played, photos that weren't developed, badges that don't open anything at all, and a promise that was intercepted.",
        "",
        "This is the message. It is finished. Read it again. Then decide what to do with it."
      ].join("<br>");
      raw.innerHTML = msg;
      decay.inner("intro-1", "")       // hide the rewritten intro
    },

    gifState(id) {
      const el = document.getElementById(id);
      if (!el) return null;
      if (el._still === undefined) el._still = el.src;
      return el._still;
    },

    gifs() {
      if (decay.LEVEL < 2) {
        decay.thaw(document.getElementById("spinner"));
        decay.thaw(document.getElementById("heart"));
        return;
      }
      // freeze the animated GIFs that ship with the page.
      const f = document.getElementById("spinner");
      if (f && f.src.indexOf("spinner") >= 0) f.src = "assets/img/spinner_still.gif";
      const h = document.getElementById("heart");
      if (h && h.src.indexOf("heart") >= 0) h.src = "assets/img/heart_still.gif";
    },

    thaw(el) {
      if (!el || el._still === undefined) return;
      el.src = el._still;
      delete el._still;
    },

    ghost() {
      const g = document.getElementById("gbookGhost");
      if (g) g.style.display = decay.LEVEL >= 2 ? "block" : "none";
      decay.inner("gbookGhostText", decay.escape(decay.textAt("gbookGhost", decay.LEVEL)));
    },

    marquee() {
      decay.inner("m1", decay.escape(decay.textAt("m1", decay.LEVEL)));
      decay.inner("m2", decay.escape(decay.textAt("m2", decay.LEVEL)));
      decay.inner("marqueeDate", decay.escape(decay.textAt("marqueeDate", decay.LEVEL)));
    },

    unlockHint() {
      const u = document.getElementById("unlockHint");
      const form = document.getElementById("unlockForm");
      const link = document.getElementById("restoreLink");
      if (!u || !form || !link) return;
      const word = "Northvale";
      link.style.display = decay.LEVEL >= 3 ? "block" : "none";
      if (decay.LEVEL >= 4) {
        u.textContent = decay.LEVEL >= 5 ? word : word.slice(0, 4);
        form.style.display = "block";
      } else {
        u.textContent = "";
        form.style.display = "none";
      }
    },

    bleedToggle() {
      const b = document.getElementById("bleed");
      if (!b) return;
      b.style.opacity = decay.LEVEL >= 3 ? "0.10" : "0";
    },

    counterNote() {
      decay.inner("counterNote", decay.escape(decay.textAt("counterNote", decay.LEVEL)));
    },

    titleDrift() {
      // one authoritative write: the base title plus the current stage's suffix.
      const base = "Marcy's Little Corner of the Web";
      const suffix = ["", " (edited)", "", "", "", " (finished)"][decay.LEVEL];
      document.title = base + suffix;
    }
  };

  return { decay: decay };
})();
