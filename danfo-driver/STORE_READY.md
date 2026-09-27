# Danfo Craze: store launch checklist

**Status:** the game code has been reviewed and tested, and it is ready to be wrapped as an app. The items below that are not ticked need you (the Afrocade Media account owner) to do them in the store consoles.

## Done in the game
- [x] A full code review of gameplay, screens and saved data, audio and offline play. All bugs found were fixed (see "Fixed" below).
- [x] Automated play-testing on all 3 levels and several cities, plus tests of every screen and flow. No crashes, no memory growth, no numbers going wrong.
- [x] Works fully offline after the first launch. Fonts are bundled with the game; there are no Google Fonts calls.
- [x] Sound stops when the app goes to the background or the phone locks, and a run pauses automatically.
- [x] Plays sound through the iPhone silent switch, as games are expected to.
- [x] No debug or cheat hooks in the live build.
- [x] App icon (the plate reads AFRIKA), plus a maskable icon for Android's round and squircle icon shapes.
- [x] Privacy policy at `/privacy.html`, linked inside the app from the name screen.
- [x] English, Pidgin and French for all menus, missions, quiz and game-over text.
- [x] Fits small phones (iPhone SE, 320 px wide) and large ones. Portrait layout.

## You need to do (store consoles)
- [ ] **Privacy policy URL:** `https://danfo-craze.vercel.app/privacy.html`. Better still, host it on your own domain (for example afrocade.com).
- [ ] **Support email:** add one to both store listings. The privacy page tells people to use it.
- [ ] **Data safety (Google) and privacy labels (Apple):** answer **"No data collected"** and **"No data shared"**. Everything stays on the device, and sharing only happens when the player chooses to.
- [ ] **Age rating:** use the questionnaires. There is no violence (cars bump and fly off), no gambling, no chat and no purchases. Expect a rating around **Everyone / 4+**.
- [ ] **Audience:**
  - Recommended for launch: set the target age to **13+**. That avoids the stricter Kids and Families programme rules, because "Challenge a friend" opens WhatsApp and other apps.
  - If you want to appear in the Kids or Families sections, we need to add a "grown-ups only" check in front of the share buttons first. It's about an hour's work; just ask.
- [ ] **Music rights:** keep proof that the 78 party clips were made on a **paid Suno plan** (Pro or Premier). A screenshot of the plan and the song list is enough.
- [ ] **Developer accounts:** Google Play costs US$25 once. The Apple Developer Program costs US$99 a year.

## Wrapping the game as an app (next technical step)
Use **Capacitor**, which works for both stores from this same code:
1. Create a Capacitor project and copy the `danfo-driver/` folder in as the web assets. Leave out `music/SUNO_BRIEF.md`, `screenshots/` and `*.md`.
2. Add `@capacitor/share` and `@capacitor/app`. Use native share, because Android WebViews have no share sheet. Use `appStateChange` to pause the game when the app goes to the background.
3. Lock the screen to portrait on iOS (`Info.plist`) and Android (`AndroidManifest.xml`).
4. Generate the icons and splash screens from `brand/icon-1024.png` using `@capacitor/assets`.
5. Build: an Android App Bundle (`.aab`) for Google Play, and an Xcode archive for the App Store.

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
