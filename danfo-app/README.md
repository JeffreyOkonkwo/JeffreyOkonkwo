# Danfo Craze: store app (Android + iOS)

Published by **Hegenius, a business name of God Push Inc.** Support: support@godpush.app

This folder wraps the web game in `../danfo-driver` as a native app with **Capacitor 8**, adding native share, back-button handling and pause handling.

> **Version 1.0 has no ads and no purchases.** The ad and purchase plugins are *not* installed, and the AdMob App IDs are *not* in the native files. Everything for 1.1 (AdMob rewarded ads and menu banner; RevenueCat purchases) is built and switched off. To turn it on, follow **`V1.1_MONETIZATION.md`**. The rest of this README describes the 1.1 setup.

## Where things live
| What | File |
|---|---|
| All ad unit IDs, product IDs, entitlements, feature flags | `../danfo-driver/monetize/config.js` |
| Ads + purchases code | `../danfo-driver/monetize/monetize.js` |
| AdMob App ID, Android (1.1) | added to `AndroidManifest.xml` in 1.1: exact snippet in `V1.1_MONETIZATION.md` |
| AdMob App ID, iOS (1.1) | added to `Info.plist` (`GADApplicationIdentifier`) in 1.1: exact snippet in `V1.1_MONETIZATION.md` |
| RevenueCat API keys | `keys.local.json`: **never committed** (git-ignored) |
| App name / bundle ID | `capacitor.config.json` (`app.godpush.danfocraze`) |

## Test ads vs real ads
- `npm run sync` gives a **development** build. It always uses **Google's official test ad units**. Use this build for all testing: tapping your own real ads can get the AdMob account banned.
- `npm run sync:release` gives a **release** build. It uses the real ad units in `config.js`. Only build this for store uploads.

The ads are **kid-safe for everyone**:
- Tagged as child-directed and under the age of consent.
- Max rating **G**.
- Non-personalised only.
- No Apple tracking (ATT) pop-up.
- The Android advertising-ID permission is removed.

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
| `route_lekki` | non-consumable | Lekki route (new Lagos area, +25% coins there) |
| `route_ikorodu` | non-consumable | Ikorodu route |
| `route_third_mainland` | non-consumable | Third Mainland at sunset route |
| `oga_driver_club_monthly` | subscription | entitlement **oga_club**. **Hidden** until `flags.ogaClub = true` in `config.js` |

In RevenueCat, attach `remove_ads` to the entitlement **no_ads**, and `oga_driver_club_monthly` to **oga_club**. You set the coin pack prices in the store consoles; the shop shows the local price from the store.

## Build
```bash
npm install
npm run sync            # or: npm run sync:release
npm run android         # opens Android Studio, then Build > Generate Signed Bundle (.aab)
npm run ios             # opens Xcode (on a Mac), then Product > Archive
```
Icons and splash screens are already generated from `../danfo-driver/brand`. To regenerate them: `node scripts/make-icons.cjs`.

## Before you submit
See `../danfo-driver/STORE_READY.md`. For 1.0: no ads, no purchases, "Data not collected", all ages. Publisher / developer name: **Hegenius** (God Push Inc., organization accounts with a D-U-N-S number).
