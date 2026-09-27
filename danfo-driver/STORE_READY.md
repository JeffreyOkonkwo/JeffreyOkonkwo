# Danfo Craze: store launch checklist

**Publisher shown to players:** Hegenius, a business name of God Push Inc. (Ontario business name, BIN 1001759289; God Push Inc. is federal corporation 1822561-3, Toronto, Ontario, Canada). Afrocade is the marketing brand that promotes the game. It is not the publisher, so do not list it as developer or seller.
**Support email:** support@godpush.app
**App ID (Android and iOS):** `com.hegenius.danfocraze`
**Audience:** players aged 13 and over. The game is not directed to children under 13.
**Version 1.0 earns from day one:** rewarded ads and a menu banner (Google AdMob), in-app purchases (RevenueCat), and brand sponsorships on in-game signs (see `SPONSORS.md`).

The step by step build and upload list is in `../danfo-app/LAUNCH_CHECKLIST.md`.

## Done in the game
- [x] Full code review of gameplay, screens, saved data, audio and offline play. All bugs found were fixed (see "Fixed" below).
- [x] Automated play testing on all 3 levels and several cities, plus tests of every screen and flow. No crashes, no memory growth and no numbers going wrong.
- [x] Works fully offline after the first launch. Fonts are bundled with the game, so there are no Google Fonts calls.
- [x] Sound stops when the app goes to the background or the phone locks, and a run pauses automatically.
- [x] No debug or cheat hooks in the live build.
- [x] App icons and splash screens for both stores.
- [x] Privacy policy at `/privacy.html`, linked inside the app from the name screen. It names Hegenius, a business name of God Push Inc., as publisher and support@godpush.app as the contact. It discloses AdMob ads, in-app purchases and the 13+ audience.
- [x] Google's consent message (Europe, the United Kingdom and other places where the law requires it) appears before any ads, and players can change their answer from the name screen ("Privacy choices").
- [x] The year of birth check was removed, because the game is now for players aged 13 and over.
- [x] English, Pidgin and French for all menus, missions, quiz and game over text.
- [x] Fits small phones (iPhone SE, 320 px wide) and large ones. Portrait layout only.
- [x] Store app project (`../danfo-app`, Capacitor 8, app ID `com.hegenius.danfocraze`) for Android and iOS, with AdMob and RevenueCat built in.
- [x] Money: rewarded ads (continue, double coins, Honk Boost), a menu banner, a shop (Remove Ads, Starter Pack, coin packs, 3 Lagos routes, Restore Purchases) and sponsor slots. All IDs are in `monetize/config.js`. Development builds use Google's test ads.
- [x] **Fair play rules:** paid items are looks only, and nothing paid can raise a score. Coins buy bus colours only. The paid Lagos routes give no extra points or coins. The quiz is never sold: continuing by quiz is free, limited to 3 chances a run, and there are no paid answers or skips. Each continue costs 5% of the score (10% for an ad), and the result shows a clean run or the number of continues.
- [x] **Game over screen:** one main action (Continue, by quiz or by ad), then Play Again, then Challenge a Friend. Double coins is a small link.
- [x] **Quiz:** after every answer, a one-line "Did you know?" fact with its source. All 561 questions have a source.
- [x] **Bus tag:** the slogan on the player's bus. The default is GOD IS KING. Players can write their own, and one tap brings back GOD IS KING (20 characters maximum, with a basic word filter). Free and looks only.
- [x] **Driver's licence:** the player builds a drawn driver (never a camera photo), picks a flag (all 249 countries and territories), a plate number and a name. The rank (JJC, Area Driver, Pilot, Legend) is earned from the furthest city reached. Looks are Free, Earn or Danfo Pass.
- [x] **Conductor:** one conductor on the bus with three looks (Classic free, Sunset earned, Party on the Pass) and three lines the player writes, with a word filter. No voices.
- [x] **New city welcome and trip card:** a small card at the top of the screen with WELCOME TO and the local greeting when a new city is reached, with Share, Save and Keep driving (the game pauses, the road stays in view, then a 3, 2, 1 countdown). Players can switch it to a small pop with no pause. After the run, a trip card with every city, one fact, and Share and Save.
- [x] **Garage:** 8 buses bought with coins, and stripe colours for Danfo Pass holders.
- [x] **Online leaderboard:** World, Clean runs and My country, only for players who say yes. Server checks that a score is possible, limits how often a device can submit, filters names and hides a name after 3 reports. Players can take themselves off at any time.
- [x] **Danfo Pass:** the only subscription (monthly). Looks only: gold licence frame and gold ring on the leaderboard, the flashiest looks, stripe colours, the Party conductor and new looks every month.

