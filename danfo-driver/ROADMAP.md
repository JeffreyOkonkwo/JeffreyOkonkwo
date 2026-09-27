# Danfo Craze: roadmap

Version 1.0 is items 1 to 3 plus the bus tag (done). Item 4 moved into the driver's licence (item 5). Items 5 to 8 are planned for versions 1.1 and 1.2 and are **not built yet**.

## Rules for every version
- Paid items are looks only. Nothing paid may raise a score.
- The quiz is never sold: no paid answers and no paid skips.
- The audience is 13 and over.
- All copy stays free of stereotypes about tribe, religion or poverty.
- Copy is written in full words, with no contractions and no em dashes.

## Version 1.0 (done)
1. **Game over screen:** one main action (Continue, by quiz or by ad), then Play Again, then Challenge a Friend. Double coins is a small link.
2. **Paid items are looks only:** the +25% coin bonus on paid Lagos routes is removed. Quiz continues are free (3 chances a run), so bought coins can never help a score.
3. **Quiz facts:** after every answer, a one-line "Did you know?" fact with its source.
4. **Driver look:** moved into the driver's licence (item 5). A single Oga or Madam switch felt wrong on its own, and the bus keeps just the conductor. In the licence, players build their own driver and choose whether their rank title reads Oga or Madam.
5. **Bus tag:** the slogan on the player's bus, GOD IS KING by default. Players pick another from a list or write their own (20 characters maximum, basic word filter). Free and looks only. When the leaderboard arrives, custom tags pass the same server word filter as nicknames.

## Version 1.1 (proposed): licence, leaderboard and Danfo Pass
The leaderboard shows the licence photo and the custom bus, so items 5 and 8 ship together.

### 5. Driver's licence
- **The player is the driver.** Options to customise:
  - name
  - face and skin tone
  - hair, facial hair or braids
  - headwear (cap, gele)
  - glasses
  - outfit
- **Unlocking:** a few free starter options. The rest unlock through play, the Danfo Pass or the shop.
- **The licence shows:**
  - photo
  - name
  - chosen flag
  - licence number
  - a rank title that grows with play: Learner, Driver, Oga or Madam (the player chooses which), Legend
- **Design notes:**
  - The licence "photo" is a drawn portrait built from the chosen options. It is never a camera photo, so no real images of players are collected.
  - Rank grows with distance driven, passengers carried and quiz answers. It never depends on money spent.
  - Options include a wide range of skin tones, hair types and headwear, with no option tied to a tribe or religion.

### Custom plate number
- The bus plate (now "AFRIKA 1") can be changed by the player: up to 8 letters and numbers.
- It shows on the bus in the game, in the Garage, on the licence and on the leaderboard.
- Editing the plate is free and is looks only. It passes the same word filter as nicknames.

### 8. Online leaderboard
- Each entry shows the player's flag, licence photo, custom bus and plate number next to their score.
- Challenge links open straight into the challenge.
- **Basic cheat checks:**
  - The server checks that a score is possible for the run time and speed.
  - It limits how often one device can submit scores.
  - It keeps the continue count with each score. Clean runs can have their own board.
- **Names:** nicknames pass a word filter, and there is a way to report a name.
- **Privacy work before launch:** accounts or a device ID, an update to the privacy policy, new Data safety and App Privacy answers, and a way for players to delete their leaderboard entry.

### Danfo Pass (the only subscription)
- The Danfo Pass replaces the planned Oga Driver Club, which has been removed from the code.
- It unlocks looks only (licence options, bus colours, plate styles, conductor looks). It never raises a score and never includes quiz help.
- **Store setup:** create one subscription product in both stores and one entitlement in RevenueCat when this version is built.

## Version 1.2 (proposed): conductor and city cards

### 6. Conductor as a sidekick
- **Look:** a conductor with a separate look and outfit.
- **Voice packs:**
  - languages: Pidgin, English, French
  - styles: calm, loud, comedy
- **Unlocking:** one conductor is free. More can be unlocked through play or bought.
- **Voice notes:** recorded by real voice actors. Accents are never used as the joke, and comedy lines come from situations on the road, not from people's background.

### 7. City card
- When a player reaches a new city, the game makes a shareable image with:
  - the city fact (with its source)
  - the player's custom bus and plate number
  - the licence photo
  - the score
  - the rank, if the player has one
- Players can save it to the phone or share it to WhatsApp, Instagram or TikTok.
- The image is made on the phone. Nothing is uploaded unless the player shares it.

## Open questions for Jeff
- **Leaderboard sign-in:** should players sign in (Google, Apple) or use an anonymous device ID?
- **Danfo Pass:** the price, and whether it runs monthly or by season.
- **Rank titles:** confirm the titles and the thresholds for each one.
