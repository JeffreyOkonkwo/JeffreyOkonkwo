# Danfo Driver: Research Notes on Lagos Danfo Life

*Compiled September 2026 to inform game design. Sources are cited inline.*

> **Method note.** The research environment blocked direct page fetches for most Nigerian news sites, so many figures below come from search-engine summaries of the linked articles rather than full-text reads. Anything marked **[UNVERIFIED]** is common knowledge or appeared only in secondary summaries, and could not be confirmed against a primary source. Check these before quoting them in marketing or in-game "fact" cards.

---

## 1. Economics: why every trip is a hustle

### Scale
- LAMATA's managing director has said **more than 75,000 commercial buses ("danfo")** operate on Lagos roads ([BusinessDay](https://businessday.ng/news/article/75000-commercial-buses-ply-lagos-roads-lamata/), [Gazette NG](https://gazettengr.com/75000-commercial-buses-ply-lagos-roads-lamata/)). Informal minibuses are often said to carry **about 75% of passenger trips** in Lagos ([Wikipedia: Danfo](https://en.wikipedia.org/wiki/Danfo), summarised). Treat the 75% share as an approximate, widely repeated estimate.

### The owner's "delivery"
- Most drivers **lease the bus** and must "deliver" a fixed daily or weekly sum to the owner before they keep anything for themselves ([Al Jazeera, 2020](https://www.aljazeera.com/features/2020/10/14/thugs-cops-and-unions-the-trials-of-public-bus-drivers-in-lagos); [Legit.ng feature](https://www.legit.ng/editorial/feature/1496889-a-day-life-a-lagos-bus-driver-mainland/)). Some owners take payment weekly ([BellaNaija](https://www.bellanaija.com/2022/01/bird-lagos-danfo-driver/)). Hire-purchase is a common route to owning a bus: one owner bought his first danfo on hire-purchase for about N800,000 in 2015 and paid it off in roughly 18 months ([Financial Street](https://financialstreet.ng/the-world-of-hire-purchase-transporters-in-lagos/)).
- **[UNVERIFIED]** Current (2025-26) daily delivery amounts. No primary source was reachable. Anecdotal figures range from about N15,000 to N30,000+ a day depending on the bus and route. In the game, make this a tunable daily target rather than a fixed "real" number.
- One driver said he used to make **N10,000 daily instalments** on his vehicle while buying under N4,000 of fuel a day before subsidy removal ([BusinessDay](https://businessday.ng/transport/article/subsidy-removal-transportation-fare-rises-as-increase-in-fuel-pump-price-bite/)).

### Fuel after subsidy removal (May 2023 onward)
- Fares rose immediately after the subsidy was removed. One driver said a tank that once cost under N15,000 could no longer be filled for N30,000 ([Nairametrics, May 2023](https://nairametrics.com/2023/05/30/fuel-subsidy-removal-causes-transport-costs-to-skyrocket-in-lagos/); [BusinessDay](https://businessday.ng/transport/article/subsidy-removal-transportation-fare-rises-as-increase-in-fuel-pump-price-bite/)).
- **[UNVERIFIED in this session]** Petrol cost roughly N185-200/litre before removal.
- Prices swing hard. Pump prices fell to about **N739/litre** at some Lagos stations in December 2025 ([EnviroNews](https://www.environewsnigeria.com/pump-price-drops-to-n739-in-lagos-as-dangote-promises-further-relief-for-nigerians/)), then rose to **N1,300-1,380/litre** by September 2026 ([Vanguard, Sept 2026](https://www.vanguardngr.com/2026/09/petrol-pump-prices-defy-low-depot-rates-stay-above-n1300-2/); [Leadership](https://leadership.ng/transport-fares-rise-in-lagos-ogun-as-petrol-price-hits-n1380-litre/)).
- Some danfos run on **makeshift fuel tanks**, with jerry cans behind the seats and pipes fed through holes ([Ikeja Record, via search summary](https://www.ikejarecord.com/p/danfo-tales-surviving-lagos-as-a-bus-driver)).

### Fares
- Danfo fares roughly **N200-N700** for short and medium hops, according to a 2026 consumer guide ([Lagos.Cool](https://lagos.cool/transport)). This is a secondary source.
- After the September 2026 fuel spike, **Abule-Egba to Oshodi by danfo cost about N1,500, against N680 on BRT**, and Sango-Ota to Oshodi cost N1,500-1,700 ([Leadership](https://leadership.ng/transport-fares-rise-in-lagos-ogun-as-petrol-price-hits-n1380-litre/)).
- BRT reference fares after LAMATA's 2025-26 increase: Ikorodu to Obalende **N970**, Ikotun to CMS **N1,100**, Odogunyan to CMS **N1,140** ([Tribune](https://tribuneonlineng.com/full-list-new-brt-standard-route-fares-as-lamata-implements-13-hike/); [BusinessDay](https://businessday.ng/transport/article/lamata-releases-new-brt-fares-following-13-increase/)).
- Lagosians reportedly spend about **40% of income on commuting** (attributed to LSE/IGC research in a secondary summary; **[UNVERIFIED primary]**).

### Union and "agbero" levies
- In January 2022 Lagos introduced a consolidated **N800/day** informal-transport levy meant to replace multiple touts' charges. Before that, drivers reportedly paid about **N3,000/day** to agberos ([Ripples Nigeria](https://www.ripplesnigeria.com/lagos-pegs-danfo-levies-at-n800-daily-nurtw-reacts/); [Daily Trust](https://dailytrust.com/why-n800-daily-levy-on-transporters-is-generating-ripples-in-lagos/)).
- Drivers say extortion **continued anyway**. A Guardian report quotes drivers paying **over N8,000 daily** to NURTW workers ([Guardian NG](https://guardian.ng/features/executive-motoring/years-after-transport-harmonisation-levy-nurtw-continues-extortions/)).
- Al Jazeera described three layers of dues: **"booking"** (to start work at the park each morning), **"loading"** (per trip, about the fare of two passengers) and open-ended **"tickets"**. Some drivers said they hand **around half their daily earnings** to agberos ([Al Jazeera](https://www.aljazeera.com/features/2020/10/14/thugs-cops-and-unions-the-trials-of-public-bus-drivers-in-lagos)).
- One route account describes about **N50 at each of 10 agbero points plus 10 police checkpoints**, around N1,000 per trip. The park fee is called **"owo-load"** ([Legit.ng](https://www.legit.ng/editorial/feature/1496889-a-day-life-a-lagos-bus-driver-mainland/)).
- Investigations estimate agbero collections in the **tens to hundreds of billions of naira** a year: N123bn per year ([Sahara Reporters/ICIR, 2021](https://saharareporters.com/2021/07/22/how-lagos-transport-union-thugs-or-agberos-make-n123-billion-motorists-riders-every-year%E2%80%94)) and a "N328.5bn billing" figure ([Nigeria CommunicationsWeek](https://www.nigeriacommunicationsweek.com.ng/n328-5bn-billing-how-political-patronage-built-lagos-agbero-shadow-tax-empire/), not fully read).
- Violence happens. In May 2025, agberos reportedly assaulted a one-eyed conductor until he paid ([Guardian NG](https://guardian.ng/features/focus/drivers-commuters-lament-agberos-extortion-seek-proper-regulation/)). In 2020 an agbero stabbed a conductor with a key over an "afternoon due" at Fadeyi ([Al Jazeera](https://www.aljazeera.com/features/2020/10/14/thugs-cops-and-unions-the-trials-of-public-bus-drivers-in-lagos)).
- An agbero hanging off the bus shouting **"Owo mi da!"** ("Where's my money!") is a recognisable street scene ([Effiong Samuel](https://effiongsamuel.art/danfo-owo-mi-da-and-moving-in-lagos/)).

### Police, LASTMA and other officials
- Reports describe roadside payments of **N100-N500 per checkpoint**. Drivers estimate **N3,000-N4,000/day** in informal levies, and impounded buses are released only after fines of **N100,000 or more** ([Vanguard, Nov 2023](https://www.vanguardngr.com/2023/11/alleged-lastma-police-extortion-okada-operators-cash-in-as-danfo-drivers-withdraw-services-in-lagos/); [Tribune](https://tribuneonlineng.com/the-extortion-of-bus-drivers-by-men-in-uniform/)).
- **14 September 2026:** danfo drivers on the Iyana-Ipaja/Iyana-Iba axis went on strike over alleged extortion by LASTMA, police, FRSC and NURTW, saying LASTMA impounds buses for whole days ([Vanguard](https://www.vanguardngr.com/2026/09/lagos-commuters-stranded-as-commercial-bus-drivers-strike-over-alleged-extortion/)).
- The Lagos Vehicle Inspection Service (VIS/VIO) promised a crackdown on danfos in 2024 ([Nairametrics](https://nairametrics.com/2024/02/19/lagos-vis-vows-crackdown-on-danfo-other-commercial-transporters-in-2024/)).
- **One-way driving:** under the Lagos transport law of 2018, driving against traffic means **vehicle forfeiture**. A first offence can also bring **one year's imprisonment** and a repeat offence three years, and the licence can be revoked. Some offenders have been given community service ([Lagos Ministry of Justice](https://lagosstatemoj.org/2023/10/12/lasg-warns-against-violation-of-traffic-laws/)).

### CNG conversion
- The Presidential CNG Initiative ran **free conversions for commercial buses** in Lagos parks, aiming at **10,000 vehicles in 10 weeks** (16 January to 31 March 2025) ([Nairametrics](https://nairametrics.com/2025/01/17/fg-launches-campaign-to-convert-10000-commercial-vehicles-into-cng-in-10-weeks/); [Leadership](https://leadership.ng/p-cng-takes-free-vehicle-conversion-to-lagos-parks/)). About **50,000 CNG vehicles** were on Nigerian roads by January 2025, against a target of 1 million by 2027 ([The Sun](https://thesun.ng/fg-begins-free-cng-conversion-targets-1-m-vehicles-nationwide/)).

---

## 2. Daily life on the bus

- **Hours:** drivers work **10-12 hours a day, six days a week** ([Al Jazeera](https://www.aljazeera.com/features/2020/10/14/thugs-cops-and-unions-the-trials-of-public-bus-drivers-in-lagos)). Buses are loading before 6 a.m. ([Ikeja Record](https://www.ikejarecord.com/p/danfo-tales-surviving-lagos-as-a-bus-driver)). A conductor's day runs from early morning to late night with no breaks or benefits ([Nairametrics, 2022](https://nairametrics.com/2022/06/25/a-day-in-the-life-of-a-lagos-bus-conductor/)).
- **The conductor ("condo")** calls out routes, collects fares, gives change, and keeps a mental map of who has paid. Conductors also negotiate **"load" (luggage) fees** and split them with the driver. They are the crew member most likely to fight agberos, and without ID cards they are exposed to police at night ([Nairametrics](https://nairametrics.com/2022/06/25/a-day-in-the-life-of-a-lagos-bus-conductor/); [Kraks](https://kraks.co/being-a-lagos-conductor-is-a-talent-heres-why/)).
- **Calls and slang:**
  - "Oshodi oke! Oshodi oke!": destination chants ([Medium, K. Toriola](https://medium.com/@Dearkofoworola/danfo-4aa0fd8387f9)).
  - "Wole pelu change e!": "enter with your change!" Buses carry versions such as "Ojuelegba, enter with your change oh!" ([Vanguard](https://www.vanguardngr.com/2016/11/lagos-danfo-found-us-restaurant-inscription-ojuelegba-enter-change-oh/)).
  - "Ma wole": "don't enter" (bus full).
  - "Owa!": the passenger's "stop here!" ([EkoReporter](https://ekoreporter.com.ng/the-lagos-danfo-dictionary-slangs-every-passenger-must-know/), summary).
  - **[UNVERIFIED]**: "Wole wole" (hurry in), "shenge"/"shanji" (change) and "owo da?" / "owo yin da?" (where's your fare?). These are widely heard but could not be confirmed in a reachable source.
- **Change fights and fare-dodgers:** conductors fighting passengers over change is a recurring viral story. One fight over change ended up in a gutter ([Tori.ng](https://www.tori.ng/news/64401/show-of-shame-bus-conductor-and-passenger-fight-in.html)). In another, a passenger refused full payment over a **N100 balance** ([Legit.ng](https://www.legit.ng/people/1723325-man-narrates-dramatic-incident-lagos-bus-conductor-prays-woman-collecting-fare/)). A conductor blocked a passenger from getting off on an expressway ([Legit.ng](https://www.legit.ng/people/1459232-danfo-conductor-blocks-passenger-coming-struggles-chases-express-video/)). A passenger fled when police arrived, leaving "an angry driver and almost crying conductor" ([Medium, P. Eludini](https://medium.com/@petfemspeaks/life-lessons-from-lagos-danfo-buses-part-one-1cd8ffc4228d)).
- **Slogans:** buses carry stickers and painted mottos such as **"No Food for Lazy Man"**, plus proverbs in English and Yoruba, religious lines, and football and Fuji-star stickers. Scholars treat them as a "semiotic archive" ([MIT Press, *African Arts*](https://direct.mit.edu/afar/article/56/1/42/114689/Urban-Taxi-Slogans-The-People-s-Arts); [BusinessMonitor, Sept 2026](https://businessmonitor.ng/2026/09/04/the-golden-years-of-commercial-buses-in-lagos/)).
- **Hawkers:** Emeka Ogboh's field recordings capture the "syncopated cries of street and highway hawkers" alongside conductors ([Africa Is a Country](https://africasacountry.com/2013/08/emeka-ogbohs-experimental-videos-and-soundscapes-of-lagos)). Lagos has **banned street trading and hawking** since 2023 ([Vanguard](https://www.vanguardngr.com/2023/09/lasg-bans-total-street-trading-hawking/)), and LAGESC runs raids. In September 2026 the state said it would **arrest buyers** from illegal roadside traders ([Nairametrics](https://nairametrics.com/2026/09/09/lagos-begins-arrest-of-buyers-patronising-illegal-roadside-traders-next-week/)). **[UNVERIFIED specifics]**: the classic go-slow menu of gala, pure water sachets, plantain chips, Agege bread, phone cards and chargers is common knowledge with no dated source.
- **Okada and keke competition:** Lagos banned okada in 6 LGAs from 1 June 2022 and in 4 more (Kosofe, Oshodi-Isolo, Shomolu, Mushin) from 1 September 2022 ([Tribune](https://tribuneonlineng.com/lagos-extends-okada-ban-to-4-more-lgas-5-lcdas-effective-from-sept-1/)). Okada riders "cash in" whenever danfo drivers strike ([Vanguard, 2023](https://www.vanguardngr.com/2023/11/alleged-lastma-police-extortion-okada-operators-cash-in-as-danfo-drivers-withdraw-services-in-lagos/)).
- **Go-slow:** Numbeo ranked Lagos **Africa's most congested city**, with an average one-way commute of **68.3 minutes**. In June 2025 the state government said residents lose about **4 hours a day** in traffic, and congestion costs about **N4 trillion a year** ([BusinessDay](https://businessday.ng/opinion/article/why-lagos-traffic-is-a-%E2%82%A64-trillion-productivity-drain/); [Danne Institute](https://danneinstitute.org/publications/what-traffic-congestion-costs-lagos-commuters/)). Hotspots with sources: **Third Mainland Bridge** (tailbacks of several km, and reports of robberies on the bridge) ([ICE](https://www.ice.org.uk/what-is-civil-engineering/infrastructure-projects/third-mainland-bridge-lagos); [Kola King](https://kolaking.substack.com/p/third-mainland-bridge-of-horror-where)), **Mile 2-Oshodi**, **Oworonshoki-Gbagada**, and **Ojuelegba**. The Lekki-Epe corridor now has its own bus reform (below). No congestion ranking with sources was found for CMS, Obalende or Ikorodu Road, although they are universally cited.

---

## 3. Policy: the danfo's uncertain future

- **2017:** Governor Ambode's government announced a plan to phase out danfo and molue as "not conducive for a mega city" ([TheCable](https://www.thecable.ng/theyre-not-conducive-for-a-mega-city-lagos-to-phase-out-yellow-buses/); [Newsweek](https://www.newsweek.com/lagos-nigeria-yellow-danfo-bus-593596)). It did not happen.
- **First and Last Mile (FLM) buses:** 500 small shuttles were the first phase of a planned 5,000. Within two years most had "almost disappeared" or were in poor condition ([Guardian NG](https://guardian.ng/features/executive-motoring/towards-a-befitting-public-transport-system-for-centre-of-excellence/)).
- **July 2024:** from 1 October 2024 only VIS-certified danfos may run as mid-capacity buses on **Lekki-Epe**, with compliant korope feeding FLM routes. The governor's aide denied a "ban" ([Pulse](https://www.pulse.ng/story/is-sanwo-olu-banning-danfo-korope-buses-in-lagos-govs-aide-explains-2024072707390542172); [Guardian NG](https://guardian.ng/news/nigeria/metro/lagos-to-integrate-korope-danfo-buses-into-transport-reforms-official/)).
- **December 2025 to February 2026:** the Lekki-Epe Bus Reform Scheme brought regulated services and **Cowry Card** cashless fares, and the carriageway was declared **off-limits to informal operators** ([Nairametrics, Feb 2026](https://nairametrics.com/2026/02/18/lagos-says-lekki-epe-carriageway-out-of-bounds-for-informal-transport-operators/)).
- **August 2026, Bus Industry Transition Programme (BITP):** Lagos, NURTW and RTEAN signed an MoU to move danfo operators into **franchises on 8 Quality Bus Corridors**. The first four routes are Iju-Ishaga-Abule Egba, Ketu-Alapere-Akanimodo, Iyana-Iba-Igando-Iyana-Ipaja and Ojuelegba-Lawanson-Cele. Unions are reorganised as cooperatives and fares move to **fully digital payment** on a date not yet set ([Arise News](https://www.arise.tv/lagos-signs-mou-with-nurtw-rtean-to-transition-danfo-operators-into-regulated-bus-franchise-system/); [BusinessDay](https://businessday.ng/transport/article/lagos-moves-to-regulate-danfo-operators-under-bus-transition-programme/); [Nairametrics](https://nairametrics.com/2026/08/06/lagos-moves-to-phase-danfo-into-franchise-bus-system/)). Experts have already "spotted cracks" in the plan ([Nairametrics, 21 Aug 2026](https://nairametrics.com/2026/08/21/lagos-danfo-reform-faces-a-major-test-experts-spot-the-cracks/)). An earlier startup that tried cashless danfo fares **failed because of union resistance** ([Techpoint](https://techpoint.africa/insight/investigation-local-unions-broke-gona/)).
- "Lagos-Omnibus": no programme by that name was found. The current branding is **BITP / QBC franchising**, and **Lagbus** is the older state bus franchise. **[UNVERIFIED name]**

---

## 4. Music and culture

- **Heritage:** danfos began in the 1970s as **VW Type 2 Kombis** seating about 14. The name spread in the 1980s alongside the **VW T3**, and today's fleet is mostly Toyota HiAce and similar vans **[UNVERIFIED fleet mix]** ([Fulcrum](https://iafulcrum.com/mag/origin-story-lagos-danfo/); [A. Aderibigbe](https://abdulrahmanaderibigbe.com/the-danfo-story-the-yellow-heartbeat-of-lagos-the-danfo-story-the-yellow-heartbeat-of-lagos/)).
- **Livery:** yellow with **two black stripes** ([Digit NG](https://digitng.com/danfo-yellow-of-lagos/)). **[UNVERIFIED]** The yellow-and-black standard is usually credited to the Fashola era (2007-2015); an older blue-and-white scheme sometimes appears in earlier accounts. Red Bull has run a "Danfo Rally" ([Red Bull](https://www.redbull.com/ng-en/events/red-bull-danfo-rally/red-bull-danfo-rally-what-is-a-danfo)).
- **Music:** "Fuji and Afrobeat music blasted from worn-out speakers" ([BusinessMonitor](https://businessmonitor.ng/2026/09/04/the-golden-years-of-commercial-buses-in-lagos/)). Fuji plays on keke and buses, and **gospel-fuji** (Dekunle Fuji) has become a crossover genre ([The Naija Way](https://thenaijaway.substack.com/p/scaling-mount-fuji)). Street-pop is well documented as a genre ([TurnTable Charts](https://www.turntablecharts.com/news/2035)). **[UNVERIFIED]** Gospel and sermon tapes on early-morning runs are common knowledge but have no source here.
- **Anthem:** **"Danfo Driver"** (2003) by **Mad Melon and Mountain Black**, real ex-danfo drivers from Ajegunle. It later appeared in the 2006 US film *Phat Girlz* ([Pulse](https://www.pulse.ng/story/here-is-all-you-need-to-know-about-mad-melon-of-danfo-drivers-2024081409493688073); [Urban Central](https://urbancntrl.co/danfo-driver-album/)). **Note:** a game called "Danfo Driver" will invite comparison with this song. Consider a clearance or a nod.
- **Art:** Emeka Ogboh's sound works *Lagos-Oshodi* (2011) and *Conductors / Oshodi* (2018) use real conductor chants ([Frieze](https://www.frieze.com/article/emeka-ogbohs-kaleidoscopic-fragments-lagos); [Africa Is a Country](https://africasacountry.com/2013/08/emeka-ogbohs-experimental-videos-and-soundscapes-of-lagos)). Fela referenced Lagos go-slow, and Nollywood routinely uses danfos as comic set pieces. **[UNVERIFIED]**: no single definitive Nollywood title was confirmed.

---

## 5. Game-design takeaways

### Mechanics (15)
1. **Daily Delivery meter:** each shift starts in debt to Oga (the owner). A progress bar shows "Delivery -> Fuel -> Your own money", ordered to match how drivers actually get paid.
2. **Fuel price roulette:** the pump price changes between days (for example N739 to N1,380). You can refuel or risk running on the jerry can.
3. **Owo-load at the park:** a booking/loading fee is deducted at each terminal. Upgrades such as "union card" or "cooperative membership" reduce it, echoing BITP.
4. **Agbero hop-on:** a tout grabs the door mid-run shouting "Owo mi da!". You can pay, shake him off with a swerve (risk), or let the conductor argue (a timed minigame).
5. **Conductor call minigame:** rhythm prompts ("Oshodi oke! Ma wole!") pull more passengers when timed well. This ties into the music mode.
6. **Change juggling:** passengers pay with large notes. With no change you risk a fight; with correct change you get a tip multiplier. "Enter with your change" passengers are bonus fares.
7. **Fare-dodger chase:** a jumper bolts at "Owa!". Swipe to send the conductor after them, or let them go and lose fare. Keep it slapstick and never violent.
8. **Go-slow zones:** hotspot segments where speed drops and hawkers swarm. Buying gala or pure water restores a "passenger patience" meter.
9. **Passenger patience and on-time drops:** each passenger has a timer (office worker, student, market woman). Late drops mean shouting and lost tips.
10. **One-way shortcut (risk/reward):** you can dodge go-slow against traffic, but it raises a LASTMA heat meter. **Getting caught means the bus is impounded and the run ends**, which mirrors the real forfeiture law. Present it as bad play, not smart play.
11. **Checkpoint encounters:** stops that cost time. Documents and roadworthiness (a VIS upgrade) let you pass cleanly. Do not reward bribing as the optimal strategy (see sensitivity).
12. **CNG conversion upgrade:** lower running cost, with rare "gas station queue" events.
13. **Cowry Card lanes (late game):** on franchise corridors fares are digital, so there are no change fights but a stricter schedule. The player can see the city modernising.
14. **Okada/keke rivals:** bikes steal waiting passengers at stops. In "ban zones" the bikes disappear.
15. **Bus Jam Party mode:** an overnight or weekend mode where the playlist (Fuji, street-pop, Afrobeats, gospel-fuji) drives passenger mood and rhythm-based boarding. Custom slogans painted on the bus act as cosmetic buffs.

### Characters (archetypes)
- **Drivers:** the Veteran ("50 years on the road"), the Graduate forced into driving, the Hire-Purchase Hustler trying to own his bus, the Gospel Driver.
- **Conductors:** the Poet of the Pavement (fastest caller), the Brawler, the Tender-hearted one who prays for passengers before collecting fare.
- **Passengers:** Market Mama with load, Office Babe in heels, Student with no change, Preacher, Fare-Dodger, Hawker who boards to sell, Oyinbo tourist.
- **Officials and others:** LASTMA officer (orange/maroon uniform), police patrol, VIO inspector, LAGESC raid squad, Agbero crew and their "Chairman", Oga the bus owner.

### Locations and levels
Oshodi (hub), Ojuelegba (roundabout chaos), Third Mainland Bridge (long go-slow with lagoon view), CMS/Marina and Obalende (island terminals), Ikorodu Road, Iyana-Ipaja/Abule-Egba, Mile 2, and Lekki-Epe (late-game reform corridor).

### Sensitivity notes
- **Punch up, not down.** Drivers, conductors and hawkers are working people squeezed by the system. Humour should come from situations, not from their poverty, accents or intelligence.
- **Bribery:** real, and a real grievance (the September 2026 strike). Show it as a drain the player resents and can reduce by legitimate means (papers, VIS, cooperative), not as a cheat code. Avoid naming real officials or agencies in a defamatory way, and consider fictionalised agency names (for example "LTMA").
- **Violence:** reported stabbings and assaults happen, but keep chases cartoonish, with no weapons.
- **Real people:** do not depict identifiable union bosses (such as MC Oluomo) or politicians.
- **Language:** use Yoruba and Pidgin lines checked by native speakers, and localise subtitles.
- **Music licensing:** use original or cleared tracks in genre styles. Do not sample Fuji or Afrobeats hits without clearance. The name "Danfo Driver" overlaps the Mad Melon and Mountain Black song.
- **Traffic safety:** one-way driving kills people in real life. The game already punishes it; keep that framing.

---

# African cities (road trip after Nigeria)

After Kano, the run continues across Africa: Accra → Dakar → Marrakech → Cairo → Addis Ababa → Nairobi → Kigali → Kinshasa → Johannesburg, then back to Lagos.
Every city keeps your yellow danfo. Local minibuses, taxis, shop signs, conductor calls, street obstacles and clothing change with the city. The kerbs are painted in that country's flag colours.
Once you reach a place, you can start your next run there from **Journey**.

| City | Local minibus in game | Conductor | Calls used | Landmark drawn | Hop obstacles |
|---|---|---|---|---|---|
| Accra | tro-tro: white with red, gold or green stripe; slogans "GOD IS MY SEATBELT", "ALL SHALL PASS" | mate | "Circle! Circle!", "Kanesh-Kanesh-Kanesh!" | Black Star Gate by the sea | potholes, barriers |
| Dakar | car rapide in blue and yellow ("ALHAMDOULILAH"); white Ndiaga Ndiaye | apprenti | "Colobane!", "Petersen!", "Nanga def?" | African Renaissance Monument | sand drifts, sheep |
| Marrakech | beige grand taxi (no painted slogans) | - | "Bab Doukkala!", "Jemaa el-Fna! Yallah!" | Koutoubia minaret, snowy Atlas | barriers, sand |
| Cairo | white microbus | - | "Ramsis!", "Giza, Giza!", "Ataba, yalla!" | pyramids, Cairo Tower | potholes, bumps |
| Addis Ababa | blue-and-white minibus taxi | woyala | "Piassa!", "Megenagna!", "Bole!" | Entoto hills, glass bank tower | potholes, goats |
| Nairobi | matatu: white with yellow stripe plus graffiti art ("nganya") | makanga | "Tao! Tao!", "Beba beba!", "Rongai, panda!" | KICC, giraffes | potholes, branches |
| Kigali | white minibus with a blue or green band | - | "Nyabugogo!", "Kimironko!", "Muraho!" | Convention Centre dome, green hills | barriers only (no potholes, it's clean) |
| Kinshasa | yellow-and-blue taxi-bus ("TOKENDE" = "let's go") | receveur | "Victoire!", "Gombe!", "Ngaba, tokende!" | Limete Tower, Congo River | potholes, sand |
| Johannesburg | white Quantum minibus taxi | queue marshal | "Bree! Bree!", "Sho't left!" | Hillbrow Tower, Ponte, mine dumps | potholes |

**Welcome words:** Akwaaba (Accra), Dalal ak jamm (Dakar), Marhaba (Marrakech), Ahlan (Cairo), Selam (Addis Ababa), Karibu (Nairobi), Murakaza neza (Kigali), Boyei malamu (Kinshasa), Sawubona (Johannesburg).

**Kept out on purpose:** slurs and edgy slang (for example kwasia, toubab, ferenji, chokora, karao), scam and crime terms (sakawa, "Ketch" taxis, kuluna), portraits of religious leaders, and anything political: protests, borders, ethnic conflicts, the Rwandan genocide, taxi violence.

**Sources:** Wikipedia (Tro tro, Ndiaga Ndiaye, Sunu BRT, Taxis of Morocco, Weyala, Transport in Addis Ababa, Matatu, Kigali Convention Centre, Limete Tower), Ghana News Agency (Okada legalisation, Dec 2025), Kenyanism ("Beba beba, tao"), Citizen Digital (matatu graffiti, 2026), Kigali Newcomers (moto taxis), 7sur7.cd (Ketch taxi ban), The Citizen (Joburg taxi hand signs).
