"""Flatten raw Jira pages into tidy tables: issues, sprints, status transitions, sprint membership events."""
import json, glob, re, pandas as pd
iss = [i for f in sorted(glob.glob('raw/page_*.json')) for i in json.load(open(f))['issues']]
SP = re.compile(r'\[(.*)\]\s*$', re.S)
def sprint_obj(s):
    body = SP.search(s).group(1); d = {}
    for part in re.split(r',(?=[a-zA-Z]+=)', body):
        k, _, v = part.partition('='); d[k] = None if v == '<null>' else v
    return d
sprints, issues, trans, mem = {}, [], [], []
for i in iss:
    f = i['fields']
    for s in f.get('customfield_10557') or []:
        o = sprint_obj(s); sprints[o['id']] = o
    issues.append(dict(key=i['key'], type=f['issuetype']['name'], status=f['status']['name'], status_cat=f['status'].get('statusCategory', {}).get('name'),
                       priority=(f.get('priority') or {}).get('name'), created=f['created'], resolved=f['resolutiondate'],
                       resolution=(f.get('resolution') or {}).get('name'), points=f.get('customfield_10555'),
                       assignee_hash=(hash((f.get('assignee') or {}).get('key')) % 10**8) if f.get('assignee') else None,
                       sprint_names='|'.join(sprint_obj(s)['name'] for s in (f.get('customfield_10557') or [])),
                       sprint_ids='|'.join(sprint_obj(s)['id'] for s in (f.get('customfield_10557') or []))))
    for h in i['changelog']['histories']:
        for it in h['items']:
            if it['field'] == 'status': trans.append(dict(key=i['key'], at=h['created'], frm=it['fromString'], to=it['toString']))
            if it['field'] == 'Sprint': mem.append(dict(key=i['key'], at=h['created'], frm=it['fromString'] or '', to=it['toString'] or '', frm_id=it.get('from') or '', to_id=it.get('to') or ''))
S = pd.DataFrame(sprints.values())[['id', 'name', 'state', 'rapidViewId', 'startDate', 'endDate', 'completeDate', 'activatedDate', 'goal']]
pd.DataFrame(issues).to_csv('data_issues.csv', index=False); S.to_csv('data_sprints.csv', index=False)
pd.DataFrame(trans).to_csv('data_transitions.csv', index=False); pd.DataFrame(mem).to_csv('data_membership.csv', index=False)
print(len(issues), len(S), len(trans), len(mem))
