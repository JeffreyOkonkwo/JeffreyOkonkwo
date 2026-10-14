"""Pull WiredTiger (WT) issues that were in any sprint and touched since 2025-01-01, with full changelog, from MongoDB's public Jira."""
import json, time, urllib.request, urllib.parse, os
OUT = 'raw'
JQL = 'project = WT AND sprint is not EMPTY AND updated >= "2025-01-01" ORDER BY key ASC'
F = 'summary,status,issuetype,priority,created,resolutiondate,resolution,customfield_10557,customfield_10555,assignee,labels,components,customfield_14050,customfield_12751'
start, total, n = 0, None, 0
while total is None or start < total:
    q = urllib.parse.urlencode({'jql': JQL, 'startAt': start, 'maxResults': 100, 'fields': F, 'expand': 'changelog'})
    for t in range(5):
        try:
            d = json.load(urllib.request.urlopen('https://jira.mongodb.org/rest/api/2/search?' + q, timeout=120)); break
        except Exception as e:
            print('retry', start, e); time.sleep(5 * (t + 1))
    total = d['total']; json.dump(d, open(f'{OUT}/page_{start:05d}.json', 'w'))
    start += len(d['issues']); n += 1; print(start, '/', total, flush=True); time.sleep(0.6)
print('done', start)
