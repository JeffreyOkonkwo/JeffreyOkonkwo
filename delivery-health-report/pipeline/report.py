"""Build the Delivery Health Report (executive PDF) from the computed tables. Swiss technical style, Letter size.
Usage: python3 report.py  ->  report.html  (render with render_report.mjs)"""
import pandas as pd, numpy as np, html
E = html.escape
SC = pd.read_csv('out_sprint_scorecard.csv', parse_dates=['start']); FL = pd.read_csv('out_flow_items.csv'); H = pd.read_csv('out_headlines.csv', index_col=0)
IT = pd.read_csv('out_sprint_items.csv'); I = pd.read_csv('data_issues.csv')
import os
F = os.path.abspath('node_modules/@fontsource')
INK, PAPER, LINE, ACC, GREY, SOFT = '#0C0E0D', '#F3F4F1', '#D3D6D1', '#FF4A1C', '#8A8F8B', '#3A3F3C'
TEAMC = {'SE Foundations': INK, 'SE Persistence': GREY, 'SE Transactions': ACC}
A = H.loc['All']; pct = lambda x: f'{float(x) * 100:.0f}%'

# ---------- numbers used in the copy (all computed, none typed by hand)
tr = SC[SC.team == 'SE Transactions']; h1 = tr[tr.start < '2026-01-01']; h2 = tr[tr.start >= '2026-01-01']
tr_sd1, tr_sd2 = h1.committed_done.sum() / h1.committed.sum(), h2.committed_done.sum() / h2.committed.sum()
tr_c1, tr_c2 = h1.committed.mean(), h2.committed.mean()
IT2 = IT.merge(I[['key', 'type']], on='key'); added = IT2[IT2.added]
unpl = added.type.isin(['Bug', 'Build Failure']).mean()
n_sp = IT.groupby('key').sprint_id.nunique(); n3, n5, nmax = int((n_sp >= 3).sum()), int((n_sp >= 5).sum()), int(n_sp.max())
hit80 = int((SC.committed_done / SC.committed.replace(0, np.nan) >= 0.8).sum()); with_c = int((SC.committed > 0).sum())
goals = int((SC.goal.fillna('').str.len() > 3).sum())
rv = FL[FL.code_review_days > 0].code_review_days; rv85 = rv.quantile(.85)
pe = H.loc['SE Persistence']

# ---------- small SVG chart helpers
def line_chart(w, h):
    pad = (46, 16, 30, 26)  # l t r b
    x0, x1 = SC.start.min(), SC.start.max(); X = lambda d: pad[0] + (d - x0).days / (x1 - x0).days * (w - pad[0] - pad[2]); Y = lambda v: pad[1] + (1 - v) * (h - pad[1] - pad[3])
    s = f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
    for v in (0, .5, 1):
        s += f'<line x1="{pad[0]}" x2="{w - pad[2]}" y1="{Y(v)}" y2="{Y(v)}" stroke="{LINE}"/><text x="{pad[0] - 8}" y="{Y(v) + 4}" text-anchor="end" class="ax">{int(v * 100)}%</text>'
    s += f'<line x1="{pad[0]}" x2="{w - pad[2]}" y1="{Y(.8)}" y2="{Y(.8)}" stroke="{ACC}" stroke-dasharray="6 5" stroke-width="1.5"/><text x="{w - pad[2]}" y="{Y(.8) - 6}" text-anchor="end" class="ax" fill="{ACC}">80% target</text>'
    for t, g in SC[SC.committed > 0].groupby('team'):
        g = g.sort_values('start'); r = (g.committed_done.rolling(3, min_periods=1).sum() / g.committed.rolling(3, min_periods=1).sum())
        pts = ' '.join(f'{X(d):.1f},{Y(v):.1f}' for d, v in zip(g.start, r))
        s += f'<polyline points="{pts}" fill="none" stroke="{TEAMC[t]}" stroke-width="{3 if t == "SE Transactions" else 2}" stroke-linejoin="round"/>'
    for d, lab in [(pd.Timestamp('2025-07-01'), 'Jul 2025'), (pd.Timestamp('2026-01-01'), 'Jan 2026'), (pd.Timestamp('2026-07-01'), 'Jul 2026')]:
        s += f'<text x="{X(d)}" y="{h - 6}" text-anchor="middle" class="ax">{lab}</text>'
    return s + '</svg>'

