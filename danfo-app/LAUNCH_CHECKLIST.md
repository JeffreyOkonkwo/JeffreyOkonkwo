# Danfo Craze: build and upload checklist (Mac)

App ID: `com.hegenius.danfocraze` · Publisher: Hegenius · Support: support@godpush.app
Store form answers: `../danfo-driver/STORE_READY.md`

## 1. Set up the Mac (once)
- [ ] Install **Xcode** from the Mac App Store, open it once, and accept the licence.
- [ ] Install **Android Studio** (it includes Java).
- [ ] Install **Node.js 22 or newer** from nodejs.org.
- [ ] In Terminal:
  ```bash
  git clone https://github.com/JeffreyOkonkwo/JeffreyOkonkwo.git
  cd JeffreyOkonkwo && git checkout claude/danfo-driver-game-bffg28
  cd danfo-app && npm install
  ```

## 2. Consoles (while accounts are approved)
- [ ] **AdMob:** Privacy and messaging, create and publish a **European regulations message**. Blocking controls: maximum rating **PG**.
- [ ] **Google Play Console:** Create app, name "Danfo Craze", Game, Free.
- [ ] **App Store Connect:** Apps, New App, bundle ID `com.hegenius.danfocraze`, SKU `danfocraze`.

## 3. Tester build (Google test ads)
- [ ] `npm run sync`
- [ ] **Android:** `npm run android`. In Android Studio: Build, Generate Signed App Bundle or APK, Android App Bundle, Create new key store. Save the key store file **outside** the project, and back up the file and its password in two safe places. Build the **release** variant.
- [ ] Play Console: Testing, Internal testing, Create release, upload `android/app/release/app-release.aab`, add testers by email, and share the join link.
- [ ] Play Console: Settings, License testing, add the same emails (their purchases are free test purchases).
- [ ] **iPhone:** `npm run ios`. In Xcode: App target, Signing and Capabilities, choose the God Push Inc. team. Then Product, Archive, Distribute App, App Store Connect, Upload.
- [ ] App Store Connect: TestFlight, add internal testers (same day) or an external group with a public link (short beta review first).

## 4. Purchases (after the first upload)
- [ ] Create the 8 products in both consoles (IDs and prices in `STORE_READY.md`).
- [ ] RevenueCat: connect both apps (bundle ID `com.hegenius.danfocraze`), attach `remove_ads` to the entitlement `no_ads`.
- [ ] `cp keys.example.json keys.local.json` and paste the public keys (`appl_...` and `goog_...`). Never commit this file.
- [ ] `npm run bump`, `npm run sync`, then build and upload again (step 3). Testers can now try the shop.

## 5. Launch build (real ads)
- [ ] `npm run bump -- 1.0` (first time; afterwards `npm run bump`), then `npm run sync:release`. Never use this build for testing.
- [ ] Build and upload as in step 3.
- [ ] Fill in the store forms from `STORE_READY.md`: privacy policy URL `https://danfo-craze.vercel.app/privacy.html`, Data safety and App Privacy, ads, target audience **13 and over**, content rating.
- [ ] Google: promote the release to **Production** and send for review. Apple: **Submit for Review**.
- [ ] When the app is live: AdMob, App settings, **Link to app store** for each app.

## Every later update
`npm run bump`, then `npm run sync:release`, then build, upload and submit. Commit after each bump so that the build number keeps going up.
