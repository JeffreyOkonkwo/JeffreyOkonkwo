# Data sources for the Nigeria 2027 election and INEC sentiment project

Tested on 10 October 2026 from this cloud environment. Every result below comes from a live test, not from memory. All downloaded content was treated as untrusted data and parsed only with isolated scripts kept outside the download folders.

Anonymisation rule applied throughout: no author handles, display names or channel URLs of commenters are stored. Where a source returned handles (YouTube comments via vidIQ, the Kaggle tweet sets), the handle-bearing originals were dropped or deleted and only text, date and engagement counts were kept. Tweet text can still contain @mentions inside the body; these must be masked in the cleaning step.

## Summary table

| # | Source | Works here? | Method that worked | Volume achievable | Main constraint |
|---|---|---|---|---|---|
| 1a | YouTube comments, per video (vidIQ `vidiq_video_comments`) | Yes | vidIQ connector | Up to 100 threads plus replies per call; 110 credits left this cycle (about 22 calls), 150 per month after 28 Oct | 5 credits per call; credits are the bottleneck |
| 1b | YouTube comment index (vidIQ `vidiq_comment_insights`, raw mode) | Yes | vidIQ connector | 7,242 matched comments for one niche query; up to 1,000 threads per 5 credits (later pages free) | Only liked, indexed comments; few channels; relevance-ranked |
| 1c | YouTube Data API v3 (direct) | Reachable, needs key | curl to googleapis.com | Free quota 10,000 units per day; 1 unit per 100 comments | Needs a free Google Cloud API key from Jeffrey |
| 2 | Reddit r/Nigeria, r/NigeriaPolitics | No | (none) | 0 | Reddit returns its own "Blocked" page (403); WebFetch needs per-URL user approval |
| 3 | Nairaland politics | No | (none) | 0 | Cloudflare "Just a moment" challenge (403) |
| 4a | GDELT DOC API (tone timeline, article list) | No (rate-limited) | (none) | 0 | 429 on every attempt, even after 45 s; the shared egress IP is already over GDELT's limit |
| 4b | GDELT bulk GKG files (data.gdeltproject.org) | Yes | curl | One file every 15 minutes, about 670 articles each, with a tone score per article | News tone, not public opinion; no article text; Nigeria share is small |
| 5 | Google News RSS | Yes | curl | 100 items per query; date windows with `after:`/`before:` work (47 items for January 2025 alone) | Headlines and source names only, no body text; news framing, not public voice |
| 6 | X / Twitter API | No | (none) | 0 | 401 without a paid API token |
| 7a | Kaggle 2023 election tweet sets | Yes | Kaggle public API (anonymous list and download) | 10,000 tweets (26 Feb to 14 Mar 2023) plus 8,183 tweets (16 to 24 Jul 2023) | Licences listed as "Unknown" or CC0; one CC0 set is now an empty archive |
| 7b | INEC PVC and registered-voter data | Yes | curl to inecnigeria.org | Certified polling-unit PVC PDFs (Osun 2026: 83 pages; also Bayelsa, Imo, Kogi 2023) | PDF tables, need extraction; context data, not text |
| 7c | GitHub | Partly | raw.githubusercontent.com works; github.com pages and GitHub search API do not | Only files whose exact path is already known | Search blocked in this session (repo-scoped token) |
| 8 | News-site reader comments (Punch, Premium Times) | No | (none) | 0 | Punch article shows no comment system; Premium Times loads Insticator by JavaScript, not in HTML |

WebFetch note: every WebFetch request (Reddit, old.reddit, Nairaland, GDELT, Google News) failed with "permission request not answered in time". WebFetch in this setup needs Jeffrey to approve each URL, so it cannot be relied on for unattended collection. All working results above came from the shell (curl) or the vidIQ connector.

## 1. YouTube comments through vidIQ

**Credit costs (checked with `vidiq_balance`, which is free):** balance was 140 credits at the start (plan cap 150, renews 28 October 2026). `vidiq_youtube_search` costs 5 credits per call. `vidiq_video_comments` costs 5 credits per call. `vidiq_comment_insights` costs 5 credits per new search; later cursor pages are free. `vidiq_job_poll` is free. This test spent 30 credits (2 searches, 3 comment pulls, 1 comment-index search). Balance now: 110.

