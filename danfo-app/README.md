# Danfo Craze: store app (Android + iOS)

Published by **Hegenius, a business name of God Push Inc.** Support: support@godpush.app

App ID: **`com.hegenius.danfocraze`** (permanent once published; players never see it).

This folder wraps the web game in `../danfo-driver` as a native app with **Capacitor 8**. It adds:
- **AdMob:** rewarded ads (continue, double coins, Honk Boost) and a banner on the menu screen, with Google's consent message where the law requires it.
- **RevenueCat:** in-app purchases (Remove Ads, Starter Pack, coin packs, Lagos routes, Restore Purchases).
- **Brand sponsors:** billboards, shop signs, bus-stop banners and a "Presented by" line, controlled from `../danfo-driver/sponsors.json` on the website. See `../danfo-driver/SPONSORS.md`.
- **Native share, back-button handling and pause handling.**

To make a build with no ads or purchases, see `MONETIZATION.md`.

## Where things live
| What | File |
|---|---|
| All ad unit IDs, product IDs, entitlements, feature flags | `../danfo-driver/monetize/config.js` |
| Ads + purchases code | `../danfo-driver/monetize/monetize.js` |
| AdMob App ID, Android | `android/app/src/main/AndroidManifest.xml` (applied by `scripts/patch-native.py`) |
| AdMob App ID, iOS | `ios/App/App/Info.plist` `GADApplicationIdentifier` (applied by `scripts/patch-native.py`) |
| RevenueCat API keys | `keys.local.json`: **never committed** (git-ignored) |
| App name / bundle ID | `capacitor.config.json` (`com.hegenius.danfocraze`) |

## Test ads vs real ads
- `npm run sync` gives a **development** build. It always uses **Google's official test ad units**. Use this build for all testing: tapping your own real ads can get the AdMob account banned.
- `npm run sync:release` gives a **release** build. It uses the real ad units in `config.js`. Only build this for store uploads.

Ad settings (audience 13 and over):
- Not tagged as child-directed.
- Maximum ad rating **PG**.
- Never personalised, and no Apple tracking prompt.
- The Android advertising ID permission is removed.
- Google's consent message appears first in Europe, the United Kingdom and other places where the law requires it (create the message in AdMob, Privacy and messaging).

## RevenueCat keys (when your store accounts are ready)
1. In RevenueCat, open project **Danfo Craze**, connect the Apple app and the Google app, then create the products below in App Store Connect and Google Play Console.
2. Copy `keys.example.json` to **`keys.local.json`** and paste the **public** SDK keys:
   - `revenuecatAppleKey`: starts with `appl_`
   - `revenuecatGoogleKey`: starts with `goog_`
3. Run `npm run sync` (or `sync:release`). The build script writes the keys into the app bundle only, never into git.

Without keys, the game still runs normally. The shop just says it is connecting to the store.

## Products (create these IDs exactly in both stores)
| Product ID | Type | Gives |
|---|---|---|
| `remove_ads` | non-consumable, $2.99 | entitlement **no_ads**: no menu banner (rewarded ads stay optional) |
| `starter_pack` | non-consumable, $0.99 | 1,500 coins + Owambe Gold bus |
| `coins_small` / `coins_medium` / `coins_large` | consumable | 1,000 / 3,500 / 10,000 coins |
| `route_lekki` | non-consumable | Lekki route (new Lagos area, looks only) |
| `route_ikorodu` | non-consumable | Ikorodu route |
| `route_third_mainland` | non-consumable | Third Mainland at sunset route |

In RevenueCat, attach `remove_ads` to the entitlement **no_ads**. There is no subscription in version 1.0 (the Danfo Pass is planned for 1.1, see `../danfo-driver/ROADMAP.md`). You set the coin pack prices in the store consoles; the shop shows the local price from the store.

## Build
```bash
npm install
npm run sync            # or: npm run sync:release
npm run android         # opens Android Studio, then Build > Generate Signed Bundle (.aab)
npm run ios             # opens Xcode (on a Mac), then Product > Archive
```
Icons and splash screens are already generated from `../danfo-driver/brand`. If you ever delete and re-add the `android/` or `ios/` folders, run `npm run native:setup`. It reapplies the portrait lock, the AdMob App IDs, the kid-safe settings and the icons.

## Before you submit
Follow `LAUNCH_CHECKLIST.md` (build and upload steps on a Mac) and `../danfo-driver/STORE_READY.md` (store form answers). Publisher and developer name: **Hegenius**, a business name of God Push Inc. Support: support@godpush.app.
