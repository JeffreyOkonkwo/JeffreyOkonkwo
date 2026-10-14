"""Delivery metrics for the three WiredTiger storage-engine teams, April 2025 to October 2026.
Reconstructs sprint membership from the Jira changelog so commitment is measured at sprint start, not at the end."""
import pandas as pd, numpy as np, bisect
pd.options.mode.chained_assignment = None
I = pd.read_csv('data_issues.csv'); S = pd.read_csv('data_sprints.csv'); T = pd.read_csv('data_transitions.csv'); M = pd.read_csv('data_membership.csv', dtype=str).fillna('')
for c in ('created', 'resolved'): I[c] = pd.to_datetime(I[c], utc=True)
T['at'] = pd.to_datetime(T['at'], utc=True); M['at'] = pd.to_datetime(M['at'], utc=True)
TEAMS = ['SE Foundations', 'SE Persistence', 'SE Transactions']
S['team'] = S.name.str.extract(r'^(SE Transactions|SE Foundations|SE Persistence) - \d')[0]
S['start'] = pd.to_datetime(S.activatedDate.fillna(S.startDate), utc=True, format='ISO8601'); S['end'] = pd.to_datetime(S.completeDate, utc=True, format='ISO8601')
SP = S[(S.state == 'CLOSED') & S.team.notna() & (S.start >= '2025-04-01')].copy()
SP['days'] = (SP.end - SP.start).dt.total_seconds() / 86400
SP = SP[SP.days >= 7].sort_values(['team', 'start']).reset_index(drop=True)   # drop zero-length/aborted sprints
SP['id'] = SP['id'].astype(str)
DONE = {'Closed', 'Resolved'}

# status timeline per issue
TL = {k: g.sort_values('at')[['at', 'frm', 'to']].values.tolist() for k, g in T.groupby('key')}
def done_at(key, t):
    st = None
    for at, frm, to in TL.get(key, []):
        if at <= t: st = to
        else:
            if st is None: st = frm
            break
    return st in DONE
def first_done(key):
    """time of the LAST move into a done state (final resolution)"""
    x = [at for at, frm, to in TL.get(key, []) if to in DONE]
    return x[-1] if x else pd.NaT

# sprint membership timeline per issue
ME = {k: g.sort_values('at')[['at', 'frm_id', 'to_id']].values.tolist() for k, g in M.groupby('key')}
CUR = dict(zip(I.key, I.sprint_ids.fillna('').astype(str)))
CRE = dict(zip(I.key, I.created))
def ids(s): return set(x.strip() for x in str(s).split(',') if x.strip()) if s else set()
def members_at(key, t):
    if t < CRE[key]: return set()
    ev = ME.get(key)
    if not ev: return set(CUR[key].split('|')) - {''}
    if t < ev[0][0]: return ids(ev[0][1])
    cur = set()
    for at, frm, to in ev:
        if at <= t: cur = ids(to)
        else: break
    return cur

GRACE = pd.Timedelta(hours=2)
rows, items = [], []
for _, s in SP.iterrows():
    sid = s['id']
    cand = [k for k, v in CUR.items() if sid in v.split('|')] + [k for k, g in M.groupby('key') if g.frm_id.str.contains(rf'(^|,\s*){sid}(,|$)').any() or g.to_id.str.contains(rf'(^|,\s*){sid}(,|$)').any()]
    cand = sorted(set(cand))
    for k in cand:
        at_start = sid in members_at(k, s.start + GRACE)
        at_end = sid in members_at(k, s.end - pd.Timedelta(seconds=1))
        ever = at_start or at_end or any(sid in ids(to) for at, frm, to in ME.get(k, []) if s.start < at < s.end)
        if not ever: continue
        if not at_start and not at_end and not ME.get(k): continue
        done_end = done_at(k, s.end)
        done_start = done_at(k, s.start)
        if done_start: continue   # already finished before the sprint, ignore
        fd = first_done(k)
        completed = done_end and at_end
        # an item completed inside the sprint and then removed by tooling still counts as done in sprint
        if done_end and not at_end and pd.notna(fd) and s.start <= fd <= s.end and sid in members_at(k, fd - pd.Timedelta(seconds=1)): completed = True
        pts = I.loc[I.key == k, 'points'].iloc[0]
        items.append(dict(sprint_id=sid, team=s.team, sprint=s['name'], key=k, committed=at_start, added=not at_start,
                          completed=completed, carried=(at_end and not done_end), removed=(at_start and not at_end and not completed), points=pts))
IT = pd.DataFrame(items)
for _, s in SP.iterrows():
    g = IT[IT.sprint_id == s['id']]; c = g[g.committed]
    rows.append(dict(team=s.team, sprint=s['name'], sprint_id=s['id'], start=s.start.date(), end=s.end.date(), days=round(s.days, 1),
                     committed=len(c), committed_done=int(c.completed.sum()), added=int(g.added.sum()), added_done=int(g[g.added].completed.sum()),
                     total_done=int(g.completed.sum()), carried_over=int(g.carried.sum()), removed=int(g.removed.sum()),
                     committed_pts=c.points.sum(), committed_pts_done=c[c.completed].points.sum(), goal=(s.goal if isinstance(s.goal, str) else '')))
