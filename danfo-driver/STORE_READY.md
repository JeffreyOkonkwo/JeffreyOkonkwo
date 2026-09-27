# Danfo Craze: store launch checklist

**Publisher:** Hegenius, a business name of God Push Inc. (federal corporation 1822561-3, Toronto, Ontario, Canada). Afrocade is the marketing brand that promotes the game; it is not the publisher, so don't list it as developer or seller.
**Support email:** support@godpush.app
**Version 1.0 earns from day one:** kid-safe rewarded ads and a menu banner (AdMob), in-app purchases (RevenueCat), and brand sponsorships on in-game signs (see `SPONSORS.md`).

**Status:** the game code has been reviewed and tested, and the store app project is in `../danfo-app`. The items below that are not ticked are for God Push Inc. to do in the store consoles.

## Done in the game
- [x] A full code review of gameplay, screens and saved data, audio and offline play. All bugs found were fixed (see "Fixed" below).
- [x] Automated play-testing on all 3 levels and several cities, plus tests of every screen and flow. No crashes, no memory growth, no numbers going wrong.
- [x] Works fully offline after the first launch. Fonts are bundled with the game; there are no Google Fonts calls.
- [x] Sound stops when the app goes to the background or the phone locks, and a run pauses automatically.
- [x] Plays sound through the iPhone silent switch, as games are expected to.
- [x] No debug or cheat hooks in the live build.
- [x] App icon (the plate reads AFRIKA), plus a maskable icon for Android's round and squircle icon shapes. App icons and splash screens are generated for both stores.
- [x] Privacy policy at `/privacy.html`, linked inside the app from the name screen. It names Hegenius / God Push Inc. as publisher and support@godpush.app as the contact.
- [x] One-time year-of-birth check before Challenge a friend opens WhatsApp or other apps. The year itself is not stored, only "18+ yes".
- [x] English, Pidgin and French for all menus, missions, quiz and game-over text.
- [x] Fits small phones (iPhone SE, 320 px wide) and large ones. Portrait layout.
- [x] Store app project (`../danfo-app`, Capacitor 8, app ID `com.afrocade.danfocraze`) for Android and iOS, locked to portrait, with AdMob and RevenueCat built in.
- [x] Money: rewarded ads (continue, double coins, Honk Boost), a menu banner, a shop (Remove Ads, Starter Pack, coin packs, 3 Lagos routes, Restore Purchases) and sponsor slots. All IDs are in `monetize/config.js`, and development builds use Google's test ads.

## Accounts
- [ ] **Organization accounts under God Push Inc.**, not personal accounts, for both stores. Both need the company's **D-U-N-S number** (free from Dun & Bradstreet; allow a few days to a couple of weeks).
  - **Google Play Console:** organization account, **developer name: Hegenius**. The one-time fee is US$25. Verification asks for the D-U-N-S number, the company's legal details and a contact phone.
  - **Apple Developer Program:** enrol as an organization (God Push Inc., with its D-U-N-S number). The fee is US$99 a year. The seller name on the App Store is the legal entity.
