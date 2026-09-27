# Danfo Craze: roadmap

All items below are **built** and in the game: version 1.0 (items 1 to 3 and the bus tag), plus the driver's licence, conductor, city cards, online leaderboard and Danfo Pass. Item 4 moved into the driver's licence.

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
4. **Driver look:** moved into the driver's licence (item 5). A single Oga or Madam switch felt wrong on its own, and the bus keeps just the conductor. In the licence, players build their own driver. Ranks are earned, never picked, and say nothing about gender.
5. **Bus tag:** the slogan on the player's bus, GOD IS KING by default. Players can write their own, and one tap brings back GOD IS KING (20 characters maximum, basic word filter). Free and looks only. When the leaderboard arrives, custom tags pass the same server word filter as nicknames.

## Version 1.1 (built): licence, leaderboard and Danfo Pass
The leaderboard shows the licence photo and the custom bus, so items 5 and 8 ship together.

### 5. Driver's licence
- **The player is the driver.** The look is set in five simple groups, one at a time, with big buttons:
  - **Face:** skin tone, lashes, lip colour, facial hair
  - **Hair:** afro, afro puff, braids, long braids, locs, bun, low cut, bald, and hair colour
  - **Headwear:** cap, head wrap, beanie, bucket hat, gele, and headwear colour
  - **Outfit:** plain shirt, football jersey, hoodie, dashiki, kitenge, suit and tie, Ankara print, kente, track jacket, boubou, agbada, denim jacket
  - **Extras:** glasses (round, square, shades) and earrings (studs, hoops)
- **No boy or girl labels.** Long hair, lashes, lip colour, earrings and head wraps are free for everyone, so any player can build any look without choosing a gender.
- **Colours kids love (built):** based on colour surveys of children and teenagers, every favourite is included. Blue and sky blue, pink, purple, red, green, black, white and yellow are free for outfits and headwear. Orange, turquoise, lavender, mint and cerulean (the Gen Z favourite blue) are earned. Gold, silver, lime green and neon pink are on the Pass. Hair can be blue (earned), or blonde, purple or pink (Pass). The Pass also gives 15 bus stripe colours.
- **Unlocking: Free, Earn or Pass.** Licence looks have no separate shop price, so players only see two kinds of tag.
  - **Free from the start (about 25 looks):** every skin tone, eight hair styles, head wrap, cap, earrings, glasses, lashes, lip colours and three outfits.
  - **Earn by playing (about 12):** for example locs and bun, beanie and bucket hat, dashiki, kitenge, suit and denim jacket, and the auburn and blue colours. Kept forever once earned.
  - **Danfo Pass (about 12):** the flashiest looks, such as gele, shades, Ankara, kente, agbada, boubou, track jacket, and gold, purple and blonde colours.
  - Free players can build a full, good-looking driver without paying; the Pass is what makes it stand out.
- **The licence shows:** photo, name, flag, licence number, plate number, rank and the furthest city reached.
- **Flags:** every country and territory (249), grouped as Africa first and then the rest of the world, plus "Africa (no country)". Use the open flag-icons set (MIT licence), about 540 KB compressed.
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
- **Three boards:** World, Clean runs (scores with no continues) and My country.
- Each entry shows the player's flag, licence photo, custom bus, plate number and rank next to their score.
- Challenge links open straight into the challenge.
- **Basic cheat checks:**
  - The server checks that a score is possible for the run time and speed.
  - It limits how often one device can submit scores.
  - It keeps the continue count with each score, for the Clean runs board.
- **Names:** nicknames pass a word filter, and there is a way to report a name.
- **Privacy:** no sign-in. The game makes a random player number, asks before the first score is sent, and players can take themselves off at any time. The privacy policy and store answers are updated.

### Danfo Pass (the only subscription)
- The Danfo Pass replaces the planned Oga Driver Club, which has been removed from the code.
- It unlocks looks only (licence options, hair and headwear colours, bus colours, plate styles, speech bubble styles). It never raises a score and never includes quiz help.
- **What makes players want it:** a gold licence frame that also shows on their leaderboard row, new looks every month, and the flashiest outfits and colours.
- **Shop vs Pass:** the shop keeps what it sells in 1.0 (coin packs, Remove Ads, the Starter Pack and the Lagos routes), and coins still buy the 8 buses in the Garage. The Pass adds stripe colours for any bus you own. Licence looks are never sold one by one; they are free, earned or in the Pass.
- **Store setup:** create the subscription `danfo_pass_monthly` in both stores and the entitlement `danfo_pass` in RevenueCat (see `STORE_READY.md`).

## Version 1.2 (built): conductor and trip cards

### 6. Conductor as a sidekick
- **Look:** Area Boy or Area Girl (with or without hijab), all free. Players pick one in the Garage.
- **No voices.** The conductor speaks in speech bubbles, as in the game today, so nothing is mispronounced and no accent is faked.
- **Players write the lines.** Three lines, each up to 24 letters, free to edit:
  - **Calling passengers:** "Come in! Come in!"
  - **Bus is moving:** "Oya, we dey go!"
  - **Close call:** "Driver, shine your eye!"
- **"Start from" buttons** fill in ready-made lines in Pidgin, English or French, so nobody has to type.
- **Safety:** each line passes the same word filter as the bus tag. Custom lines only show on the player's own phone; other players never see them.

### 7. New city card and trip card
- **New city card, during the run.** The first time a player reaches a city, the game pauses and a small card appears at the top of the screen, so the road and the bus stay in view. It says "WELCOME TO ACCRA!" with the city's own greeting and its language, for example "Akwaaba! Welcome, in Twi".
- **Three buttons:** Share, Save or Keep driving. Share and Save make a full picture with the bus, the licence photo, and one "Did you know?" fact with its source.
- **Settling back in:** after the card closes, a blinking 3, 2, 1 counts down. The road ahead is cleared and the bus is safe for a moment.
- **Opt out:** "Next time, no pause" switches to a small welcome pop that does not stop the game and fades after about 3 seconds. It can be switched back in Journey.
- **Only for new cities:** cities already reached get a short banner, so the card stays special.
- **Trip card, after the run:** a small "Trip card" link on the game over screen lists every city the run touched, with the new ones marked, one "Did you know?" fact about the newest city with its source, the player's bus and licence photo, and Share and Save buttons.
- **Sharing:** players can save the trip card to the phone or share it to WhatsApp, Instagram or TikTok. The image is made on the phone, and nothing is uploaded unless the player shares it.

## Keep it simple
Every new screen must be easy for a young player to use without help:
- one main button per screen
- big buttons with short words
- at most one level of tabs
- no typing needed to play

## Open questions for Jeff
- **Danfo Pass price:** the code suggests $2.99 a month. Change it in the store consoles if you want another price.
- **Leaderboard sign-in:** built with an anonymous player number and no sign-in. Google or Apple sign-in can come later if players want their place on a new phone.
