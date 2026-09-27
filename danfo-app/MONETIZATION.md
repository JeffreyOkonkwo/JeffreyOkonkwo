# Danfo Craze monetization reference

Ads and purchases are **on from version 1.0**:
- **Master switch:** `enabled: true` in `../danfo-driver/monetize/config.js`
- **Plugins:** `@capacitor-community/admob` and `@revenuecat/purchases-capacitor`
- **Native settings:** applied by `scripts/patch-native.py`

This page lists every piece in case you need to check, rebuild or switch something off.

**To ship a build with NO ads or purchases:**
1. Set `enabled: false` in the config.
2. Run `npm uninstall @capacitor-community/admob @revenuecat/purchases-capacitor`.
3. Remove AdMob and Purchases from `scripts/plugins-entry.js`.
4. Delete the AdMob blocks below from the native files.
5. Update the privacy policy and store answers to "no data collected".

## 1. Master switch
`enabled` in `../danfo-driver/monetize/config.js`. All the ad unit IDs, product IDs, entitlements and flags are in that file. The Oga Driver Club subscription stays hidden while `flags.ogaClub` is `false`.

## 2. Plugins
`scripts/plugins-entry.js` bundles AdMob, Purchases, Share and App into `www/monetize/plugins.js` at build time.

## 3. AdMob App IDs in the native files (already applied)
**Android.** In `android/app/src/main/AndroidManifest.xml`, add this inside `<application ...>`, just before `<activity`:
```xml
        <!-- AdMob App ID (Android). Ad unit IDs live in danfo-driver/monetize/config.js -->
        <meta-data
            android:name="com.google.android.gms.ads.APPLICATION_ID"
            android:value="ca-app-pub-4606547282835953~1503749311" />
        <!-- kid-safe ads for everyone (also set in code): child-directed, rated G -->
        <meta-data android:name="com.google.android.gms.ads.flag.OPTIMIZE_INITIALIZATION" android:value="true" />
        <meta-data android:name="com.google.android.gms.ads.flag.OPTIMIZE_AD_LOADING" android:value="true" />
```
(The file already removes the `AD_ID` permission, which a game played by children needs.)

**iOS.** In `ios/App/App/Info.plist`, add this before the final `</dict>`:
```xml
	<!-- AdMob App ID (iOS). Ad unit IDs live in danfo-driver/monetize/config.js -->
	<key>GADApplicationIdentifier</key>
	<string>ca-app-pub-4606547282835953~1312177623</string>
	<!-- Google's recommended SKAdNetwork IDs (ads work without Apple's tracking pop-up) -->
	<key>SKAdNetworkItems</key>
	<array>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>cstr6suwn9.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>4fzdc2evr5.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>2fnua5tdw4.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>ydx93a7ass.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>p78axxw29g.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>v72qych5uu.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>ludvb6z3bs.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>cp8zw746q7.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>3sh42y64q3.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>c6k4g5qg8m.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>s39g8k73mm.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>3qy4746246.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>f38h382jlk.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>hs6bdukanm.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>mlmmfzh3r3.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>v4nxqhlyqp.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>wzmmz9fp6w.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>su67r6k2v3.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>yclnxrl5pm.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>t38b2kh725.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>7ug5zh24hu.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>gta9lk7p23.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>vutu7akeur.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>y5ghdn5j9k.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>v9wttpbfk9.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>n38lu8286q.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>47vhws6wlr.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>kbd757ywx3.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>9t245vhmpl.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>a2p9lx4jpn.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>22mmun2rn5.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>44jx6755aq.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>k674qkevps.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>4468km3ulz.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>2u9pt9hc89.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>8s468mfl3y.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>klf5c3l5u5.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>ppxm28t8ap.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>kbmxgpxpgc.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>uw77j35x4d.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>578prtvx9j.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>4dzt52r2t5.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>tl55sbb4fm.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>c3frkrj4fj.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>e5fvkxwrpn.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>8c4e2ghe7u.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>3rd42ekr43.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>97r2b46745.skadnetwork</string>
		</dict>
		<dict>
			<key>SKAdNetworkIdentifier</key>
			<string>3qcr597p9d.skadnetwork</string>
		</dict>
	</array>
```
Don't add `NSUserTrackingUsageDescription`: the game never asks to track.

## 4. RevenueCat keys (never committed)
1. In RevenueCat, connect the Apple and Google apps to project **Danfo Craze**.
2. Create the products in both stores (see `README.md`).
3. Set up the entitlements: `no_ads` gets `remove_ads`, and `oga_club` gets `oga_driver_club_monthly`.
4. Copy `keys.example.json` to `keys.local.json` and paste the **public** keys (`appl_...`, `goog_...`). This file is git-ignored.

## 5. Build and test
- `npm run sync` gives a **development** build with Google's **test** ads. Test the rewarded continue, double coins, Honk Boost, the menu banner, every product in the shop, and Restore Purchases.
- `npm run sync:release` gives the store build with the **real** ad units.

## 6. Paperwork (under-13s are in the audience)
- Follow Google Play Families and Apple rules: see the end of `../danfo-driver/STORE_READY.md`.
- Update the privacy policy to add AdMob (kid-safe, non-personalised) and RevenueCat.
- Update the Data safety form, App Privacy labels and the "Contains ads" answer.