## Accounts
- [x] D-U-N-S number issued to God Push Inc.
- [ ] **Google Play Console:** organization account (paid, verification documents uploaded). After Google approves it, rename the developer name from "God Push" to **Hegenius**.
- [ ] **Apple Developer Program:** organization enrollment for God Push Inc. is under review. The seller name on the App Store is the legal entity (God Push Inc.). Hegenius can appear as the developer name where Apple allows it.
- [ ] **Support email:** use **support@godpush.app** in both store listings.

## AdMob settings
- [ ] **Privacy and messaging:** create and publish a **European regulations (GDPR) message** for this app. Without it, the consent step has nothing to show and ads will not serve in Europe and the United Kingdom. A **US state regulations** message is optional and recommended.
- [ ] **Blocking controls:** set the **maximum ad content rating to PG**, and block sensitive categories such as gambling, dating, alcohol and politics.
- [ ] **Do not** mark the app as child-directed in AdMob. The code does not tag ads as child-directed, because the audience is 13 and over.
- [ ] After the store listings are live, link the app to its store listing (Apps, App settings, Link to app store). Ads fill properly only after the account review passes and the app is linked.

## Google Play Console answers
- [ ] **Privacy policy URL:** `https://danfo-craze.vercel.app/privacy.html`
- [ ] **Ads:** "Yes, my app contains ads".
- [ ] **Advertising ID:** "No". The app removes the `AD_ID` permission and does not use the advertising ID.
- [ ] **Target audience and content:** select the age groups **13 to 15, 16 to 17, and 18 and over**. Do not select any group under 13. If Google asks whether the app could unintentionally appeal to children, answer honestly. If Google decides it may appeal to children, keep the store listing aimed at teenagers and adults.
- [ ] **Content rating:** complete the questionnaire truthfully. There is no violence beyond cartoon cars bumping, no gambling, no chat, and there are ads and in-app purchases.
- [ ] **Data safety:**
  - **Data collected and shared (by Google AdMob), for advertising, analytics and fraud prevention:**
    - Location: approximate location (from IP address)
    - App activity: app interactions
    - App info and performance: crash logs and diagnostics
    - Device or other IDs
  - **Data collected (by RevenueCat), for app functionality, not shared:**
    - Financial info: purchase history
  - **Data collected (by us, for the online leaderboard, only when the player says yes), for app functionality, not shared:**
    - Personal info: name (the nickname the player types)
    - App activity: other user-generated content (plate number and drawn driver look) and in-game scores
    - Device or other IDs: a random player number made by the app
    - Mark this data as **optional** (players can play without the leaderboard) and say players can ask for it to be deleted (they can remove it in the game).
  - **Data is encrypted in transit:** yes.
  - **Players can ask for data to be deleted:** yes, in the game (Ranks, Take me off the board) or by email to support@godpush.app.
  - Check these answers against Google's current "AdMob data disclosure" page and the RevenueCat data safety guide before you submit, because both pages are updated from time to time.

## Apple App Store Connect answers
- [ ] **Privacy policy URL:** `https://danfo-craze.vercel.app/privacy.html`
- [ ] **App Privacy:**
  - Data used to track you: **none**. The app never shows the tracking prompt.
  - **Data not linked to you:**
    - Location: coarse location (third party advertising, analytics)
    - Identifiers: device ID (third party advertising, analytics)
    - Usage data: product interaction and advertising data (third party advertising, analytics)
    - Diagnostics: crash data and performance data (third party advertising, analytics)
    - Purchases: purchase history (app functionality)
  - **Data linked to you (online leaderboard, only when the player says yes), for app functionality:**
    - Contact info: name (the nickname)
    - Identifiers: user ID (a random player number made by the app)
    - User content: gameplay content (score, plate number and drawn driver look)
    - None of it is used for tracking.
- [ ] **Age rating:** answer the questionnaire truthfully. If App Store Connect lets you choose a higher age rating than the calculated one, choose **13+**. Do not select "Made for Kids", and do not choose the Kids category.
- [ ] **Encryption:** already answered in the app (`ITSAppUsesNonExemptEncryption` is false), so uploads are not held for this question.

## In-app purchases
- [ ] Create the products in both consoles with exactly these IDs:
  - `remove_ads` (non-consumable)
  - `starter_pack` (non-consumable)
  - `coins_small`, `coins_medium`, `coins_large` (consumable)
  - `route_lekki`, `route_ikorodu`, `route_third_mainland` (non-consumable)
  - `danfo_pass_monthly` (auto-renewing subscription, 1 month). On Google Play, create it under Subscriptions with a monthly base plan. On the App Store, create a subscription group called Danfo Pass and add it there.
