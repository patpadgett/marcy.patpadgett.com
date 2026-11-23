/* app.js — wires the restore mechanism and the initial render. */
(function () {
  "use strict";

  // the counter image and its number are both owned by M.threads.counter.update()
  // restore: after stage three the page offers to put itself back.
  const link = document.getElementById("restoreLink");
  const form = document.getElementById("unlockForm");
  if (link) {
    link.addEventListener("click", function (ev) {
      ev.preventDefault();
      if (form) form.style.display = form.style.display === "block" ? "none" : "block";
    });
  }
  if (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      const input = document.getElementById("unlock");
      if (input.value.trim().toLowerCase() === "northvale") {
        M.decay.reset();
        input.value = "";
        form.style.display = "none";
        if (link) link.style.display = "none";
      } else {
        input.value = "";
        input.placeholder = "the page said something about a place...";
      }
    });
  }

  // the counter starts at 1999; the page changes it as the truth surfaces.
  M.threads.counter.update();
  M.decay.render();
})();