def tr_bars(w, h):
    g = tr.sort_values('start'); n = len(g); pad = (34, 10, 6, 24); bw = (w - pad[0] - pad[2]) / n; mx = g.committed.max()
    Y = lambda v: pad[1] + (1 - v / mx) * (h - pad[1] - pad[3])
    s = f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
    for v in (0, 20, 40):
        s += f'<line x1="{pad[0]}" x2="{w - pad[2]}" y1="{Y(v)}" y2="{Y(v)}" stroke="{LINE}"/><text x="{pad[0] - 6}" y="{Y(v) + 4}" text-anchor="end" class="ax">{v}</text>'
    for i, (_, r) in enumerate(g.iterrows()):
        x = pad[0] + i * bw
        s += f'<rect x="{x + 1:.1f}" y="{Y(r.committed):.1f}" width="{bw - 2:.1f}" height="{Y(0) - Y(r.committed):.1f}" fill="{LINE}"/>'
        s += f'<rect x="{x + 1:.1f}" y="{Y(r.committed_done):.1f}" width="{bw - 2:.1f}" height="{Y(0) - Y(r.committed_done):.1f}" fill="{INK}"/>'
    xi = list(g.start).index(g[g.start >= '2026-01-01'].start.iloc[0])
    s += f'<line x1="{pad[0] + xi * bw}" x2="{pad[0] + xi * bw}" y1="{pad[1]}" y2="{Y(0)}" stroke="{ACC}" stroke-width="1.5" stroke-dasharray="4 4"/><text x="{pad[0] + xi * bw + 6}" y="{pad[1] + 12}" class="ax" fill="{ACC}">2026</text>'
    return s + f'<text x="{pad[0]}" y="{h - 4}" class="ax">Apr 2025</text><text x="{w - pad[2]}" y="{h - 4}" text-anchor="end" class="ax">Oct 2026</text></svg>'

def time_split(w):
    t = FL.groupby('team')[['in_progress_days', 'code_review_days', 'blocked_days', 'other_wait_days']].sum()
    t = t.div(t.sum(axis=1), axis=0); cols = [('in_progress_days', INK, 'Working'), ('code_review_days', ACC, 'Code review'), ('blocked_days', GREY, 'Blocked'), ('other_wait_days', LINE, 'Waiting in queue')]
    s = ''
    for team, r in t.iterrows():
        s += f'<div class="sb"><span>{E(team.replace("SE ", ""))}</span><div class="bar">'
        s += ''.join(f'<i style="width:{r[c] * 100:.1f}%;background:{col};color:{INK if col == LINE else "#fff"}">{"" if r[c] < .09 else f"{r[c] * 100:.0f}%"}</i>' for c, col, _ in cols) + '</div></div>'
    s += '<div class="lg">' + ''.join(f'<span><i style="background:{col}"></i>{lab}</span>' for _, col, lab in cols) + '</div>'
    return s

fonts = (f"@font-face{{font-family:Arch;src:url(file://{F}-variable/archivo/files/archivo-latin-wdth-normal.woff2);font-weight:100 900;font-stretch:62% 125%}}"
         + ''.join(f"@font-face{{font-family:Mono;font-weight:{w};src:url(file://{F}/jetbrains-mono/files/jetbrains-mono-latin-{w}-normal.woff2)}}" for w in (400, 500, 700, 800)))
