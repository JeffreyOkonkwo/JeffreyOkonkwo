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
- **The player is the driver.** The look is set in five simple groups, one at a time, with big buttons:
  - **Face:** skin tone, lashes, lip colour, facial hair
  - **Hair:** afro, afro puff, braids, long braids, locs, bun, low cut, bald, and hair colour
  - **Headwear:** cap, head wrap, beanie, bucket hat, gele, and headwear colour
  - **Outfit:** plain shirt, football jersey, hoodie, dashiki, kitenge, suit and tie, Ankara print, kente, track jacket, boubou, agbada, denim jacket
  - **Extras:** glasses (round, square, shades) and earrings (studs, hoops)
- **No boy or girl labels.** Long hair, lashes, lip colour, earrings and head wraps are free for everyone, so any player can build any look without choosing a gender.
- **Unlocking:** every group has free options. More outfits, hair colours (auburn, blonde, blue, purple) and headwear colours unlock through play, the Danfo Pass or the shop. Looks only.
- **The licence shows:** photo, name, flag, licence number, plate number, rank and the furthest city reached.
- **Ranks are earned from the player's record, never picked.** Four ranks, based on the furthest city reached on the journey:

  | Rank | Earned by | Where the word comes from |
  |---|---|---|
  | JJC | Everyone starts here | West African Pidgin, "Johnny Just Come": a newcomer |
  | Area Driver | Reach Kano | Knows the roads; matches the game's middle level |
  | Pilot | Reach Cairo | Nairobi matatu slang (Sheng) for the driver |
  | Legend | Reach Johannesburg | Plain English, understood everywhere |

  None of the titles says anything about gender. Money never changes a rank.
- **Design notes:**
  - The licence "photo" is a drawn portrait built from the chosen options. It is never a camera photo, so no real images of players are collected.
  - No option is tied to a tribe or religion.

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
- It unlocks looks only (licence options, hair and headwear colours, bus colours, plate styles, conductor looks and speech bubble styles). It never raises a score and never includes quiz help.
- **Store setup:** create one subscription product in both stores and one entitlement in RevenueCat when this version is built.

## Version 1.2 (proposed): conductor and trip cards

### 6. Conductor as a sidekick
- **Look:** a conductor with a separate look and outfit. One is free; more unlock through play, the Danfo Pass or the shop.
- **No voices.** The conductor speaks in speech bubbles, as in the game today, so nothing is mispronounced and no accent is faked.
- **Players write the lines.** Three lines, each up to 24 letters, free to edit:
  - **Calling passengers:** "Come in! Come in!"
  - **Bus is moving:** "Oya, we dey go!"
  - **Close call:** "Driver, shine your eye!"
- **"Start from" buttons** fill in ready-made lines in Pidgin, English or French, so nobody has to type.
- **Safety:** each line passes the same word filter as the bus tag. Custom lines only show on the player's own phone; other players never see them.

### 7. Trip card
- **The run is never interrupted.** When a player reaches a new city during a run, a short banner shows (as the game does today) and the run keeps going.
- After the run, the game over screen shows one small link, "Trip card". It opens a shareable image with:
  - every city the run touched, with the new ones marked
  - one "Did you know?" fact about the newest city, with its source, sized to fit its box
  - the player's bus with its tag and plate number
  - the licence photo, name, rank and score
- Players can save it to the phone or share it to WhatsApp, Instagram or TikTok.
- The image is made on the phone. Nothing is uploaded unless the player shares it.

## Keep it simple
Every new screen must be easy for a young player to use without help:
- one main button per screen
- big buttons with short words
- at most one level of tabs
- no typing needed to play

## Open questions for Jeff
- **Leaderboard sign-in:** should players sign in (Google, Apple) or use an anonymous device ID?
- **Danfo Pass:** the price, and whether it runs monthly or by season.
- **Ranks:** confirm JJC, Area Driver, Pilot and Legend, and the cities that earn them.
