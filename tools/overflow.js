const { chromium } = require('/home/pat/projects/ydks/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  for (const w of [390, 560, 768, 1024, 1280, 1440, 1600]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto('http://127.0.0.1:8814/index.html', { waitUntil: 'networkidle' });
    await p.waitForTimeout(900);
    const r = await p.evaluate(() => {
      const mem = document.getElementById('membrane');
      const bad = [];
      document.querySelectorAll('#page *').forEach(el => {
        const b = el.getBoundingClientRect();
        if (b.width === 0) return;
        if (b.right > window.innerWidth + 1 || b.left < -1) {
          bad.push((el.className || el.tagName) + ' @' + Math.round(b.left) + '..' + Math.round(b.right));
        }
      });
      return { sw: mem.scrollWidth, cw: mem.clientWidth, bad: bad.slice(0, 6) };
    });
    console.log(w, 'scrollW', r.sw, 'clientW', r.cw, r.bad.length ? 'OVERFLOW: ' + r.bad.join(' | ') : 'clean');
    await p.close();
  }
  await b.close();
})();