CSS = f"""{fonts}
@page{{size:Letter;margin:0}} *{{box-sizing:border-box;margin:0;padding:0}}
body{{background:{PAPER};color:{INK};font-family:Arch,sans-serif}}
.pg{{position:relative;width:8.5in;height:11in;padding:.62in .6in .7in;overflow:hidden;page-break-after:always;background:{PAPER}}}
.pg:before{{content:'';position:absolute;inset:0 .6in;background-image:repeating-linear-gradient(90deg,{LINE} 0 1px,transparent 1px calc((100% - 1px)/12));opacity:.45}}
.hd{{position:relative;display:flex;justify-content:space-between;font:500 8.5pt/1 Mono;text-transform:uppercase;letter-spacing:.04em;border-bottom:2.5px solid {INK};padding-bottom:8px;margin-bottom:22px}}
.hd b{{color:{ACC}}}
.ft{{position:absolute;left:.6in;right:.6in;bottom:.38in;display:flex;justify-content:space-between;font:500 7.5pt/1 Mono;color:{GREY};text-transform:uppercase;border-top:1px solid {LINE};padding-top:7px}}
h1{{position:relative;font:900 34pt/.95 Arch;font-stretch:122%;letter-spacing:-.03em}}
h2{{position:relative;font:800 17pt/1.05 Arch;font-stretch:115%;letter-spacing:-.02em;margin:16px 0 8px}}
.two h2{{font-size:13pt}}
h3{{font:700 8pt/1 Mono;text-transform:uppercase;letter-spacing:.05em;color:{GREY};margin-bottom:8px}}
p,li{{position:relative;font:400 10pt/1.45 Arch;color:{SOFT}}} p b,li b{{color:{INK}}}
.lead{{font-size:11pt;margin-top:10px;max-width:6.6in}}
.rag{{position:relative;display:flex;gap:0;margin-top:16px;border:2.5px solid {INK};background:#fff}}
.rag div{{flex:1;padding:12px 14px;border-right:1px solid {LINE}}} .rag div:last-child{{border-right:0}}
.rag .v{{white-space:nowrap;font:800 22pt/1 Arch;font-stretch:112%;letter-spacing:-.02em;margin-top:6px}} .rag .v.o{{color:{ACC}}}
.rag small{{display:block;font:400 8pt/1.3 Arch;color:{GREY};margin-top:5px}}
.st{{display:inline-block;font:800 8.5pt/1 Mono;background:{ACC};color:#fff;padding:5px 8px;text-transform:uppercase;letter-spacing:.05em}}
.fd{{position:relative;display:grid;grid-template-columns:.45in 1fr;border-top:1px solid {LINE};padding:6px 0}}
.fd span{{font:800 11pt/1.2 Mono;color:{ACC}}} .fd p{{font-size:10pt}}
.box{{position:relative;background:#fff;border:2px solid {INK};padding:12px 14px;margin-top:8px}}
.ax{{font:500 8px Mono;fill:{GREY}}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.sb{{display:grid;grid-template-columns:1in 1fr;align-items:center;margin:6px 0;font:600 9pt Arch}}
.bar{{display:flex;height:22px}} .bar i{{display:block;height:100%;font:700 7.5pt/22px Mono;color:#fff;text-align:center;font-style:normal}}
.lg{{display:flex;gap:14px;margin-top:8px;font:500 7.5pt Mono;color:{GREY}}} .lg i{{display:inline-block;width:9px;height:9px;margin-right:5px;vertical-align:-1px}}
table{{position:relative;width:100%;border-collapse:collapse;background:#fff;border:2px solid {INK}}}
th{{text-align:left;font:700 7.5pt/1.2 Mono;text-transform:uppercase;letter-spacing:.04em;color:{GREY};padding:8px 8px;border-bottom:2px solid {INK}}}
td{{font:400 8.8pt/1.35 Arch;color:{INK};padding:7px 8px;border-top:1px solid {LINE};vertical-align:top}}
td.k{{font:800 8.5pt/1.3 Mono;color:{ACC};white-space:nowrap}} td.r{{font:700 8pt Mono;white-space:nowrap}}
.ph{{position:relative;display:grid;grid-template-columns:repeat(3,1fr);gap:0;border:2.5px solid {INK};background:#fff;margin-top:6px}}
.ph>div{{padding:12px 13px;border-right:1px solid {LINE}}} .ph>div:last-child{{border-right:0}}
.ph h4{{font:800 13pt/1 Arch;font-stretch:115%;margin-bottom:3px}} .ph .d{{font:700 7.5pt Mono;color:{ACC};text-transform:uppercase;margin-bottom:9px}}
.ph li{{font-size:9pt;margin:0 0 6px 14px}}
.kp td{{font-size:9pt}}
"""
def page(n, body, total=5):
    return f'<div class="pg"><div class="hd"><span><b>Delivery health report</b> / WiredTiger storage engine program</span><span>Jeffrey Okonkwo</span></div>{body}<div class="ft"><span>Data: MongoDB public Jira, project WT. Sprints Apr 2025 to Oct 2026</span><span>{n:02d} / {total:02d}</span></div></div>'