**Search test.** Query "INEC 2027 election electronic transmission", videos only, published after 1 January 2025, region NG, 25 results. Channels found include Channels Television, Arise News, TVC News Nigeria, News Central TV and several commentator channels. 14 of the 25 videos had zero comments. Comment volume clusters on a few videos: Channels Television (107 comments), Dr. Omoshola Deji (73), News Central TV (10). A second search scoped to the Channels Television channel with a multi-term query ("INEC PVC vote buying 2027") returned only one video, so channel-scoped searches should use short, single-topic queries. Sahara Reporters, Punch, BBC News Pidgin and Legit TV were not separately searched in this test to save credits; they should be searched by channel in the collection run.

**Comment pull test (three videos, `maxResult` 100, newest first):**

| Video | Channel | Threads | Replies | Date span | Pages left |
|---|---|---|---|---|---|
| WIsZmOVRMHg | Channels Television | 77 | 30 | 6 to 9 Feb 2026 | none |
| uAIXBf_c8bM | Dr. Omoshola Deji | 64 | 9 | 4 to 5 Feb 2026 | none |
| ZqUTuvr8H_k | Landslide News | 7 | 2 | 8 to 9 Oct 2026 | none |

One call returned every comment on each video. Fields returned: author handle, author channel URL, text (HTML-escaped, with `<br>` tags), like count, published date and time (UTC), reply list with the same fields, video ID and title. Dates are included for every comment and every reply. Handles were removed before saving.

Many comments on a news video are off-topic (for example, kidnapping in Kaduna under a video about result transmission), so a relevance filter is required. The language is mostly English with some Nigerian Pidgin ("He be like say ogun won't kill ineec", "Dey play").

**Comment index test (`vidiq_comment_insights`, raw mode).** Niche "Nigerian politics and elections news", comments from 1 January 2025 onward. Result: 176 qualified channels, 5 channels with matching comments, 7,242 comments matched, about 12 threads per page. Fields: comment ID, video ID, channel ID, date, like count, an LLM "intent" hint and text. No author handle is returned, which suits the anonymisation rule. Limits: only comments that the index already holds (low-like comments are excluded), relevance-ranked rather than random, script-level language filter only, many comments are about Nigerian politics in general rather than INEC. Traversal is capped at 1,000 threads or 100 pages per search, and the cursor expires after one hour. Each page is about 10,000 tokens, so paging to 1,000 threads is cheap in credits but slow to page through.

**Terms of use.** vidIQ returns data from the YouTube API, so YouTube API Services Terms apply: display and analyse, do not redistribute raw comments in bulk, delete data on request, refresh or delete stored data within 30 days if it is used in a public app. For a portfolio, publish only aggregates and a small number of paraphrased or short quoted examples without names.

**Saved samples:**
- `raw/youtube_vidiq_WIsZmOVRMHg/comments_anon.json` (all 107 comments, anonymised by script)
- `raw/youtube_vidiq_ZqUTuvr8H_k/comments_anon.json` (all 9 comments)
- `raw/youtube_vidiq_uAIXBf_c8bM/comments_anon_excerpt.json` (12 of 73, hand-transcribed excerpt because that tool output was not saved to disk)
- `raw/youtube_vidiq_comment_insights_raw/page1.json` (12 threads plus coverage numbers)
- `raw/youtube_vidiq_search_2026-10-10/search_results.json` (video list with comment counts)

**YouTube Data API v3 directly.** `googleapis.com` is reachable from the shell. The 403 response says "Method does not allow unregistered callers ... Please use API Key". With a free API key the default quota is 10,000 units per day, and `commentThreads.list` costs 1 unit for up to 100 comments. That is far cheaper than vidIQ credits. This is the best upgrade path if Jeffrey is willing to create a key.

## 2. Reddit

- `curl https://www.reddit.com/r/Nigeria/search.json?q=INEC&restrict_sr=1` returned 403 with Reddit's own "Blocked" page.
- `old.reddit.com` search returned a 302 redirect to the blocked path.
- `oauth.reddit.com` returned 403 without a token.
- WebFetch on both URLs failed for lack of user approval.

