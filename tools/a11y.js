const { chromium } = require('/home/pat/projects/ydks/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 1280, height: 800 }, reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  await p.goto('http://127.0.0.1:8814/index.html', { waitUntil: 'networkidle' });
  await p.waitForTimeout(1400);
  const r = await p.evaluate(() => ({
    calm: document.body.classList.contains('calm'),
    calmBtn: document.getElementById('calmToggle').textContent,
    marqueeAnim: getComputedStyle(document.querySelector('.marquee-in')).animationName,
    blinkAnim: getComputedStyle(document.querySelector('.blink-note')).animationName,
    focusRing: getComputedStyle(document.querySelector('.lnk'), ':focus-visible').outlineColor
  }));
  console.log(JSON.stringify(r));
  await p.keyboard.press('Tab'); await p.keyboard.press('Tab');
  console.log('focused:', await p.evaluate(() => document.activeElement.textContent.trim().slice(0,20)));
  await ctx.close(); await b.close();
})();
