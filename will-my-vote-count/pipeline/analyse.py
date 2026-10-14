"""Tag fear themes and tone for YouTube comments (2025 to 2026) and the 2023 tweet baseline.

Outputs (data/):
  comments_tagged.csv   one row per relevant comment, themes as 0/1 columns, tone score
  theme_summary.csv     theme share 2025-26 against the 2023 baseline, with tone
  theme_month.csv       relevant comments and theme counts by month
"""
import hashlib, html, json, re, sys
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sys.path.insert(0, './scripts')
from themes import THEMES, tag, LABEL, STEP, ELECTION_WORDS, PRE_ELECTION_COURT_VIDEOS

NG = './'

# 1. YouTube comments
yt = pd.read_csv(NG + 'data/comments_raw.csv')
extra = json.load(open(NG + 'raw/youtube_vidiq_WIsZmOVRMHg/comments_anon.json'))
rows = []
for c in extra['comments']:
    for r in [c] + c.get('replies', []):
        rows.append(dict(comment_id_hash=hashlib.sha1(('WIsZmOVRMHg' + r['published_at'] + r['text']).encode()).hexdigest(),
                         video_id='WIsZmOVRMHg', video_title=c['video_title'], channel_title='Channels Television',
                         published_utc=r['published_at'], like_count=r.get('likes', 0), is_reply=r is not c,
                         source='video_comments', text=r['text']))
yt = pd.concat([yt, pd.DataFrame(rows)], ignore_index=True)
yt['text'] = yt.text.astype(str).map(html.unescape).str.replace(r'<[^>]+>', ' ', regex=True).str.replace(r'@[\w.\-]+', '@user', regex=True).str.strip()
yt['platform'] = 'YouTube'
# 1b. X, Facebook and Nairaland comments read in a logged-in browser (no names stored), when collected
import os
SOC = NG + 'data/social_raw.csv'
if os.path.exists(SOC):
    so = pd.read_csv(SOC).dropna(subset=['text'])
    plat = {'x': 'X', 'facebook': 'Facebook', 'nairaland': 'Nairaland', 'instagram': 'Instagram'}
    so['platform'] = so.platform.str.lower().map(plat).fillna(so.platform)
    # Keyword searches ("X search: rig 2027") pull in posts because they match a theme, so they are kept for browsing but left out of the headline shares.
    so['searched'] = so.source.fillna('').str.contains('search', case=False)
    so = so.assign(video_id=so.platform.str.lower() + ':' + so.source.fillna('search').astype(str).str.slice(0, 60),
                   video_title=so.post_title, channel_title=so.platform + ': ' + so.source.fillna('search').astype(str),
                   published_utc=so.published, like_count=0, is_reply=True, source='social')
    yt['searched'] = False
    yt = pd.concat([yt, so[['comment_id_hash', 'video_id', 'video_title', 'channel_title', 'published_utc', 'like_count', 'is_reply', 'source', 'text', 'platform', 'searched']]], ignore_index=True)
    yt['text'] = yt.text.astype(str).str.replace(r'@[\w.\-]+', '@user', regex=True).str.replace(r'https?://\S+', ' ', regex=True).str.strip()
yt = yt.drop_duplicates(['text', 'published_utc'])
yt['date'] = pd.to_datetime(yt.published_utc, utc=True, errors='coerce', format='mixed')
yt = yt[yt.date.notna() & (yt.date >= '2025-01-01')]
yt['dataset'] = '2025-26 online'
yt.to_csv(NG + 'data/comments_all.csv', index=False)

# 2. 2023 tweet baseline (election aftermath, 26 Feb to 14 Mar 2023)
tw = pd.read_csv(NG + 'raw/kaggle_ahamefulechijoke__twitter-data-nigerian-2023-presidential-election/tweets_anon.csv')
tw = tw.rename(columns={'likes': 'like_count'})
tw['text'] = tw.text.astype(str).str.replace(r'https?://\S+', ' ', regex=True).str.replace(r'@\w+', '@user', regex=True).str.strip()
tw = tw.drop_duplicates('text')
tw['date'] = pd.to_datetime(tw['date'], utc=True)
tw['dataset'] = '2023 X (Twitter)'
tw['channel_title'] = 'X'

# 3. Tone: VADER with a small Nigerian English and Pidgin lexicon added
sia = SentimentIntensityAnalyzer()
sia.lexicon.update({
    'rig': -2.5, 'rigged': -2.8, 'rigging': -2.8, 'thugs': -2.5, 'thuggery': -2.8, 'wahala': -1.8, 'yeye': -1.8,
    'ole': -2.2, 'thief': -2.6, 'thieves': -2.6, 'fraud': -2.8, 'compromised': -2.2, 'useless': -2.2, 'shameless': -2.4,
    'japa': -0.8, 'suffer': -2.0, 'suffering': -2.2, 'hunger': -2.0, 'scam': -2.6, 'biased': -1.8, 'bias': -1.6,
    'credible': 1.8, 'transparent': 1.8, 'transparency': 1.5, 'kudos': 2.2, 'well done': 2.0, 'weldone': 2.0,
    'hope': 1.2, 'peaceful': 1.8, 'free and fair': 2.2, 'god bless': 1.8,
})
def tone(t):
    return sia.polarity_scores(t)['compound']

