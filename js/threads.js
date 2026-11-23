/* threads.js — the seven threads. Nothing is destroyed. Every thread is a way
 * of finding something the page was trying not to say. */
window.M = window.M || {};
(function () {
  "use strict";

  // ---------------------------------------------------------------- guestbook
  const seedEntries = [
    ["jess", "03/14/99", "your page is so cool!!!! i put it on my favorites"],
    ["kayla", "03/15/99", "i liked the part about the piano :)"],
    ["mom", "03/16/99", "please eat something and do your homework"],
    ["danny", "03/18/99", "ur annoying but this page is ok"],
    ["a friend", "04/02/99", "what happened to the 4th picture??"],
    ["someone", "04/07/99", "why does your counter go backwards?"],
    ["me", "04/09/27", "i'm almost done. please don't close the window."]
  ];

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function renderBook() {
    const book = document.getElementById("guestList");
    if (!book) return;
    book.innerHTML = seedEntries.map(function (e) {
      return '<div style="border-bottom:1px dotted #999;padding:5px 0;">' +
        '<font size="2" color="#003366"><b>' + esc(e[0]) + '</b> <i>' + e[1] + '</i></font><br>' +
        '<font size="2">' + esc(e[2]) + '</font></div>';
    }).join("") +
    '<div id="gbookGhost" style="border:1px dashed #003366;padding:6px;margin:6px 0;display:none;">' +
      '<font size="2" color="#003366"><b>04/09/27</b></font><br>' +
      '<font size="2"><span id="gbookGhostText"></span></font>' +
    '</div>';
  }

  M.threads = {
    guest: {
      submit(ev) {
        ev.preventDefault();
        const f = ev.target;
        const name = (f.elements.name.value || "").trim() || "anonymous";
        const msg = (f.elements.comment.value || "").trim() || "(no comment)";
        const book = document.getElementById("guestList");
        const ent = document.createElement("div");
        ent.style.cssText = "border-bottom:1px dotted #999;padding:5px 0;";
        ent.innerHTML = '<font size="2" color="#003366"><b>' + esc(name) + '</b> <i>today</i></font><br>' +
                        '<font size="2">' + esc(msg) + '</font>';
        book.insertBefore(ent, book.firstChild);
        f.reset();
        M.decay.record();
        flash("your entry was written down. thank you for coming.");
      }
    },

    pix: {
      view(ev) {
        ev.preventDefault();
        M.decay.record();
        flash("the pictures are fine. it's the captions i can't keep straight.");
      }
    },

    quiz: {
      submit(ev) {
        ev.preventDefault();
        const f = ev.target;
        const picked = f.querySelector('input[name="quiz"]:checked');
        if (!picked) { flash("you have to pick one. i'm not going to pick for you."); return; }
        const r = document.getElementById("quizResult");
        if (picked.value === "machine" || picked.value === "code") {
          r.innerHTML = '<font size="2" color="#cc0000"><b>that was not one of the options i gave you.</b></font>';
        } else {
          r.innerHTML = '<font size="2" color="#003366"><b>correct!!!</b> that is what i would have picked too.</font>';
        }
        M.decay.record();
        M.decay.inner("quizMsg", M.decay.escape(M.decay.textAt("quizMsg", M.decay.LEVEL)));
        flash("the quiz keeps its own answers. you just supplied one.");
      }
    },

    counter: {
      number() { return M.decay.atStage(2) ? "020471" : "001999"; },
      update() {
        const future = M.decay.atStage(2);
        const src = future ? "assets/img/counter_2041.gif" : "assets/img/counter_1999.gif";
        ["counterImg", "counterImg2"].forEach(function (id) {
          const img = document.getElementById(id);
          if (img && img.src.indexOf(src) < 0) img.src = src;
        });
        ["counterNum", "counterNum2"].forEach(function (id) {
          const el = document.getElementById(id);
          if (el) el.textContent = M.threads.counter.number();
        });
      }
    },

    ring: {
      n: 47,
      next(ev) {
        ev.preventDefault();
        M.threads.ring.n = M.threads.ring.n >= 49 ? 47 : M.threads.ring.n + 1;
        M.decay.record();
        flash(M.threads.ring.n === 49
          ? "node 49 is not a page. it is a space where a page was supposed to be."
          : "this is just a page. keep going.");
      },
      prev(ev) {
        ev.preventDefault();
        M.threads.ring.n = Math.max(47, M.threads.ring.n - 1);
        M.decay.record();
        flash("back to node " + M.threads.ring.n + ".");
      },
      update() { }
    }
  };

  let toast;
  function flash(msg) {
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "toast";
      toast.style.cssText = "position:fixed;left:50%;bottom:22px;transform:translateX(-50%);" +
        "background:#000040;color:#fff;border:2px solid #ffcc00;padding:8px 14px;" +
        "font:12px Arial,sans-serif;z-index:99;max-width:80vw;text-align:center;";
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.style.display = "block";
    clearTimeout(flash.t);
    flash.t = setTimeout(function () { toast.style.display = "none"; }, 4200);
  }

  renderBook();
})();
