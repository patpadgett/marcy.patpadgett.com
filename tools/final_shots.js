const { chromium } = require('/home/pat/projects/ydks/node_modules/playwright');
const path = require('path');
const OUT = path.join(__dirname, '..', '.impeccable', 'review');

(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox', '--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  async function page(w, h) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.addInitScript(() => { try { localStorage.clear(); } catch (e) {} window.__forceAperture = true; });
    await p.goto('http://127.0.0.1:8814/index.html', { waitUntil: 'networkidle' });
    await p.waitForTimeout(1800);
    return p;
  }

  const p = await page(1440, 900);
  console.log('aperture active:', await p.evaluate(() => !!(window.M && M.Aperture && M.Aperture.active)));
  await p.screenshot({ path: path.join(OUT, 'desktop.png') });
  await p.evaluate(() => { document.getElementById('membrane').scrollTop = 9999; });
  await p.waitForTimeout(500);
  await p.screenshot({ path: path.join(OUT, 'desktop-bottom.png') });
  await p.evaluate(() => { document.getElementById('membrane').scrollTop = 0; });
  await p.waitForTimeout(300);

  // three punches
  await p.mouse.click(300, 640); await p.waitForTimeout(450);
  await p.mouse.click(1150, 720); await p.waitForTimeout(450);
  await p.mouse.click(760, 500); await p.waitForTimeout(1100);
  await p.screenshot({ path: path.join(OUT, 'desktop-cracked.png') });

  // a fragment card
  await p.click('button[data-go="guestbook"]', { force: true });
  await p.waitForTimeout(800);
  const ents = await p.$$('.ent');
  for (const i of [0, 1, 5]) { await ents[i].click({ force: true }); await p.waitForTimeout(1150); }
  await p.waitForTimeout(500);
  await p.screenshot({ path: path.join(OUT, 'fragment.png') });
  const fc = await p.$('.frag');
  if (fc) { await fc.click({ force: true }); await p.waitForTimeout(800); }

  // finale
  await p.evaluate(() => { [1, 2, 3, 4, 5, 6, 7].forEach(n => window.M.App.grant(n)); });
  for (let i = 0; i < 9; i++) {
    const f = await p.$('.frag');
    if (f) { await f.click({ force: true }); }
    await p.waitForTimeout(900);
  }
  await p.waitForTimeout(16000);
  await p.screenshot({ path: path.join(OUT, 'finale.png') });

  // widths
  const p2 = await page(1280, 800);
  await p2.screenshot({ path: path.join(OUT, 'width-1280.png') });
  await p2.close();

  const m = await page(390, 844);
  await m.screenshot({ path: path.join(OUT, 'mobile.png') });
  await m.mouse.click(200, 520); await m.waitForTimeout(700);
  await m.screenshot({ path: path.join(OUT, 'mobile-cracked.png') });
  await b.close();
  console.log('captured');
})().catch(e => { console.error('FATAL', e); process.exit(1); });
