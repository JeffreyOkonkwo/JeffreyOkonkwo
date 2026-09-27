// Every upload to Google Play or TestFlight needs a higher build number.
// Run `npm run bump` before each upload. `npm run bump -- 1.1` also sets the version players see.
const fs = require('fs'), path = require('path'), root = path.join(__dirname, '..');
const gp = path.join(root, 'android/app/build.gradle'), xp = path.join(root, 'ios/App/App.xcodeproj/project.pbxproj');
let g = fs.readFileSync(gp, 'utf8'), x = fs.readFileSync(xp, 'utf8');
const build = Math.max(+g.match(/versionCode (\d+)/)[1], +x.match(/CURRENT_PROJECT_VERSION = (\d+);/)[1]) + 1;
const name = process.argv[2];
g = g.replace(/versionCode \d+/, `versionCode ${build}`); x = x.replace(/CURRENT_PROJECT_VERSION = \d+;/g, `CURRENT_PROJECT_VERSION = ${build};`);
if (name) { if (!/^\d+(\.\d+){1,2}$/.test(name)) throw new Error('Version must look like 1.0 or 1.0.1'); g = g.replace(/versionName "[^"]*"/, `versionName "${name}"`); x = x.replace(/MARKETING_VERSION = [^;]+;/g, `MARKETING_VERSION = ${name};`); }
fs.writeFileSync(gp, g); fs.writeFileSync(xp, x);
console.log(`Build number is now ${build}` + (name ? `, version ${name}` : '') + '. Commit this change so the next bump starts from here.');
