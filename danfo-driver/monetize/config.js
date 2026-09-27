// Danfo Craze: every ad unit ID, product ID and money switch lives here.
// Ad unit IDs are not secrets. RevenueCat API keys are never committed: they come from
// danfo-app/keys.local.json at build time (see danfo-app/README.md) and arrive here as window.DC_BUILD.
window.DC_MONEY_CONFIG = {
  // MASTER SWITCH. Version 1.0 ships with no ads and no purchases: keep this false.
  // Version 1.1: set true and follow danfo-app/V1.1_MONETIZATION.md (plugins, native App IDs, RevenueCat keys).
  enabled: false,

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
  // Kid-safe ads for everyone: family-rated, no personalised or tracking ads, no Apple tracking pop-up
  adSafety: { childDirected: true, underAgeOfConsent: true, maxAdContentRating: 'General', nonPersonalized: true },

  // --- RevenueCat --------------------------------------------------------------------------
  revenuecat: {
    appleKey: (window.DC_BUILD && window.DC_BUILD.revenuecatAppleKey) || 'PASTE_REVENUECAT_APPLE_PUBLIC_KEY_IN_danfo-app/keys.local.json',
    googleKey: (window.DC_BUILD && window.DC_BUILD.revenuecatGoogleKey) || 'PASTE_REVENUECAT_GOOGLE_PUBLIC_KEY_IN_danfo-app/keys.local.json',
  },
  entitlements: { noAds: 'no_ads', ogaClub: 'oga_club' },
  // what each product gives; prices shown in the shop come from the store (localised)
  products: [
    { id: 'remove_ads', type: 'non_consumable', grants: { entitlement: 'no_ads' }, fallbackPrice: '$2.99' },
    { id: 'starter_pack', type: 'non_consumable', grants: { coins: 1500, skin: 'gold' }, fallbackPrice: '$0.99' },
    { id: 'coins_small', type: 'consumable', grants: { coins: 1000 } },
    { id: 'coins_medium', type: 'consumable', grants: { coins: 3500 } },
    { id: 'coins_large', type: 'consumable', grants: { coins: 10000 } },
    { id: 'route_lekki', type: 'non_consumable', grants: { route: 'lekki' } },
    { id: 'route_ikorodu', type: 'non_consumable', grants: { route: 'ikorodu' } },
    { id: 'route_third_mainland', type: 'non_consumable', grants: { route: 'mainland' } },
    { id: 'oga_driver_club_monthly', type: 'subscription', grants: { entitlement: 'oga_club' }, flag: 'ogaClub' },
  ],

  // --- feature flags ---------------------------------------------------------------------
  flags: {
    ogaClub: false,       // subscription is built but hidden until you switch this on
    rewardedAds: true,
    menuBanner: true,
  },
};
