import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 816, height: 1056 }, deviceScaleFactor: 2 });
await p.goto('file://./report.html'); await p.waitForTimeout(800);
await p.pdf({ path: '../reports/Delivery_Health_Report.pdf', format: 'Letter', printBackground: true });
const n = await p.locator('.pg').count();
for (let i = 0; i < n; i++) await p.locator('.pg').nth(i).screenshot({ path: `./rp_${i + 1}.png` });
await b.close(); console.log('pages', n);
