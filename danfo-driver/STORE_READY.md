# Danfo Craze: store launch checklist

**Publisher:** Hegenius, a business name of God Push Inc. (federal corporation 1822561-3, Toronto, Ontario, Canada). Afrocade is the marketing brand that promotes the game; it is not the publisher, so don't list it as developer or seller.
**Support email:** support@godpush.app
**Version 1.0:** no ads and no in-app purchases. Ads and purchases arrive in version 1.1 (see the end of this file).

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
- [x] Store app project (`../danfo-app`, Capacitor 8) for Android and iOS, locked to portrait. The 1.0 build contains no ad or purchase SDKs.

## Accounts
- [ ] **Organization accounts under God Push Inc.**, not personal accounts, for both stores. Both need the company's **D-U-N-S number** (free from Dun & Bradstreet; allow a few days to a couple of weeks).
  - **Google Play Console:** organization account, **developer name: Hegenius**. The one-time fee is US$25. Verification asks for the D-U-N-S number, the company's legal details and a contact phone.
  - **Apple Developer Program:** enrol as an organization (God Push Inc., with its D-U-N-S number). The fee is US$99 a year. The seller name on the App Store is the legal entity.
- [ ] **Support email:** use **support@godpush.app** in both store listings (it's already on the privacy page).

## Store console answers for version 1.0 (no ads, no purchases)
- [ ] **Privacy policy URL:** `https://danfo-craze.vercel.app/privacy.html`. You can also host it on a God Push domain (for example godpush.app/danfo-craze/privacy).
- [ ] **Data safety (Google):** no data collected; no data shared. Everything stays on the device, and sharing only happens when the player chooses to.
- [ ] **App Privacy (Apple):** "Data Not Collected".
- [ ] **Ads:** "No, my app does not contain ads".
- [ ] **Age rating:** use the questionnaires. There is no violence (cars bump and fly off), no gambling, no chat, no ads and no purchases. Expect **Everyone / 4+**.
- [ ] **Audience: all ages.**
  - **Google Play:** select every age group, including under 13 (Families programme). Version 1.0 has no ads or purchases. "Challenge a friend" asks for a year of birth the first time, before it opens any other app.
  - **Apple:** rated 4+, so anyone can download it. The Kids category is possible for 1.0, but it would restrict version 1.1's ads, so it's simpler not to choose it.
- [ ] **Music rights:** keep proof that the 78 party clips were made on a **paid Suno plan** (Pro or Premier). A screenshot of the plan and the song list is enough.

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

## Version 1.1: ads and purchases (built, switched off in 1.0)
The code is ready. AdMob and RevenueCat accounts are set up, and the IDs are in `monetize/config.js`. To turn it on, follow `../danfo-app/V1.1_MONETIZATION.md`:
1. Set `enabled: true` in `monetize/config.js`.
2. Add the AdMob and RevenueCat plugins.
3. Add the AdMob App IDs to the native files.
4. Paste the RevenueCat keys.

**Because under-13s are in the audience, ads in 1.1 must follow Google Play Families and Apple Kids rules:**
- **Google Families:**
  - Use only Families self-certified ad SDKs. AdMob qualifies.
  - Tag every ad request as child-directed (COPPA) with max rating **G**, and show non-personalised ads only.
  - Don't use the Android advertising ID. The manifest removes the `AD_ID` permission.
  - Keep ads clearly separate from gameplay, and don't use deceptive or interruptive formats. Rewarded ads are opt-in only, and the banner shows on the menu only.
  - In-app purchases must be clear about what they cost. Children's purchases go through Google's family approval.
- **Apple:**
  - The Kids category doesn't allow third-party ads, so keep the app **out of the Kids category** and rate it 4+.
  - Don't show the tracking (ATT) prompt and don't track.
  - Keep the kid-safe ad settings above for everyone.
  - Purchases must use Apple in-app purchase (RevenueCat does), with a **Restore Purchases** button (built).
- **Updates:**
  - Update the privacy policy, the Data safety form and Apple's App Privacy labels **before** 1.1 is released. They must list AdMob (device and ad data, coarse location, for advertising and fraud prevention) and RevenueCat (purchase history and an app user ID, for app functionality).
  - Change the Google "Contains ads" answer to **Yes**.
