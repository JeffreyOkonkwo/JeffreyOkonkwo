# Danfo Craze: brand sponsorships

Sponsorships are the fastest way to earn money from Danfo Craze. You sell sign space inside the game directly to brands and invoice them yourself. There is no ad network, no approval wait and no app update. You change `sponsors.json`, deploy the website, and every player sees the new signs the next time they open the game, on the web and in the store apps.

Publisher: **Hegenius, a business name of God Push Inc.** Contact: support@godpush.app

## What a brand gets

| Slot | Where it shows | How often |
|---|---|---|
| **Title sponsor** (`title`) | A "Presented by BRAND" line on the start screen | Every visit. Only one brand at a time. |
| **Billboards** (`billboards`) | Roadside billboards on bridges and lagoon stretches | About 60% of billboards when at least one sponsor is set |
| **Shop signs** (`shopSigns`) | Shop fronts along the road | About 1 shop in 5 |
| **Bus-stop banners** (`stopBanners`) | The banner under each bus-stop overpass | Every bus stop when at least one sponsor is set |

Text is shown in capitals, up to 40 characters. Each brand also picks one colour.

## Suggested packages (flat monthly, invoiced directly)

These are starting points. Adjust them once you know your monthly players.

| Package | Includes | Suggested price / month |
|---|---|---|
| **Street** | 1 shop sign | ₦50,000 (about $35) |
| **Junction** | 1 billboard + 1 shop sign | ₦150,000 (about $100) |
| **Bus Stop** | All bus-stop banners (shared, max 3 brands) | ₦250,000 (about $170) |
| **Presented by** | Title line + billboards + bus-stop banners (exclusive) | ₦750,000 (about $500) |

Tips:
- Offer a **free first month** to the first 2 or 3 local brands so the game looks sponsored. Other brands then follow.
- Put screenshots and your monthly player count in a one-page PDF. Screenshots from the game sell better than words.
- Take payment up front each month (bank transfer, Paystack or Stripe invoice).
- Use `weight` to give paying brands more screen time than free ones (weight 3 shows about 3× as often as weight 1).

## Brand policy (strict)

Danfo Craze is for players aged 13 and over, and younger players may still see it. **Only brands suitable for everyone.** Say no to:
- betting, lotteries or gambling
- alcohol, tobacco or vaping
- loans, crypto or "get rich" schemes
- dating
- politics or religion campaigns
- weapons
- anything that Google Play or App Store ad policies would reject

Good fits: food and drinks (non-alcoholic), transport, telecoms, schools, books, sports, music, local shops, fashion.

No links, phone numbers or website addresses go on signs. The signs are brand names and short slogans only, so players cannot tap out to a brand's site.

## How to change the signs

1. Edit `danfo-driver/sponsors.json`:

```json
{
  "title": { "text": "Sunny Jollof Co.", "color": "#FFC91A" },
  "billboards": [
    { "text": "Sunny Jollof - taste of home", "color": "#ff5a3c", "weight": 3 }
  ],
  "shopSigns": [
    { "text": "Sunny Jollof", "color": "#ff5a3c" },
    { "text": "Mama Put Express", "color": "#18b86b" }
  ],
  "stopBanners": [
    { "text": "Sunny Jollof", "color": "#ff5a3c" }
  ]
}
```

   - `text`: up to 40 characters (longer is cut off).
   - `color`: a hex colour like `#ff5a3c`.
   - `weight`: optional, default 1.
   - Set `"title": null` or leave a list as `[]` to use the game's own signs.
2. Commit and deploy the website. Players get the new list next time they open the game. Games that are offline keep the last copy that shipped with them.
3. When a sponsorship ends, remove the brand and deploy again.

Check that the file is valid JSON before deploying (for example, paste it into any JSON checker). If the file is broken, the game ignores it and shows its own signs.
