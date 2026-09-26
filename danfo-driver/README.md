# Danfo Driver (prototype v0.1)

An endless-runner vertical slice set on Lagos roads. The whole game is one file with no build step, and it runs in any
modern browser on phone or laptop. Open `index.html` to play.

## Modes

- **Drive the danfo**: pick up hailing passengers (14 seats), drop them at named stops before the timer runs out
  (late means half fare), hop potholes, dodge go-slow traffic, pay LASTMA fines, and chase passengers who run
  off without paying ("Owo mi da?!"). Taking a one-way shortcut saves distance but sets the police on you for
  10 seconds. Crash while they're chasing and you pay a "settlement". Boarding passengers fills the
  **Bus Jam Party** meter: 9 seconds of synthesised afrobeat, bouncing passengers, double naira, and traffic moves out of your way.
  The day ends when the bus takes 3 hits. The score screen subtracts the owner's ₦12,000 "delivery" from what you made.
- **Catch the danfo**: you're a passenger late for work. Run, dodge okadas and hawkers, jump open gutters,
  and reach the loading danfo before it pulls off.

## Controls

| | Laptop | Phone |
|---|---|---|
| Change lane | ← → or A D | swipe left/right, or tap the left/right third of the screen |
| Hop | ↑ W or Space | swipe up, or tap the middle |
| Party / horn | P / H | on-screen buttons |

## Art direction

Everything is drawn in code on a canvas in a "clay" style: soft top-lit gradients, dark rims and a highlight on
every shape. Characters include gele and fila headwear, ankara-dot shirts, a conductor hanging off the door, hawkers
carrying pure water and gala, the yellow bus with two black stripes and a painted slogan, and a Ghana-must-go bag on the roof rack.
Sound is synthesised with WebAudio, so the game needs no asset files.

## Research

See [`RESEARCH.md`](RESEARCH.md) for sourced notes on danfo economics, conductor culture, enforcement, policy
(BITP franchising, Cowry card) and music, plus the game-design takeaways. Figures marked [UNVERIFIED] still need checking.

> Naming note: "Danfo Driver" is also the title of a well-known 2003 song by Mad Melon & Mountain Black.
> Do a trademark/naming check before any commercial release.
