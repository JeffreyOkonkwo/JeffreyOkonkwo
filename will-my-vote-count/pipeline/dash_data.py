"""Write the dashboard datasets (no comment text except a few short quotes)."""
import pandas as pd, sys
sys.path.insert(0, './scripts')
from themes import THEMES, LABEL, STEP
NG = './'; OUT = NG + 'dash/data/'
ids = [t[0] for t in THEMES]

c = pd.read_csv(NG + 'data/comments_tagged.csv', parse_dates=['date'])
c['month'] = c.date.dt.strftime('%Y-%m')
c['tone'] = c.tone.round(3)
c['searched'] = c.searched.astype(bool).astype(int)
c[['comment_id_hash', 'month', 'platform', 'searched', 'channel_title', 'video_id', 'tone'] + ids].rename(columns={'comment_id_hash': 'id', 'channel_title': 'channel'}).to_csv(OUT + 'fears.csv', index=False)

# corpus: every comment read, by video (relevant or not), so the page can say how many were read
raw = pd.read_csv(NG + 'data/comments_all.csv')
v = pd.read_csv(NG + 'data/videos.csv')
read = raw.groupby('video_id').size().rename('comments_read')
corp = v.set_index('video_id').join(read, how='outer')
corp.loc['WIsZmOVRMHg', ['title', 'channel', 'published', 'comments_read']] = ['2027: Why INEC Cannot Transmit Results Electronically', 'Channels Television', '2026-02-09', 107]
corp['fear_comments'] = c.groupby('video_id').size()
corp = corp.reset_index().rename(columns={'index': 'video_id'})
soc = raw[raw.platform != 'YouTube'].groupby('video_id').agg(channel=('channel_title', 'first'), title=('video_title', 'first'), platform=('platform', 'first'))
for vid, r in soc.iterrows():
    corp.loc[vid, ['channel', 'title']] = [r.channel, r.title if isinstance(r.title, str) else r.channel]
corp['platform'] = ['YouTube' if not str(i).split(':')[0] in ('x', 'facebook', 'nairaland', 'instagram') else {'x': 'X', 'facebook': 'Facebook', 'nairaland': 'Nairaland', 'instagram': 'Instagram'}[str(i).split(':')[0]] for i in corp.index]
corp['channel'] = corp.channel.fillna('Other channels (comment index)')
corp['fear_comments'] = corp.fear_comments.fillna(0).astype(int)
corp['comments_read'] = corp.comments_read.fillna(0).astype(int)
corp = corp[corp.comments_read > 0]
corp[['video_id', 'platform', 'channel', 'title', 'published', 'comments_read', 'fear_comments']].to_csv(OUT + 'videos.csv', index=False)
print('read', corp.comments_read.sum(), 'videos', len(corp), 'fear', corp.fear_comments.sum())

# themes reference, with the 2023 baseline share
s = pd.read_csv(NG + 'data/theme_summary.csv')
s[['theme', 'label', 'process_step', 'y2023_share']].assign(y2023_share=s.y2023_share.round(4)).to_csv(OUT + 'themes.csv', index=False)

pu = pd.read_csv(NG + 'data/pu_2023_by_state.csv')
pu = pu.rename(columns={'state_name': 'state', 'Polling units': 'polling_units', 'Readable result sheet': 'readable', 'Never uploaded': 'never_uploaded',
                        'Unreadable upload': 'unreadable', 'Wrong document': 'wrong_document', 'Cancelled or no election': 'cancelled', 'Missing signature or stamp': 'missing_signature_or_stamp'})
pu[['state', 'polling_units', 'readable', 'never_uploaded', 'unreadable', 'wrong_document', 'cancelled', 'missing_signature_or_stamp']].to_csv(OUT + 'results_2023.csv', index=False)

pd.read_csv(NG + 'data/fixes.csv').to_csv(OUT + 'fixes.csv', index=False)
