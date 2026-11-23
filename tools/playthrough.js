const { chromium } = require('/home/pat/projects/ydks/node_modules/playwright');
const path = require('path');
const OUT = path.join(__dirname, '..', '.impeccable', 'review');

(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message + '\n' + e.stack));
  await p.addInitScript(() => { try { localStorage.clear(); } catch (e) {} });
  await p.goto('http://127.0.0.1:8814/index.html', { waitUntil: 'networkidle' });
  await p.waitForTimeout(1600);

  async function dismiss() {
    for (let i = 0; i < 3; i++) {
      const f = await p.$('.frag');
      if (!f) return;
      await f.click({ force: true }).catch(() => {});
      await p.waitForTimeout(900);
      if (await p.$('.frag')) await p.waitForTimeout(1200);
    }
  }
  async function go(v) { await p.click(`button[data-go="${v}"]`, { force: true }); await p.waitForTimeout(700); }
  async function frags() { return p.evaluate(() => Object.keys(window.M.App.state.frags).length); }

  // guestbook: three burns
  await go('guestbook');
  const ents = await p.$$('.ent');
  for (const i of [0, 1, 5]) {
    await ents[i].click({ force: true }).catch(() => {});
    await p.waitForTimeout(1100);
  }
  await p.screenshot({ path: path.join(OUT, 'g-burned.png') });
  console.log('after book', await frags()); await dismiss();
  await p.screenshot({ path: path.join(OUT, 'frag.png') });

  // pix: three developments
  await go('pix');
  const prints = await p.$$('.print');
  for (const i of [0, 1, 2]) {
    await prints[i].click({ force: true }).catch(() => {});
    await p.waitForTimeout(1200);
  }
  console.log('developed count', await p.evaluate(() => document.querySelectorAll('.print.developed').length));
  await p.screenshot({ path: path.join(OUT, 'g-developed.png') });
  console.log('after pix', await frags()); await dismiss();

  // counter
  await go('home');
  for (let i = 0; i < 3; i++) { await p.click('#counter', { force: true }); await p.waitForTimeout(500); }
  await p.waitForTimeout(3000);
  await p.screenshot({ path: path.join(OUT, 'g-counter.png') });
  console.log('after counter', await frags()); await dismiss();

  // quiz
  await go('quiz');
  const qs = await p.$$('.q');
  for (const q of qs) {
    const o = await q.$('.opt');
    if (o) { await o.click({ force: true }).catch(() => {}); await p.waitForTimeout(700); }
  }
  await p.waitForTimeout(900);
  await p.screenshot({ path: path.join(OUT, 'g-quiz.png') });
  console.log('after quiz', await frags()); await dismiss();

  // midi
  await go('home');
  await p.click('#midiBtn', { force: true });
  await p.waitForTimeout(6000);
  await p.screenshot({ path: path.join(OUT, 'g-midi.png') });
  console.log('after midi', await frags()); await dismiss();

  // ring
  await p.click('#ringNext', { force: true }); await p.waitForTimeout(1600);
  await p.screenshot({ path: path.join(OUT, 'g-node48.png') });
  await p.click('#ringNext', { force: true }); await p.waitForTimeout(1600);
  console.log('after ring', await frags()); await dismiss();

  // badge log
  await p.click('button[data-go="home"]', { force: true }); await p.waitForTimeout(600);
  await p.click('.badge.b1', { force: true }); await p.waitForTimeout(2500);
  await p.screenshot({ path: path.join(OUT, 'g-log.png') });
  await p.keyboard.press('Escape');
  await p.waitForTimeout(1200);

  console.log('after log', await frags()); await dismiss();
  await p.waitForTimeout(3500);
  await p.screenshot({ path: path.join(OUT, 'g-finale1.png') });
  await p.waitForTimeout(9000);
  await p.screenshot({ path: path.join(OUT, 'g-finale2.png') });

  // sign the guestbook
  const btn = await p.$('#finSign');
  if (btn) {
    await btn.click();
    await p.waitForTimeout(500);
    await p.fill('#finName', 'patrick');
    await p.keyboard.press('Enter');
    await p.waitForTimeout(1200);
    await p.screenshot({ path: path.join(OUT, 'g-finale3.png') });
  }
  console.log('ERRORS:', errs.length ? errs.join('\n---\n').slice(0, 2000) : 'none');
  await b.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
