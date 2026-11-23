/* collective-globe.js — an orthographic Earth that turns red as the
 * collective takes over. Cities light up in population order: the biggest
 * first, the smallest last. At 100% the whole globe is red. */
(function () {
  "use strict";
  const C = [
    [28.6, 77.2, 32], [35.7, 139.7, 37], [40.7, -74.0, 19], [51.5, -0.13, 9],
    [48.9, 2.35, 11], [52.5, 13.4, 4], [55.8, 37.6, 13], [19.4, -99.1, 22],
    [-23.5, -46.6, 22], [6.5, 3.4, 15], [30.0, 31.2, 21], [31.2, 121.5, 29],
    [37.6, 127.0, 17], [1.35, 103.8, 6], [13.8, 100.5, 11], [14.6, 121.0, 14],
    [-6.2, 106.8, 27], [19.1, 72.9, 20], [12.97, 77.6, 13], [23.8, 90.4, 16],
    [39.9, 116.4, 21], [34.0, -118.2, 13], [41.9, -87.6, 9], [19.4, -99.1, 8],
    [-34.6, -58.4, 15], [-22.9, -43.2, 13], [25.2, 55.3, 4], [33.3, 44.4, 7],
    [36.2, 37.1, 4], [45.5, -73.6, 5], [43.7, -79.4, 5], [49.3, -123.1, 3],
    [-1.3, 36.8, 3], [0.35, 32.6, 3], [9.0, 38.7, 4], [31.6, -8.0, 4],
    [30.0, -90.1, 2], [14.6, -90.5, 3], [25.7, -100.3, 5], [32.7, -97.0, 5],
    [47.5, 19.0, 2], [41.0, 28.9, 5], [50.1, 14.4, 2], [38.7, -9.1, 3],
    [52.2, 21.0, 3], [44.4, 26.1, 2], [59.9, 30.3, 5], [60.2, 24.9, 1],
    [-33.9, 151.2, 5], [-37.8, 145.0, 4], [-41.3, 174.8, 2], [36.8, 174.8, 2],
    [64.1, -21.9, 1], [55.7, 37.6, 1], [71.0, 25.0, 1], [-1.9, -78.5, 2],
    [-12.0, -77.0, 2], [4.7, -74.1, 3], [10.5, -66.9, 2], [18.5, -69.9, 2],
    [22.3, 114.2, 4], [25.0, 121.5, 4], [35.0, 135.7, 3], [43.1, 141.3, 2]
  ].sort(function (a, b) { return b[2] - a[2]; });

  let canvas = null, ctx = null, raf = 0, rot = 0, progress = 0, running = false;
  const slow = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const R = 132, S = 300, CX = 150, CY = 150;

  function project(lat, lon) {
    const la = lat * Math.PI / 180, lo = (lon - rot) * Math.PI / 180;
    const cosc = Math.cos(la) * Math.cos(lo);
    return { x: CX + R * Math.cos(la) * Math.sin(lo), y: CY - R * Math.sin(la), vis: cosc > 0, d: cosc };
  }

  function line(points, color, width) {
    ctx.strokeStyle = color; ctx.lineWidth = width || 0.7;
    ctx.beginPath();
    let drawing = false;
    points.forEach(function (p) {
      if (!p.vis) { drawing = false; return; }
      if (!drawing) { ctx.moveTo(p.x, p.y); drawing = true; }
      else ctx.lineTo(p.x, p.y);
    });
    ctx.stroke();
  }

  function frame() {
    if (!running) return;
    rot = (rot + (slow ? 0.0015 : 0.006)) % 360;
    const red = progress >= 1;
    ctx.clearRect(0, 0, S, S);

    // void and atmosphere
    const glow = ctx.createRadialGradient(CX, CY, R * .2, CX, CY, R * 1.16);
    glow.addColorStop(0, red ? "rgba(70,10,14,.55)" : "rgba(8,30,38,.55)");
    glow.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = glow; ctx.fillRect(0, 0, S, S);

    // sphere
    const sea = ctx.createRadialGradient(CX - 32, CY - 36, 10, CX, CY, R);
    sea.addColorStop(0, red ? "#2b0710" : "#08202a");
    sea.addColorStop(1, "#03070a");
    ctx.beginPath(); ctx.arc(CX, CY, R, 0, Math.PI * 2);
    ctx.fillStyle = sea; ctx.fill();
    ctx.strokeStyle = red ? "#ff5d6c" : "#1a6a70"; ctx.lineWidth = 1.2; ctx.stroke();

    // graticule, tinted by progress
    const gridCol = red ? "rgba(255,93,108,.55)" : "rgba(90,200,195,.26)";
    for (let lat = -60; lat <= 60; lat += 20) {
      const pts = [];
      for (let lon = -180; lon <= 180; lon += 5) pts.push(project(lat, lon));
      line(pts, gridCol);
    }
    for (let lon = -180; lon < 180; lon += 20) {
      const pts = [];
      for (let lat = -90; lat <= 90; lat += 5) pts.push(project(lat, lon));
      line(pts, gridCol);
    }

    // population-ordered infection
    const now = Date.now() / 1000;
    C.forEach(function (city, i) {
      const p = project(city[0], city[1]);
      if (!p.vis) return;
      const infected = (i + 1) / C.length <= progress + 0.0001;
      const rr = 1.4 + Math.min(2.4, city[2] / 11) * p.d;
      ctx.beginPath(); ctx.arc(p.x, p.y, rr, 0, Math.PI * 2);
      ctx.fillStyle = infected ? "#ff5d6c" : "#7dfbe6";
      ctx.shadowColor = infected ? "#ff2b45" : "#3ffbe0";
      ctx.shadowBlur = infected ? 10 : 4;
      ctx.fill(); ctx.shadowBlur = 0;
      if (infected) {
        const wave = (now * .55 + i * .07) % 1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, 3 + wave * 16, 0, Math.PI * 2);
        ctx.strokeStyle = "rgba(255,70,90," + (0.42 * (1 - wave)) + ")";
        ctx.lineWidth = 1; ctx.stroke();
      }
    });

    // scan sweep across the disk
    const sweep = ((now * .28) % 1) * S;
    ctx.fillStyle = "rgba(120,255,235,.06)";
    ctx.fillRect(0, sweep, S, 7);

    ctx.font = "10px 'Courier New', monospace";
    ctx.fillStyle = red ? "#ff5d6c" : "#4b9b92";
    ctx.fillText("GLOBAL COVERAGE " + Math.round(progress * 100) + "%", 8, 16);
    raf = requestAnimationFrame(frame);
  }

  window.M = window.M || {};
  M.globe = {
    mount: function (cv) {
      canvas = cv; ctx = cv.getContext("2d");
      canvas.width = S; canvas.height = S;
      running = true; frame();
    },
    setProgress: function (p) { progress = Math.max(0, Math.min(1, p)); },
    stop: function () { running = false; cancelAnimationFrame(raf); canvas = null; ctx = null; }
  };
})();