- [ ] **Support email:** use **support@godpush.app** in both store listings (it's already on the privacy page).

## Store console answers for version 1.0 (kid-safe ads + purchases)
- [ ] **Privacy policy URL:** `https://danfo-craze.vercel.app/privacy.html`. It covers the ads, purchases and sponsor signs.
- [ ] **RevenueCat keys:** once both store accounts exist, connect the apps in RevenueCat and create the products (see `../danfo-app/README.md`). Then paste the public keys into `../danfo-app/keys.local.json`. Until then, the shop shows "Connecting to the store…" and the ads still work.
- [ ] **AdMob:**
  - Once the store listings exist, link the app to them in AdMob (Apps › App settings › Link to app store). Ads fill properly only after the account review passes and the app is linked.
  - In AdMob › Blocking controls, set the **max ad content rating to G** and turn off sensitive categories (gambling, dating, alcohol, politics).
- [ ] **Data safety (Google):**
  - **Collected, by AdMob:**
    - Approximate location (from IP address)
    - App interactions
    - Diagnostics
    - Device or other IDs (for advertising and fraud prevention, shared with Google)
  - **Collected, by RevenueCat:** purchase history, plus an app-generated user ID (for app functionality).
  - **Other answers:** data is encrypted in transit.
  - Cross-check against Google's "AdMob data disclosure" guide and RevenueCat's data safety guide.
- [ ] **App Privacy (Apple):**
  - Tracking: **No**.
  - **Data not linked to you:**
    - Coarse Location, Device ID, Product Interaction and Advertising Data (third-party advertising, via AdMob)
    - Purchase History (app functionality, via RevenueCat)
- [ ] **Ads:** "Yes, my app contains ads".
- [ ] **In-app purchases:** create the products in both consoles with these IDs:
  - `remove_ads`
  - `starter_pack`
  - `coins_small`, `coins_medium`, `coins_large`
  - `route_lekki`, `route_ikorodu`, `route_third_mainland`
  - The subscription stays off.
  - **Suggested prices:**
    - Remove Ads $2.99
    - Starter Pack $0.99
    - Coins $0.99 / $2.99 / $6.99
    - Routes $0.99 each
- [ ] **Age rating:** use the questionnaires. There is no violence (cars bump and fly off), no gambling and no chat. It contains ads and in-app purchases. Expect **Everyone / 4+**.
- [ ] **Audience and ad rules (under-13s play this game):**
  - **Google Play:** select every age group, including under 13 (Families programme). Families rules the game already follows:
    - AdMob, a Families self-certified ad SDK
    - every ad request child-directed (COPPA), rated G and non-personalised
    - no Android advertising ID
    - rewarded ads opt-in only; the banner on the menu only, never during play
    - no ads that mimic gameplay
    - purchases clearly priced by the store
  - **Apple:** rate 4+. **Don't choose the Kids category**, because Apple doesn't allow third-party ads there. No tracking prompt, and purchases through Apple with Restore Purchases.
  - **Sponsor signs:** family-friendly brands only (see `SPONSORS.md`). No betting, alcohol, loans, crypto, dating or political ads.
- [ ] **Music rights:** keep proof that the 5 party songs (danfo-v2-03a, 03b, 04b, 08a, 08b) were made on a **paid Suno plan** (Pro or Premier). A screenshot of the plan and the song list is enough.

## Building the app
See `../danfo-app/README.md`. In short: `npm install`, `npm run sync`, then `npm run android` (Android Studio, then a signed `.aab`) or `npm run ios` (Xcode on a Mac, then Archive).

## Store listing (draft)
- **Name:** Danfo Craze
- **Subtitle (Apple, 30 characters max):** Drive a danfo across Africa
- **Short description (Google, 80 characters max):** Dodge traffic, carry passengers, escape police and learn about Africa. We no dey carry last!
- **Full description:**
  > Hop in the driver's seat of a yellow Lagos danfo and hustle across Africa! Swipe to dodge okadas, BRT buses and wahala. Hop potholes, pick up waving passengers for points, and don't let the police catch you, or you'll have to settle!
  >
  > • Road trip from Lagos to Accra, Dakar, Marrakech, Cairo, Addis Ababa, Nairobi, Kigali, Kinshasa and Johannesburg, each with its own buses, landmarks and street life
  > • Rare Bus Jam Party: the road clears, the music drops, and passengers and coins come to you
  > • Crashed? Answer an Africa quiz question to keep driving. 560+ fact-checked questions about all 54 countries
  > • Day and night, rain, and Sun Coins that turn night to day
  > • Daily missions, bus colours to unlock, and challenge links to beat your friends
  > • Play in English, Pidgin or French. Works offline
- **Category:** Games › Racing (or Arcade). Secondary category: Education.
- **Developer / seller:** Hegenius (God Push Inc.)
- **Screenshots:** take them from the live game. Good ones are the title screen, a Lagos drive, a Bus Jam Party, a city landmark (Cairo or Nairobi), the quiz and the share card.

## Fixed in this review
- **Hard mode:** a police officer could line up with cars so all three lanes were blocked. Police now move with the traffic.
- **Challenge links and saved data:** a crafted link or damaged saved data could freeze the game forever. All saved values are now checked when they are loaded.
- **Party end:** the safety moment after a party didn't work, because a value was never set when a run started.
- **Title screen:** the background demo played party music and sounds, and the party song could carry on into your real run.
- **Continue after a crash:** sirens and half-finished lessons carried over. Also, a crash paid out an open Sun Coin card.
- **Keyboard:** Enter on a menu button started a run instead of opening the menu, and the P key couldn't resume the game.
- **Challenge links:** they broke for nicknames containing `~` or `%`.
- **Practice quiz:** coins could be farmed without limit. It now pays at most 100 coins a day.
- **Daily bonus:** changing the phone's clock could collect it again and again.
- **Minor:** "SPEED UP!" kept showing at top speed, "CHANCE AM" paid out for cars the party had already pushed aside, and the name screen promised a leaderboard that doesn't exist yet.
- **Offline cache:**
  - Pages load from the saved copy if the network takes longer than 3 seconds (weak 2G/3G).
  - Music keeps at most 6 clips, instead of all 78 (about 33 MB).
  - A missing file no longer returns the game page by mistake.
- **Battery:** the game redraws much less often behind the pause and game-over screens. Cheap-phone mode also draws simpler shading.

## Turning ads or purchases off
To ship a build with no ads and no purchases, set `enabled: false` in `monetize/config.js`, remove the two plugins and the native AdMob IDs (steps in `../danfo-app/MONETIZATION.md`), and switch the privacy policy and store answers back to "no data collected".
