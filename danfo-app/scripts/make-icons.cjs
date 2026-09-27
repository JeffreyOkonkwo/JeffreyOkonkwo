// Regenerates the app icons and splash screens from danfo-driver/brand (run: node scripts/make-icons.cjs)
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const root = path.join(__dirname, '..'), brand = path.join(root, '..', 'danfo-driver', 'brand');
const img = f => 'data:image/png;base64,' + fs.readFileSync(path.join(brand, f)).toString('base64');
const logoSvg = 'data:image/svg+xml;base64,' + fs.readFileSync(path.join(brand, 'logo.svg')).toString('base64');
const out = [];
const RES = path.join(root, 'android/app/src/main/res');
for (const [d, n] of [['mdpi', 48], ['hdpi', 72], ['xhdpi', 96], ['xxhdpi', 144], ['xxxhdpi', 192]]) {
  out.push({ f: `${RES}/mipmap-${d}/ic_launcher.png`, w: n, h: n, kind: 'icon' });
  out.push({ f: `${RES}/mipmap-${d}/ic_launcher_round.png`, w: n, h: n, kind: 'round' });
  out.push({ f: `${RES}/mipmap-${d}/ic_launcher_foreground.png`, w: n * 2.25, h: n * 2.25, kind: 'fg' });
}
for (const f of fs.readdirSync(RES)) if (f.startsWith('drawable')) { const s = path.join(RES, f, 'splash.png'); if (fs.existsSync(s)) { const [w, h] = execSync(`file "${s}"`).toString().match(/(\d+) x (\d+)/).slice(1).map(Number); out.push({ f: s, w, h, kind: 'splash' }); } }
const IOS = path.join(root, 'ios/App/App/Assets.xcassets');
out.push({ f: `${IOS}/AppIcon.appiconset/AppIcon-512@2x.png`, w: 1024, h: 1024, kind: 'ios' });
for (const f of fs.readdirSync(`${IOS}/Splash.imageset`)) if (f.endsWith('.png')) out.push({ f: `${IOS}/Splash.imageset/${f}`, w: 2732, h: 2732, kind: 'splash' });
(async () => {
  const b = await chromium.launch(), p = await b.newPage();
  await p.setContent(`<img id=i src="${img('icon-1024.png')}"><img id=l src="${logoSvg}">`); await p.waitForFunction(() => [...document.images].every(i => i.complete));
  for (const o of out) {
    const data = await p.evaluate(({ w, h, kind }) => {
      const c = document.createElement('canvas'); c.width = w; c.height = h; const x = c.getContext('2d'), i = document.getElementById('i'), l = document.getElementById('l'), G = '#18b86b';
      if (kind === 'icon' || kind === 'ios') { x.fillStyle = G; x.fillRect(0, 0, w, h); const s = kind === 'ios' ? 1.12 : 1; x.drawImage(i, (w - w * s) / 2, (h - h * s) / 2, w * s, h * s); }
      else if (kind === 'round') { x.beginPath(); x.arc(w / 2, h / 2, w / 2, 0, 7); x.clip(); x.fillStyle = G; x.fillRect(0, 0, w, h); x.drawImage(i, w * .06, h * .06, w * .88, h * .88); }
      else if (kind === 'fg') { const s = .62; x.drawImage(i, (w - w * s) / 2, (h - h * s) / 2, w * s, h * s); }
      else { const g = x.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#5ec8ff'); g.addColorStop(1, '#0e8f52'); x.fillStyle = g; x.fillRect(0, 0, w, h);
        const lw = Math.min(w * .8, h * .8 * 1600 / 660), lh = lw * 660 / 1600; x.drawImage(l, (w - lw) / 2, (h - lh) / 2, lw, lh); }
      return c.toDataURL('image/png').split(',')[1];
    }, o);
    fs.writeFileSync(o.f, Buffer.from(data, 'base64'));
  }
  fs.writeFileSync(`${RES}/values/ic_launcher_background.xml`, '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#18B86B</color>\n</resources>\n');
  console.log('wrote', out.length, 'images'); await b.close();
})();
