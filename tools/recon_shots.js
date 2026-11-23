const { chromium } = require('/home/pat/projects/ydks/node_modules/playwright');
const path = require('path'), fs = require('fs');
const OUT = '.impeccable/review/recon';
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8814/reconstruction.html', { waitUntil: 'networkidle' });
  await p.waitForTimeout(1200);
  await p.screenshot({ path: path.join(OUT, 'a1.png') });
  const n = await p.evaluate(() => document.querySelectorAll('.act, .outro').length);
  for (let i = 0; i < n; i++) {
    await p.evaluate(k => {
      const el = document.querySelectorAll('.act, .outro')[k];
      window.scrollTo({ top: el.offsetTop + Math.min(el.offsetHeight * 0.35, 420), behavior: 'instant' });
    }, i);
    await p.waitForTimeout(1500);
    await p.screenshot({ path: path.join(OUT, 'act' + (i + 1) + '.png') });
    const info = await p.evaluate(() => ({ act: document.body.getAttribute('data-act'), tc: document.getElementById('hudTC').textContent }));
    console.log(i + 1, JSON.stringify(info));
  }
  console.log('errors', errs.length ? errs.join(' | ') : 'none');
  await b.close();
})();