Conclusion: not available from this environment. Reddit's Data API terms now require registration and OAuth, and commercial or large-scale use needs approval. No workaround was attempted.

## 3. Nairaland

`curl https://www.nairaland.com/politics` returned 403 with a Cloudflare "Just a moment..." challenge page. WebFetch failed for lack of approval. Not available. Bypassing a bot challenge would breach the site's intent, so it is excluded.

## 4. GDELT

- DOC 2.0 API (`api.gdeltproject.org/api/v2/doc/doc`, article list and tone timeline): 429 on four attempts spaced 6 to 45 seconds apart. The message reads "Please limit requests to one every 5 seconds". Because even the first call failed, the shared outbound IP of this environment is already over the limit. Treat it as unavailable from here; it may work from Jeffrey's own computer.
- Bulk files (`data.gdeltproject.org/gdeltv2/lastupdate.txt` and the 15-minute GKG zip): work. One GKG file had 669 article records with source domain, URL, themes, locations, organisations and a tone vector (average tone, positive, negative). Very few records per file are about Nigeria, so a usable Nigerian tone series needs many files (96 per day). This measures how the press frames INEC, not what citizens say, and contains no article text.
- Terms: GDELT is free and open for research with citation.

Saved: `raw/gdelt/` (the 429 responses), `raw/gdelt_gkg_sample/` (one GKG file).

## 5. Google News RSS

`curl` works. Saved in `raw/google_news_rss/`:
- "INEC 2027", Nigeria edition: 100 items, newest dated 10 October 2026.
- "vote buying" Nigeria, last 30 days: 59 items.
- "INEC" with `after:2025-01-01 before:2025-02-01`: 47 items, so historical monthly windows work.

Fields: headline (with source name appended), Google redirect link, publication date, source name. No article body. Example headlines: "2027: INEC displays voter register, begins PVC distribution" (Punch), "2027: ADC defies INEC warning, vows to publish polling-unit results" (Vanguard). About 100 items per query per window, so 20 months times 5 topics gives roughly 5,000 to 10,000 headlines. Use for an event timeline and a "media versus public" comparison, not as public opinion. Google News terms allow personal feed reading; do not republish the feed.

## 6. X / Twitter

`api.twitter.com/2/tweets/search/recent` returned 401 Unauthorized. Search needs a paid API tier. Not available. Scraping X is against its terms and is excluded.

## 7. Public datasets

**Kaggle.** The anonymous listing API (`kaggle.com/api/v1/datasets/list`) works, and downloads work without a key through a signed Google Storage redirect. Results:
- `gpreda/nigerian-presidential-election-2023-tweets` (CC0): the archive is now empty (22 bytes).
- `ahamefulechijoke/twitter-data-nigerian-2023-presidential-election` (licence "Unknown"): 10,000 tweets, 26 February to 14 March 2023, with date, text, likes, retweets, plus the uploader's own TextBlob polarity labels. Saved anonymised as `raw/kaggle_ahamefulechijoke__.../tweets_anon.csv`.
- `alfredgichuhi/nigerian-pres-candidates-tweets-after-elections` (CC0): 8,183 tweets in tables per party or candidate, 16 to 24 July 2023. Saved anonymised as `raw/kaggle_alfredgichuhi__.../tweets_anon.csv`.
- Others listed but not downloaded: `kareemrasheed89/nigeriapolitics-tweets5000tweets` (CC0, 2022), `kareemrasheed89/nigeria-politics-peterobi-5000tweets` (Unknown), election results sets for 1999 to 2023.

Originals containing usernames were deleted after anonymisation. Use these only as a 2023 baseline and for training or validating a sentiment model. "Unknown" licence sets are risky to republish; prefer the CC0 one for anything public.

**INEC.** `inecnigeria.org` is reachable. The page `/statistics/pvc` lists certified polling-unit PVC collection PDFs for Bayelsa, Imo, Kogi (2023) and Osun (2026). The Osun 2026 file (83 pages, 841 KB) was downloaded to `raw/inec_pvc_osun_2026/`. The CVR portal (`cvr.inecnigeria.org/pu`) and the IReV result portal (`inecelectionresults.ng`) load, but older guessed paths returned 404 and no open JSON API was found in the site scripts. These are official public records for context (for example, PVC collection rates by state), not text for sentiment.

