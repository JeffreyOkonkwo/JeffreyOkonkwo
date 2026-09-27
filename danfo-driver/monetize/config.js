// Danfo Craze: every ad unit ID, product ID and money switch lives here.
// Ad unit IDs are not secrets. RevenueCat API keys are never committed: they come from
// danfo-app/keys.local.json at build time (see danfo-app/README.md) and arrive here as window.DC_BUILD.
window.DC_MONEY_CONFIG = {
  // MASTER SWITCH for ads + purchases (on from version 1.0). Set false to ship a build with neither.
  enabled: true,

  // --- AdMob -------------------------------------------------------------------------------
  // App IDs go in native files: android/app/src/main/AndroidManifest.xml and ios/App/App/Info.plist
  admobAppId: {
    android: 'ca-app-pub-4606547282835953~1503749311',
    ios: 'ca-app-pub-4606547282835953~1312177623',
  },
  // real ad units: used ONLY in release builds (npm run sync:release)
  adUnits: {
    android: {
      rewardedContinue: 'ca-app-pub-4606547282835953/4220488550', // Continue After Crash
      rewardedDouble: 'ca-app-pub-4606547282835953/2907406884',   // Double Naira (double coins)
      rewardedHonk: 'ca-app-pub-4606547282835953/9281243544',     // Honk Boost
      bannerMenu: 'ca-app-pub-4606547282835953/6655080205',       // Menu Screen banner
    },
    ios: {
      rewardedContinue: 'ca-app-pub-4606547282835953/2715835199',
      rewardedDouble: 'ca-app-pub-4606547282835953/5673171026',
      rewardedHonk: 'ca-app-pub-4606547282835953/1774202893',
      bannerMenu: 'ca-app-pub-4606547282835953/7686014288',
    },
  },
  // Google's official TEST ad units: used in every development build
  testAdUnits: {
    android: { rewarded: 'ca-app-pub-3940256099942544/5224354917', banner: 'ca-app-pub-3940256099942544/9214589741' },
    ios: { rewarded: 'ca-app-pub-3940256099942544/1712485313', banner: 'ca-app-pub-3940256099942544/2435281174' },
  },
  // Audience is 13 and over (not directed to children). Ads are rated PG at most and never personalised,
  // there is no Apple tracking pop-up, and players in Europe and the UK see Google's consent message first.
  adSafety: { childDirected: false, underAgeOfConsent: false, maxAdContentRating: 'ParentalGuidance', nonPersonalized: true, consent: true },

  // --- RevenueCat --------------------------------------------------------------------------
  revenuecat: {
    appleKey: (window.DC_BUILD && window.DC_BUILD.revenuecatAppleKey) || 'PASTE_REVENUECAT_APPLE_PUBLIC_KEY_IN_danfo-app/keys.local.json',
    googleKey: (window.DC_BUILD && window.DC_BUILD.revenuecatGoogleKey) || 'PASTE_REVENUECAT_GOOGLE_PUBLIC_KEY_IN_danfo-app/keys.local.json',
  },
  entitlements: { noAds: 'no_ads', pass: 'danfo_pass' },
  // what each product gives; the shop shows the store's local price, and fallbackPrice (US dollars) until the store answers
  // Keep fallbackPrice the same as the prices set in App Store Connect and Google Play Console.
  // Paid items are looks only: nothing paid can raise a score. Coins buy bus colours only.
  // The Danfo Pass is the only subscription: looks only (gold frame, Pass looks, stripe colours, monthly looks).
  products: [
    { id: 'danfo_pass_monthly', type: 'subscription', grants: { entitlement: 'danfo_pass' }, fallbackPrice: '$2.99' },
    { id: 'remove_ads', type: 'non_consumable', grants: { entitlement: 'no_ads' }, fallbackPrice: '$2.99' },
    { id: 'starter_pack', type: 'non_consumable', grants: { coins: 1500, skin: 'gold' }, fallbackPrice: '$0.99' },
    { id: 'coins_small', type: 'consumable', grants: { coins: 1000 }, fallbackPrice: '$0.99' },
    { id: 'coins_medium', type: 'consumable', grants: { coins: 3500 }, fallbackPrice: '$2.99' },
    { id: 'coins_large', type: 'consumable', grants: { coins: 10000 }, fallbackPrice: '$6.99' },
    { id: 'route_lekki', type: 'non_consumable', grants: { route: 'lekki' }, fallbackPrice: '$0.99' },
    { id: 'route_ikorodu', type: 'non_consumable', grants: { route: 'ikorodu' }, fallbackPrice: '$0.99' },
    { id: 'route_third_mainland', type: 'non_consumable', grants: { route: 'mainland' }, fallbackPrice: '$0.99' },
  ],

  // --- feature flags ---------------------------------------------------------------------
  flags: {
    rewardedAds: true,
    menuBanner: true,
  },
};
