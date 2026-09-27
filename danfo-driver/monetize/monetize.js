// Danfo Craze money layer: rewarded ads, menu banner and in-app purchases.
// In the store apps it uses AdMob + RevenueCat (bundled into monetize/plugins.js by danfo-app).
// On the plain website neither exists, so ads and purchases are simply switched off.
(function () {
  const C = window.DC_MONEY_CONFIG, P = window.DCPlugins || null, isApp = !!(P && P.native), on = !!C.enabled;
  const native = isApp && on && !!(P.AdMob || P.Purchases), os = isApp ? P.platform : 'web';
  const release = !!(window.DC_BUILD && window.DC_BUILD.mode === 'release');
  const listeners = new Set(), owned = new Set(JSON.parse(localStorage.getItem('danfocraze.iap') || '[]'));
  let adsReady = false, privacyChoices = false, rcReady = false, entitlements = new Set(JSON.parse(localStorage.getItem('danfocraze.ent') || '[]')), storeProducts = {}, busy = false;
  const save = () => { try { localStorage.setItem('danfocraze.iap', JSON.stringify([...owned])); localStorage.setItem('danfocraze.ent', JSON.stringify([...entitlements])); } catch (e) {} };
  const emit = () => listeners.forEach(f => { try { f(); } catch (e) {} });
  const unit = kind => { // kind: rewardedContinue | rewardedDouble | rewardedHonk | bannerMenu
    if (!release) return C.testAdUnits[os][kind === 'bannerMenu' ? 'banner' : 'rewarded'];
    return C.adUnits[os][kind];
  };
  const S = C.adSafety;

  async function initAds() {
    if (!native || !P.AdMob) return;
    try {
      await P.AdMob.initialize({ initializeForTesting: !release, tagForChildDirectedTreatment: S.childDirected, tagForUnderAgeOfConsent: S.underAgeOfConsent, maxAdContentRating: S.maxAdContentRating });
      // Google's consent message (Europe, UK and other places that need it). No ads until it allows them.
      if (S.consent && P.AdMob.requestConsentInfo) {
        let ci = await P.AdMob.requestConsentInfo({ tagForUnderAgeOfConsent: S.underAgeOfConsent });
        if (ci.status === 'REQUIRED' && ci.isConsentFormAvailable) ci = await P.AdMob.showConsentForm();
        privacyChoices = ci.privacyOptionsRequirementStatus === 'REQUIRED';
        if (ci.canRequestAds === false) { emit(); return; }
      }
      adsReady = true; emit();
    } catch (e) { console.warn('AdMob init failed', e); }
  }
  function applyInfo(info) {
    if (!info) return;
    entitlements = new Set(Object.keys((info.entitlements && info.entitlements.active) || {}));
    for (const id of info.allPurchasedProductIdentifiers || []) { const p = C.products.find(x => x.id === id); if (p && p.type === 'non_consumable') owned.add(id); }
    save(); emit();
  }
  async function initPurchases() {
    if (!native || !P.Purchases) return;
    const key = os === 'ios' ? C.revenuecat.appleKey : C.revenuecat.googleKey;
    if (!/^(appl|goog)_/.test(key)) { console.warn('RevenueCat key missing: paste it in danfo-app/keys.local.json'); return; }
    try {
      await P.Purchases.configure({ apiKey: key });
      rcReady = true;
      P.Purchases.addCustomerInfoUpdateListener(applyInfo);
      applyInfo((await P.Purchases.getCustomerInfo()).customerInfo);
      const ids = C.products.filter(p => !p.flag || C.flags[p.flag]);
      for (const [type, list] of [['NON_SUBSCRIPTION', ids.filter(p => p.type !== 'subscription')], ['SUBSCRIPTION', ids.filter(p => p.type === 'subscription')]]) {
        if (!list.length) continue;
        const r = await P.Purchases.getProducts({ productIdentifiers: list.map(p => p.id), type });
        for (const sp of r.products || []) storeProducts[sp.identifier] = sp;
      }
      emit();
    } catch (e) { console.warn('RevenueCat init failed', e); }
  }

  // Shows a rewarded ad; resolves true only if the player watched to the end.
  function rewarded(kind) {
    if (!native || !adsReady || !C.flags.rewardedAds || busy) return Promise.resolve(false);
    busy = true;
    return new Promise(async resolve => {
      let got = false; const subs = [];
      const done = ok => { subs.forEach(h => h && h.remove && h.remove()); busy = false; resolve(ok); };
      try {
        subs.push(await P.AdMob.addListener('onRewardedVideoAdReward', () => { got = true; }));
        subs.push(await P.AdMob.addListener('onRewardedVideoAdDismissed', () => done(got)));
        subs.push(await P.AdMob.addListener('onRewardedVideoAdFailedToShow', () => done(false)));
        await P.AdMob.prepareRewardVideoAd({ adId: unit(kind), isTesting: !release, npa: S.nonPersonalized });
        await P.AdMob.showRewardVideoAd();
      } catch (e) { console.warn('rewarded ad failed', e); done(false); }
    });
  }
  let bannerOn = false;
  async function banner(show) {
    if (!native || !adsReady || !C.flags.menuBanner) return;
    const want = show && !entitlements.has(C.entitlements.noAds);
    if (want === bannerOn) return; bannerOn = want;
    try {
      if (want) await P.AdMob.showBanner({ adId: unit('bannerMenu'), adSize: 'ADAPTIVE_BANNER', position: 'BOTTOM_CENTER', margin: 0, isTesting: !release, npa: S.nonPersonalized });
      else await P.AdMob.removeBanner();
    } catch (e) { console.warn('banner failed', e); }
    document.documentElement.classList.toggle('has-banner', want);
  }
  function grant(p) { // what a purchase gives inside the game
    const g = p.grants || {};
    if (p.type === 'non_consumable') owned.add(p.id);
    if (g.entitlement) entitlements.add(g.entitlement);
    save();
    if (window.DC_ON_GRANT) window.DC_ON_GRANT(g, p);
    if (g.entitlement === C.entitlements.noAds) banner(false);
    emit();
  }
  async function buy(id) {
    const p = C.products.find(x => x.id === id), sp = storeProducts[id];
    if (!p || !rcReady || !sp) return { ok: false, reason: native ? 'unavailable' : 'web' };
    try {
      const r = await P.Purchases.purchaseStoreProduct({ product: sp });
      applyInfo(r.customerInfo); grant(p); return { ok: true };
    } catch (e) { return { ok: false, reason: e && e.userCancelled ? 'cancelled' : 'error' }; }
  }
  async function restore() {
    if (!rcReady) return false;
    try { const r = await P.Purchases.restorePurchases(); applyInfo(r.customerInfo);
      for (const id of owned) { const p = C.products.find(x => x.id === id); if (p && p.grants && p.grants.route && window.DC_ON_GRANT) window.DC_ON_GRANT({ route: p.grants.route }, p); }
      return true; } catch (e) { return false; }
  }
  window.DC_MONEY = {
    enabled: on, native, os, release,
    get adsReady() { return adsReady && C.flags.rewardedAds; },
    get storeReady() { return rcReady; },
    has: ent => entitlements.has(ent), owns: id => owned.has(id),
    price: id => (storeProducts[id] && storeProducts[id].priceString) || null,
    products: () => C.products.filter(p => !p.flag || C.flags[p.flag]),
    rewarded, banner, buy, restore, onChange: f => listeners.add(f),
    // players who saw the consent message must be able to change their answer (link in the name sheet)
    get privacyChoices() { return privacyChoices; },
    showPrivacyChoices: async () => {
      if (!(P && P.AdMob && P.AdMob.showPrivacyOptionsForm)) return;
      try { await P.AdMob.showPrivacyOptionsForm(); const ci = await P.AdMob.requestConsentInfo({ tagForUnderAgeOfConsent: S.underAgeOfConsent }); adsReady = ci.canRequestAds !== false; emit(); } catch (e) {}
    },
  };
  // native extras: Android back button pauses/returns home instead of closing the game
  if (isApp && P.App) {
    P.App.addListener('backButton', () => { if (window.DC_BACK) window.DC_BACK(); });
    P.App.addListener('pause', () => { if (window.DC_APP_HIDDEN) window.DC_APP_HIDDEN(); });
    P.App.addListener('resume', () => { if (window.DC_APP_SHOWN) window.DC_APP_SHOWN(); });
  }
  if (on) { initAds(); initPurchases(); }
})();