**GitHub.** `raw.githubusercontent.com` works for a known path. `github.com` pages returned 400 or 403, and the GitHub search API is blocked in this session because the token is bound to the configured repositories. So GitHub datasets can be pulled only when the exact file path is known in advance.

## 8. News-site reader comments

A Punch article page shows no comment system in its HTML. A Premium Times article loads Insticator comments through JavaScript only. Neither is collectable here without driving a browser against a third-party widget, which their terms do not invite. Not available.

## Recommended data plan

**Research question.** How did public YouTube discussion about INEC and the 2027 election change between January 2025 and October 2026, around key events (Electoral Act 2026, Senate vote on electronic transmission in February 2026, election timetable, PVC distribution, off-cycle governorship elections)?

**Target corpus: about 8,000 to 12,000 YouTube comments, plus two context layers.**

| Layer | Source | Target size | Role |
|---|---|---|---|
| Core public text | YouTube comments: vidIQ comment index (raw) plus per-video pulls on high-comment videos | 8,000 to 12,000 comments from 80 to 150 videos across at least 8 channels | Sentiment and topic analysis |
| Optional upgrade | YouTube Data API with Jeffrey's free key | Could raise the corpus to 30,000 or more | Same, larger and less biased toward liked comments |
| Baseline | Kaggle 2023 tweets (CC0 set first) | 8,000 to 18,000 tweets | 2023 comparison and model validation only |
| Event timeline | Google News RSS headlines, monthly windows | 3,000 to 6,000 headlines | Mark events on the chart; media framing |
| Media tone (optional) | GDELT bulk GKG files filtered to Nigeria and INEC | Daily tone series | Compare press tone with public tone |
| Context | INEC PVC PDFs | State or polling-unit figures | Background facts only |

**Date range.** 1 January 2025 to 31 October 2026, with monthly buckets. Expect thin data in early 2025 and spikes in February 2026 and from August 2026 onward.

**Credit budget.** About 110 vidIQ credits remain until 28 October, then 150 per month. Suggested use: 4 comment-index searches with different niches (20 credits; cursor pages are free), 6 to 8 channel-scoped searches (30 to 40 credits), and 10 to 12 per-video pulls on the most-commented videos (50 to 60 credits). This keeps one cycle inside the budget, with the November cycle as reserve. A scheduled weekly top-up (not daily) fits the existing preference for weekly tasks.

**Pipeline rules.** Drop author fields at ingestion. Hash comment IDs. Mask @mentions, phone numbers and account numbers in text. Strip HTML entities. Keep a relevance filter (keywords: INEC, BVAS, IReV, PVC, CVR, transmission, collation, rigging, vote buying, Amupitan, election) and report how many comments it removed. Tag language as English, Pidgin or mixed. Validate the sentiment model on a hand-labelled set of 300 to 500 comments, because off-the-shelf models handle Pidgin and sarcasm poorly.

**Limits to state publicly.**
1. YouTube commenters are not representative of Nigerian voters. They skew urban, younger, online, male and diaspora-heavy, and many comments come from the diaspora.
2. Comments sit under videos chosen by news channels and commentators, and channel audiences lean politically. The mix of channels shapes the result.
3. The vidIQ index favours liked comments and ranks by relevance, so it is not a random sample.
4. English and Nigerian Pidgin only. Hausa, Yoruba, Igbo and other languages are excluded, which under-represents large parts of the north and rural areas.
5. Reddit, Nairaland, X, WhatsApp, Facebook and TikTok, where much Nigerian political talk happens, could not be collected legitimately from this environment.
6. Sentiment toward INEC is mixed with sentiment toward parties, the Senate and candidates; the model measures tone, not voting intention, and should not be read as a poll.
7. Coordinated or partisan accounts and spam may be present and cannot be fully removed.
8. The 2023 Kaggle tweets come from a different platform and period and are a baseline only; some carry an unknown licence.
9. Raw comments will not be redistributed; only aggregates and short anonymised examples will be published, in line with YouTube API terms.