ids = [t[0] for t in THEMES]
out = []
for df in (yt, tw):
    df = df.copy()
    df['themes'] = df.text.map(tag)
    df['election_related'] = df.text.str.contains(ELECTION_WORDS)
    df['relevant'] = df.themes.str.len() > 0
    df['tone'] = df.text.map(tone)
    # Distrust of INEC: an explicit pattern, or INEC and its leaders named in a clearly negative comment (tone -0.3 or lower).
    inec_named = df.text.str.contains(r'\b(?:inec|amupitan|yakubu)\b', case=False, regex=True)
    add = inec_named & (df.tone <= -0.3) & ~df.themes.map(lambda l: 'inec_trust' in l)
    df.loc[add, 'themes'] = df.loc[add, 'themes'].map(lambda l: l + ['inec_trust'])
    if 'video_id' in df:
        pre = df.video_id.isin(PRE_ELECTION_COURT_VIDEOS) & df.themes.map(lambda l: 'courts' in l)
        df.loc[pre, 'themes'] = df.loc[pre, 'themes'].map(lambda l: [('court_pre' if x == 'courts' else x) for x in l])
    df['relevant'] = df.themes.str.len() > 0
    for i in ids:
        df[i] = df.themes.map(lambda l, i=i: int(i in l))
    out.append(df)
yt, tw = out

cols = ['comment_id_hash', 'dataset', 'platform', 'searched', 'channel_title', 'video_id', 'date', 'like_count', 'tone', 'text'] + ids
ytr = yt[yt.relevant]
ytr.assign(comment_id_hash=ytr.comment_id_hash)[cols].to_csv(NG + 'data/comments_tagged.csv', index=False)
twr = tw[tw.relevant]

def summary(df, name):
    n = len(df)
    s = pd.DataFrame({'theme': ids,
                      'label': [LABEL[i] for i in ids],
                      'process_step': [STEP[i] for i in ids],
                      f'{name}_comments': [int(df[i].sum()) for i in ids]})
    s[f'{name}_share'] = s[f'{name}_comments'] / n
    s[f'{name}_tone'] = [round(df.loc[df[i] == 1, 'tone'].mean(), 3) if df[i].sum() else None for i in ids]
    s[f'{name}_negative_share'] = [round((df.loc[df[i] == 1, 'tone'] <= -0.05).mean(), 3) if df[i].sum() else None for i in ids]
    return s

yth = ytr[~ytr.searched.astype(bool)]  # headline shares: comments under posts and videos, not keyword searches
s = summary(yth, 'now').merge(summary(twr, 'y2023')[['theme', 'y2023_comments', 'y2023_share', 'y2023_tone']], on='theme')
s['change_pts'] = (s.now_share - s.y2023_share) * 100
# The 2023 tweets were collected by searching for INEC, so every one names INEC: the distrust share is not comparable.
s.loc[s.theme == 'inec_trust', ['y2023_share', 'y2023_tone', 'change_pts']] = None
s['videos_with_theme'] = [int(ytr.loc[ytr[i] == 1, 'video_id'].nunique()) for i in s.theme]
s['videos_total'] = int(ytr.video_id.nunique())
s['top_video_share'] = [round(ytr.loc[ytr[i] == 1, 'video_id'].value_counts(normalize=True).iloc[0], 3) if ytr[i].sum() else None for i in s.theme]
s = s.sort_values('now_share', ascending=False)
s.to_csv(NG + 'data/theme_summary.csv', index=False)

m = ytr.assign(month=ytr.date.dt.strftime('%Y-%m')).groupby('month')[ids].sum()
m.insert(0, 'relevant_comments', ytr.assign(month=ytr.date.dt.strftime('%Y-%m')).groupby('month').size())
m['tone'] = ytr.assign(month=ytr.date.dt.strftime('%Y-%m')).groupby('month').tone.mean().round(3)
m.to_csv(NG + 'data/theme_month.csv')

print('YouTube comments', len(yt), 'election-related', int(yt.election_related.sum()), 'relevant (tagged)', len(ytr))
print('2023 tweets', len(tw), 'relevant', len(twr))
print('negative share now', round((ytr.tone <= -0.05).mean(), 3), 'positive', round((ytr.tone >= 0.05).mean(), 3))
print('negative share 2023', round((twr.tone <= -0.05).mean(), 3))
print(s[['label', 'now_comments', 'now_share', 'now_tone', 'videos_with_theme', 'top_video_share', 'y2023_share']].round(3).to_string(index=False))
print(m[['relevant_comments', 'tone']].to_string())

# Process step view: share of fear comments that touch each INEC step (a comment can touch several).
steps = {}
for i in ids:
    steps.setdefault(STEP[i], []).append(i)
st = pd.DataFrame([(k, int((yth[v].sum(axis=1) > 0).sum())) for k, v in steps.items()], columns=['process_step', 'comments'])
st['share'] = (st.comments / len(yth)).round(4)
st = st.sort_values('process_step')
st.to_csv(NG + 'data/step_summary.csv', index=False)
back = (yth[[i for i in ids if STEP[i][:1] in '567']].sum(axis=1) > 0).mean()
print(st.to_string(index=False)); print('back end (upload, collation, courts) share', round(back, 3), 'headline comments', len(yth), 'of', len(ytr), 'sources', ytr.video_id.nunique())
print(ytr.groupby('platform').size().to_string())