SC = pd.DataFrame(rows)
SC['say_do'] = (SC.committed_done / SC.committed.replace(0, np.nan)).round(3)
SC['scope_added_pct'] = (SC.added / SC.committed.replace(0, np.nan)).round(3)
SC['carry_over_pct'] = (SC.carried_over / (SC.committed + SC.added).replace(0, np.nan)).round(3)
SC['sprint_no'] = SC.groupby('team').cumcount() + 1
SC.to_csv('out_sprint_scorecard.csv', index=False); IT.to_csv('out_sprint_items.csv', index=False)

# flow: cycle time, time in status, team of each issue (team of last sprint it sat in)
team_of = IT.sort_values('sprint_id').groupby('key').team.last()
flow = []
ACTIVE = {'In Progress', 'Investigating'}; WAIT = {'In Code Review', 'Blocked', 'Needs Scheduling', 'Open', 'Backlog', 'Waiting For User Input'}
for k, tl in TL.items():
    if k not in team_of.index: continue
    starts = [at for at, frm, to in tl if to in ACTIVE]
    fd = first_done(k)
    if not starts or pd.isna(fd): continue
    s0 = starts[0]
    if fd <= s0: continue
    dur = {}
    for (at, frm, to), nxt in zip(tl, tl[1:] + [[fd, None, None]]):
        if at < s0 or at >= fd: continue
        dur[to] = dur.get(to, 0) + (min(nxt[0], fd) - at).total_seconds() / 86400
    flow.append(dict(key=k, team=team_of[k], started=s0, done=fd, cycle_days=(fd - s0).total_seconds() / 86400,
                     in_progress_days=sum(v for kk, v in dur.items() if kk in ACTIVE), code_review_days=dur.get('In Code Review', 0),
                     blocked_days=dur.get('Blocked', 0), other_wait_days=sum(v for kk, v in dur.items() if kk in WAIT - {'In Code Review', 'Blocked'})))
FL = pd.DataFrame(flow)
FL = FL[(FL.done >= '2025-04-01')].merge(I[['key', 'type', 'priority', 'points']], on='key')
FL['flow_eff'] = (FL.in_progress_days / FL.cycle_days).clip(0, 1)
FL.to_csv('out_flow_items.csv', index=False)

# weekly throughput per team
FL['week'] = FL.done.dt.tz_convert(None).dt.to_period('W-SUN').dt.start_time
TP = FL.groupby(['team', 'week']).size().rename('done').reset_index(); TP.to_csv('out_throughput_weekly.csv', index=False)

# daily CFD per team (status category per day)
CAT = {'Backlog': 'To do', 'Needs Scheduling': 'To do', 'Open': 'To do', 'Needs Verification': 'To do', 'Ready for Work': 'To do',
       'In Progress': 'In progress', 'Investigating': 'In progress', 'Blocked': 'Blocked', 'In Code Review': 'In review',
       'Waiting For User Input': 'Blocked', 'Closed': 'Done', 'Resolved': 'Done'}
days = pd.date_range('2025-04-01', '2026-10-12', freq='D', tz='UTC')
cfd = []
for k in team_of.index:
    tl = TL.get(k, []); cr = CRE[k]
    for d in days[::7]:
        if d < cr: continue
        st = 'Open'
        for at, frm, to in tl:
            if at <= d: st = to
            else: break
        cfd.append((team_of[k], d.date(), CAT.get(st, 'To do')))
CF = pd.DataFrame(cfd, columns=['team', 'date', 'stage']).groupby(['team', 'date', 'stage']).size().rename('items').reset_index()
CF.to_csv('out_cfd_weekly.csv', index=False)

# headline numbers
def q(x, p): return float(np.nanpercentile(x, p))
H = {}
for t in TEAMS + ['All']:
    sc = SC if t == 'All' else SC[SC.team == t]; fl = FL if t == 'All' else FL[FL.team == t]
    H[t] = dict(sprints=len(sc), committed=int(sc.committed.sum()), say_do=round(sc.committed_done.sum() / sc.committed.sum(), 3),
                median_sprint_say_do=round(sc.say_do.median(), 3), added=int(sc.added.sum()), added_pct=round(sc.added.sum() / sc.committed.sum(), 3),
                carried=int(sc.carried_over.sum()), items_done=len(fl), cycle_p50=round(q(fl.cycle_days, 50), 1), cycle_p85=round(q(fl.cycle_days, 85), 1),
                review_share=round(fl.code_review_days.sum() / fl.cycle_days.sum(), 3), blocked_share=round(fl.blocked_days.sum() / fl.cycle_days.sum(), 3),
                flow_eff=round(fl.in_progress_days.sum() / fl.cycle_days.sum(), 3), review_p50=round(q(fl.code_review_days, 50), 1),
                weekly_tp_p50=float(TP[TP.team == t].done.median()) if t != 'All' else float(TP.groupby('week').done.sum().median()))
H = pd.DataFrame(H).T; H.to_csv('out_headlines.csv'); print(H.to_string())
print(SC.groupby('team')[['say_do', 'scope_added_pct', 'carry_over_pct']].describe().round(2).T.to_string())