- [ ] **Suggested prices:** Danfo Pass $2.99 a month, Remove Ads $2.99, Starter Pack $0.99, coins $0.99, $2.99 and $6.99, routes $0.99 each.
- [ ] In RevenueCat, connect both apps using the bundle ID `com.hegenius.danfocraze`, attach `remove_ads` to the entitlement **no_ads** and `danfo_pass_monthly` to the entitlement **danfo_pass**, and paste the two public keys into `../danfo-app/keys.local.json` (never committed).

## Other
- [ ] **Leaderboard storage (one time):** in Vercel, open the danfo-craze project, Storage, Create, Blob, name it danfo-leaderboard and connect it to the project (all environments). Then redeploy. Until this is done the Ranks screen says the board is not open, and the rest of the game works as normal.
- [ ] **Sponsor signs:** brands suitable for a 13+ audience only (see `SPONSORS.md`). No betting, alcohol, loans, crypto, dating or political ads.
- [ ] **Music rights:** keep proof that the 5 party songs (danfo-v2-03a, 03b, 04b, 08a and 08b) were made on a **paid Suno plan** (Pro or Premier). A screenshot of the plan and the song list is enough.

## Store listing (draft)
- **Name:** Danfo Craze
- **Subtitle (Apple, 30 characters maximum):** Drive a danfo across Africa
- **Short description (Google, 80 characters maximum):** Dodge traffic, carry passengers, escape police and learn about Africa. We no dey carry last!
- **Full description:**
  > Take the driver's seat of a yellow Lagos danfo and hustle across Africa! Swipe to dodge okadas, BRT buses and wahala. Hop over potholes, pick up waving passengers for points, and do not let the police catch you, or you will have to settle!
  >
  > • Road trip from Lagos to Accra, Dakar, Marrakech, Cairo, Addis Ababa, Nairobi, Kigali, Kinshasa and Johannesburg, each with its own buses, landmarks and street life
  > • Rare Bus Jam Party: the road clears, the music drops, and passengers and coins come to you
  > • Crashed? Answer an Africa quiz question to keep driving, and learn a new fact with its source every time. More than 560 fact-checked questions about all 54 countries
  > • Day and night, rain, and Sun Coins that clear the sky
  > • Build your own driver's licence, earn your rank from JJC to Legend, and write your own bus tag and conductor lines
  > • A welcome in the local language in every new city, and a trip card to share after the run
  > • Online leaderboard: World, Clean runs and My country
  > • Daily missions, and challenge links to beat your friends
  > • Play in English, Pidgin or French. Works offline
- **Category:** Games, Racing (or Arcade). Secondary category: Education.
- **Developer:** Hegenius
- **Screenshots:** take them from the live game. Good ones are the title screen, a Lagos drive, a Bus Jam Party, a city landmark (Cairo or Nairobi), the quiz and the share card.

## Fixed in the code review
- **Hard mode:** a police officer could line up with cars so that all three lanes were blocked. Police now move with the traffic.
- **Challenge links and saved data:** a crafted link or damaged saved data could freeze the game. All saved values are now checked when they are loaded.
- **Party end:** the short safe moment after a party did not work, because a value was never set when a run started.
- **Title screen:** the background demo played party music, and the party song could carry on into a real run.
- **Continue after a crash:** sirens and half-finished lessons carried over into the continued run.
- **Keyboard:** Enter on a menu button started a run instead of opening the menu, and the P key could not resume the game.
- **Challenge links:** they broke for nicknames containing `~` or `%`.
- **Practice quiz:** coins could be earned without limit. It now pays at most 100 coins a day.
- **Daily bonus:** changing the phone clock could collect it again and again.
- **Minor:** "SPEED UP!" kept showing at top speed, "CHANCE AM" paid out for cars that a party had already pushed aside, and the name screen promised a leaderboard before it existed.
- **Offline cache:** pages load from the saved copy if the network takes longer than 3 seconds, music keeps at most 6 clips, and a missing file no longer returns the game page by mistake.
- **Battery:** the game redraws much less often behind the pause and game over screens, and cheap phone mode draws simpler shading.

## Turning ads or purchases off
To ship a build with no ads and no purchases, set `enabled: false` in `monetize/config.js`, remove the two plugins and the native AdMob IDs (steps in `../danfo-app/MONETIZATION.md`), and change the privacy policy and store answers back to "no data collected".