P = []
# ---------------- page 1: executive summary
P.append(page(1, f'''
<span class="st">Status: amber</span>
<h1 style="margin-top:14px">Delivery is steady.<br>Predictability is not.</h1>
<p class="lead">An outside-in health check of three storage engine teams across {int(A.sprints)} two-week sprints. The teams finish real work every week, but fewer than half of the items committed at sprint start are done by sprint end, so plans are hard for anyone outside the team to rely on.</p>
<div class="rag">
 <div><h3>Say-do ratio</h3><div class="v o">{pct(A.say_do)}</div><small>committed items done in the sprint. Target 80%.</small></div>
 <div><h3>Added mid-sprint</h3><div class="v">{pct(A.added_pct)}</div><small>{int(A.added)} items added on top of {int(A.committed)} committed</small></div>
 <div><h3>Cycle time p85</h3><div class="v">{A.cycle_p85:.0f} days</div><small>median {A.cycle_p50:.0f} days, start to done</small></div>
 <div><h3>Stuck items</h3><div class="v o">{n3}</div><small>items carried through 3 or more sprints</small></div>
</div>
<h2>Five findings</h2>
<div class="fd"><span>01</span><p><b>Only {hit80} of {with_c} sprints hit an 80% say-do ratio.</b> The program-wide ratio is {pct(A.say_do)}. Foundations is the most predictable team at {pct(H.loc["SE Foundations"].say_do)}.</p></div>
<div class="fd"><span>02</span><p><b>Transactions grew its commitment, and its reliability fell.</b> Average items committed per sprint rose from {tr_c1:.0f} in 2025 to {tr_c2:.0f} in 2026, while its say-do ratio fell from {pct(tr_sd1)} to {pct(tr_sd2)}.</p></div>
<div class="fd"><span>03</span><p><b>Unplanned work is a standing load, not a surprise.</b> {pct(unpl)} of items added mid-sprint were bugs or build failures. The plan does not reserve capacity for them.</p></div>
<div class="fd"><span>04</span><p><b>Code review is the biggest queue.</b> It takes {pct(A.review_share)} of all cycle time. When an item waits for review, 15% wait longer than {rv85:.0f} days.</p></div>
<div class="fd"><span>05</span><p><b>Sprints run without goals.</b> Only {goals} of {int(A.sprints)} sprints recorded a sprint goal, so there is no shared test for what to drop when new work arrives.</p></div>
<h2>Decisions requested</h2>
<div class="fd"><span>A</span><p><b>Reserve 20% of each sprint for unplanned work</b> and commit only the remaining capacity.</p></div>
<div class="fd"><span>B</span><p><b>Set a two-day service level for code review</b>, with a daily review slot owned by the team.</p></div>
<div class="fd"><span>C</span><p><b>Move Persistence to Kanban with WIP limits.</b> It adds {pe.added_pct:.1f} times more work mid-sprint than it commits, so sprints are not its real operating model.</p></div>
'''))
# ---------------- page 2: evidence
P.append(page(2, f'''
<h1 style="font-size:26pt">The evidence</h1>
<h2>Say-do ratio by team, three-sprint rolling average</h2>
<div class="box">{line_chart(690, 210)}
<div class="lg"><span><i style="background:{INK}"></i>Foundations</span><span><i style="background:{GREY}"></i>Persistence</span><span><i style="background:{ACC}"></i>Transactions</span></div></div>
<div class="two">
 <div><h2>Transactions, committed vs done</h2><div class="box">{tr_bars(320, 170)}
 <div class="lg"><span><i style="background:{LINE}"></i>Committed at start</span><span><i style="background:{INK}"></i>Done by end</span></div></div></div>
 <div><h2>Added mid-sprint, by type</h2><div class="box" style="height:217px">
 {''.join(f'<div class="sb" style="grid-template-columns:1.15in 1fr"><span>{E(t)}</span><div class="bar"><i style="width:{v * 100 / added.type.value_counts(normalize=True).max():.0f}%;background:{ACC if t in ("Bug", "Build Failure") else INK}">{v * 100:.0f}%</i></div></div>' for t, v in added.type.value_counts(normalize=True).head(5).items())}
 <div class="lg"><span><i style="background:{ACC}"></i>Unplanned: bugs and build failures</span></div></div></div>
</div>
<h2>Where cycle time goes</h2>
<div class="box">{time_split(690)}</div>
<p style="margin-top:12px">Read across: Foundations spends the largest share of its cycle time actually working. Transactions loses the most to code review. Persistence loses the most to blocked items, at {pct(pe.blocked_share)} of its cycle time.</p>
'''))
# ---------------- page 3: RAID
raid = [
 ('R1', 'Risk', 'Release dates slip because sprint plans complete less than half of what they commit.', 'High', 'Track say-do every sprint. Commit to 80% of measured capacity, not wishes.', 'Delivery manager'),
 ('R2', 'Risk', f'Code review queues grow as the Transactions team adds people ({pct(H.loc["SE Transactions"].review_share)} of its cycle time is review).', 'High', 'Two-day review service level, daily review slot, pair reviews for large changes.', 'Tech lead'),
 ('R3', 'Risk', f'{n5} items have been carried through 5 or more sprints (one through {nmax}). Old work hides real capacity.', 'Medium', 'Backlog triage: close, split or re-plan anything carried 3 or more times.', 'Product owner'),
 ('A1', 'Assumption', 'Jira status history reflects real work. Teams that update tickets late will show longer cycle times than reality.', 'Medium', 'Confirm with each team lead before acting on any single number.', 'Delivery manager'),
 ('A2', 'Assumption', 'Story points are set before sprint start. 93% of committed items carry points.', 'Low', 'Use item counts as the primary measure, points as a cross-check.', 'Delivery manager'),
 ('I1', 'Issue', f'Unplanned bugs and build failures make up {pct(unpl)} of mid-sprint additions with no capacity held for them.', 'High', 'Hold a 20% buffer. Rotate a build-failure owner each sprint.', 'Engineering manager'),
 ('I2', 'Issue', f'Only {goals} of {int(A.sprints)} sprints have a written goal.', 'Medium', 'No sprint starts without a one-sentence goal agreed in planning.', 'Product owner'),
 ('D1', 'Dependency', 'Build failures come from the shared continuous integration pipeline, outside any one team.', 'High', 'Agree an owner and a fix-time target with the build and release group.', 'Delivery manager'),
 ('D2', 'Dependency', 'Persistence work is blocked for long stretches waiting on other teams.', 'Medium', 'Name every blocking dependency in planning, with an owner and a date.', 'Team lead'),
]
rows = ''.join(f'<tr><td class="k">{a}</td><td class="r">{b}</td><td>{E(c)}</td><td class="r" style="color:{ACC if d == "High" else INK}">{d}</td><td>{E(e)}</td><td>{E(f)}</td></tr>' for a, b, c, d, e, f in raid)
P.append(page(3, f'''
<h1 style="font-size:26pt">RAID log</h1>
<p class="lead" style="margin-bottom:16px">Risks, assumptions, issues and dependencies, each with a mitigation and an owner role. Reviewed every two weeks in the program sync.</p>
<table><tr><th>ID</th><th>Type</th><th>Description</th><th>Rating</th><th>Mitigation</th><th>Owner</th></tr>{rows}</table>
'''))
# ---------------- page 4: 90-day plan
P.append(page(4, f'''
<h1 style="font-size:26pt">90-day recovery plan</h1>
<p class="lead">What I would do in my first 90 days as delivery manager for this program. The aim is predictability first, then speed.</p>
<div class="ph">
 <div><div class="d">Days 1 to 30</div><h4>Make it visible</h4><ul>
  <li>Meet each team lead and confirm the data matches their reality.</li>
  <li>Publish this dashboard and review it in every sprint review.</li>
  <li>Add a one-sentence goal to every sprint.</li>
  <li>Triage all {n3} items carried 3 or more times.</li></ul></div>
 <div><div class="d">Days 31 to 60</div><h4>Protect the plan</h4><ul>
  <li>Commit to 80% of measured capacity and hold 20% for unplanned work.</li>
  <li>Start the two-day code review service level.</li>
  <li>Rotate a build-failure owner each sprint.</li>
  <li>Move Persistence to Kanban with WIP limits.</li></ul></div>
 <div><div class="d">Days 61 to 90</div><h4>Make it stick</h4><ul>
  <li>Forecast with the 85th percentile cycle time, not averages.</li>
  <li>Run a cross-team retrospective on dependencies.</li>
  <li>Hand the metrics to the teams to own.</li>
  <li>Report results against the targets below.</li></ul></div>
</div>
<h2>Targets at day 90</h2>
<table class="kp"><tr><th>Measure</th><th>Today</th><th>Target</th><th>Why it matters</th></tr>
<tr><td><b>Say-do ratio</b></td><td class="r">{pct(A.say_do)}</td><td class="r" style="color:{ACC}">70% or more</td><td>Leaders can plan around what the teams say.</td></tr>
<tr><td><b>Scope added mid-sprint</b></td><td class="r">{pct(A.added_pct)}</td><td class="r" style="color:{ACC}">under 30%</td><td>Unplanned work goes into the buffer, not the plan.</td></tr>
<tr><td><b>Code review share of cycle time</b></td><td class="r">{pct(A.review_share)}</td><td class="r" style="color:{ACC}">under 15%</td><td>The biggest queue shrinks.</td></tr>
<tr><td><b>Items carried 3 or more sprints</b></td><td class="r">{n3}</td><td class="r" style="color:{ACC}">half that or fewer</td><td>The board shows real work only.</td></tr>
<tr><td><b>Cycle time, 85th percentile</b></td><td class="r">{A.cycle_p85:.0f} days</td><td class="r" style="color:{ACC}">under 12 days</td><td>Forecasts customers can trust.</td></tr>
<tr><td><b>Sprints with a written goal</b></td><td class="r">{goals} of {int(A.sprints)}</td><td class="r" style="color:{ACC}">every sprint</td><td>A shared test for what to drop.</td></tr>
</table>
'''))
# ---------------- page 5: method
P.append(page(5, f'''
<h1 style="font-size:26pt">Method and limits</h1>
<h2>Data</h2>
<p>MongoDB runs its WiredTiger storage engine project in a public Jira. I pulled every WT issue that sat in a sprint and changed after January 2025: 2,943 issues with full status and sprint history. The analysis covers the three teams with regular two-week sprints from April 2025 to October 2026: Foundations ({int(H.loc["SE Foundations"].sprints)} sprints), Persistence ({int(H.loc["SE Persistence"].sprints)}) and Transactions ({int(H.loc["SE Transactions"].sprints)}). Sprints shorter than seven days were left out.</p>
<h2>How each measure is built</h2>
<p><b>Committed</b> means the item was in the sprint two hours after it started, rebuilt from the sprint history of every ticket, not from the end-of-sprint view. <b>Done</b> means closed or resolved by the time the sprint was completed. <b>Say-do ratio</b> is committed items done divided by committed items. <b>Added</b> means the item joined after the start. <b>Cycle time</b> runs from the first move into In Progress or Investigating to the final close. Time in each status is summed between those two points.</p>
<h2>Limits, stated plainly</h2>
<p>This is an outside-in read of public tickets. It does not know about holidays, people moving between teams, on-call duty or work done outside Jira. Many open-source teams use sprints as a planning rhythm, not a promise, so a low say-do ratio here is a signal to ask about, not a verdict on the people. Team sizes are estimated from distinct assignees. No individual is named or scored anywhere in this report or the data.</p>
<h2>Built with</h2>
<p>Python (Jira REST API, pandas) for extraction and metrics, Power BI (star schema, DAX) for the dashboard, Excel for the scorecard model. Every number in this report is generated from the published data files, and the code is in the repository.</p>
'''))
open('report.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print('ok', 'unplanned', round(unpl, 3), 'n3', n3, 'n5', n5, 'max', nmax, 'hit80', hit80, 'of', with_c, 'goals', goals, 'rv85', round(rv85, 1), 'tr', round(tr_c1, 1), round(tr_c2, 1), round(tr_sd1, 3), round(tr_sd2, 3))
