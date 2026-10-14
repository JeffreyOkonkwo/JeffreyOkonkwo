"""Page layout for the Beat the Delay Power BI report. Page is 1280 x 720.
Panels (titles, notes, art) are drawn into the background image; visuals sit inside panels at the
'slot' rectangles with transparent backgrounds. Each panel: id, x, y, w, h, title, note, and
slots {name: (x, y, w, h)} in page pixels."""

def _kpi_tiles():
    tiles = [('k1', 'train', 'Delays that stopped a train', None), ('k2', 'clock', 'Hours lost to delays', None),
             ('k3', 'people', 'People-related share of time', 'red'), ('k4', 'rush', 'Rush hour against midday', 'yellow'),
             ('k5', 'stopwatch', 'Average stop, in minutes', None), ('k6', 'pin', 'Worst station, by minutes lost', None)]
    out = []
    for i, (pid, icon, label, acc) in enumerate(tiles):
        x = 16 + round(i * 209.6)
        out.append({'id': pid, 'x': x, 'y': 66, 'w': 200, 'h': 76, 'tile': True, 'icon': icon, 'kpi': label,
                    **({'accent': acc} if acc else {}), 'slots': {'card': (x + 50, 90, 142, 46)}})
    return out


PAGES = [
  {
    'name': 'command', 'display': 'Command centre', 'style': 'neon',
    'panels': [
      {'id': 'head', 'x': 16, 'y': 10, 'w': 1248, 'h': 48, 'header': True,
       'title': 'BEAT THE DELAY', 'note': 'Toronto subway delay analytics | Jan 2025 to Aug 2026',
       'slots': {'nav': (500, 15, 540, 38), 's_line': (1052, 12, 200, 44)}},
      *_kpi_tiles(),
      {'id': 'causes', 'x': 16, 'y': 150, 'w': 440, 'h': 268, 'title': 'Minutes lost by cause',
       'note': 'Red marks people-related causes', 'slots': {'chart': (26, 196, 420, 214)}},
      {'id': 'hours', 'x': 466, 'y': 150, 'w': 456, 'h': 268, 'title': 'Delays by hour of day',
       'note': 'From the first train at 5 a.m. Red marks the rush hours.', 'slots': {'chart': (476, 196, 436, 214)}},
      {'id': 'split', 'x': 932, 'y': 150, 'w': 332, 'h': 268, 'title': 'People or equipment?',
       'note': 'Share of minutes lost by cause type', 'slots': {'chart': (942, 196, 312, 214)}},
      {'id': 'trend', 'x': 16, 'y': 426, 'w': 372, 'h': 284, 'title': 'Month by month',
       'note': 'Minutes lost each month', 'slots': {'chart': (26, 472, 352, 230)}},
      {'id': 'stations', 'x': 398, 'y': 426, 'w': 318, 'h': 284, 'title': 'Top eight stations',
       'note': 'Minutes lost, line-wide delays left out', 'slots': {'chart': (408, 472, 298, 230)}},
      {'id': 'heat', 'x': 726, 'y': 426, 'w': 538, 'h': 284, 'title': 'When the delays happen',
       'note': 'Delays by weekday and hour. Darker red means more delays.', 'slots': {'chart': (736, 472, 518, 230)}},
    ],
  },
  {
    'name': 'overview', 'display': 'Overview',
    'panels': [
      {'id': 'hero', 'x': 16, 'y': 16, 'w': 1248, 'h': 248, 'art': True,
       'eyebrow': 'Beat the Delay | Toronto subway, January 2025 to August 2026',
       'title': 'Half of the time lost to subway delays is caused by people, not trains',
       'note': 'Every Toronto subway delay since January 2025, turned into a tool a rider can use every morning. '
               'Where does the time go, and when should a rider leave?'},
      {'id': 'k1', 'x': 16, 'y': 280, 'w': 300, 'h': 108, 'kpi': 'Delays that stopped a train', 'slots': {'card': (28, 304, 276, 76)}},
      {'id': 'k2', 'x': 332, 'y': 280, 'w': 300, 'h': 108, 'kpi': 'Hours lost to delays', 'slots': {'card': (344, 304, 276, 76)}},
      {'id': 'k3', 'x': 648, 'y': 280, 'w': 300, 'h': 108, 'kpi': 'Share of lost time that is people-related', 'accent': 'red', 'slots': {'card': (660, 304, 276, 76)}},
      {'id': 'k4', 'x': 964, 'y': 280, 'w': 300, 'h': 108, 'kpi': 'More delays per hour in weekday rush than midday', 'accent': 'yellow', 'slots': {'card': (976, 304, 276, 76)}},
      {'id': 'causes', 'x': 16, 'y': 404, 'w': 420, 'h': 300, 'title': 'People-related causes cost the most time',
       'note': 'Minutes lost by cause. Red marks people-related causes.', 'slots': {'chart': (28, 456, 396, 240)}},
      {'id': 'hours', 'x': 452, 'y': 404, 'w': 448, 'h': 300, 'title': 'The rush hours are the rough stretch',
       'note': 'Delays by hour the train was stopped. Red marks the rush hours.', 'slots': {'chart': (464, 456, 424, 240)}},
      {'id': 'stations', 'x': 916, 'y': 404, 'w': 348, 'h': 300, 'title': 'Bloor-Yonge loses the most time',
       'note': 'Minutes lost, top eight stations', 'slots': {'chart': (928, 456, 324, 240)}},
    ],
  },
  {
    'name': 'stations', 'display': 'Station explorer',
    'panels': [
      {'id': 'filters', 'x': 16, 'y': 16, 'w': 1248, 'h': 72, 'filters': True,
       'slots': {'s_line': (32, 24, 260, 58), 's_station': (308, 24, 300, 58), 's_period': (632, 24, 616, 58)}},
      {'id': 'rank', 'x': 16, 'y': 104, 'w': 380, 'h': 600, 'title': 'Station ranking',
       'note': 'Minutes lost by station. Scroll for the full list.', 'slots': {'chart': (28, 156, 356, 540)}},
      {'id': 'heat', 'x': 412, 'y': 104, 'w': 852, 'h': 338, 'title': 'When the delays happen',
       'note': 'Delays by weekday and hour, from the first train at 5 a.m. Darker red means more delays.',
       'slots': {'chart': (424, 156, 828, 278)}},
      {'id': 'trend', 'x': 412, 'y': 458, 'w': 560, 'h': 246, 'title': 'Month by month',
       'note': 'Minutes lost each month. Red marks the worst month.', 'slots': {'chart': (424, 508, 536, 188)}},
      {'id': 's1', 'x': 988, 'y': 458, 'w': 276, 'h': 115, 'kpi': 'Hours lost', 'slots': {'card': (1000, 482, 252, 80)}},
      {'id': 's2', 'x': 988, 'y': 589, 'w': 276, 'h': 115, 'kpi': 'Average stop, in minutes', 'slots': {'card': (1000, 613, 252, 80)}},
    ],
  },
  {
    'name': 'causes', 'display': 'Causes',
    'panels': [
      {'id': 'c1', 'x': 16, 'y': 16, 'w': 300, 'h': 120, 'kpi': 'Lost time that is people-related', 'accent': 'red', 'slots': {'card': (28, 42, 276, 84)}},
      {'id': 'c2', 'x': 332, 'y': 16, 'w': 300, 'h': 120, 'kpi': 'Average stop, in minutes', 'slots': {'card': (344, 42, 276, 84)}},
      {'id': 'c3', 'x': 648, 'y': 16, 'w': 300, 'h': 120, 'kpi': 'Half of all delays end within (minutes)', 'slots': {'card': (660, 42, 276, 84)}},
      {'id': 'c4', 'x': 964, 'y': 16, 'w': 300, 'h': 120, 'kpi': 'Delays that run past 10 minutes', 'accent': 'yellow', 'slots': {'card': (976, 42, 276, 84)}},
      {'id': 'split', 'x': 16, 'y': 152, 'w': 380, 'h': 552, 'title': 'People or equipment?',
       'note': 'Share of minutes lost by cause type', 'slots': {'chart': (28, 204, 356, 492)}},
      {'id': 'avg', 'x': 412, 'y': 152, 'w': 418, 'h': 552, 'title': 'Weather and track-level emergencies stop trains longest',
       'note': 'Average minutes per delay, by cause. Red marks people-related causes.', 'slots': {'chart': (424, 204, 394, 492)}},
      {'id': 'tail', 'x': 846, 'y': 152, 'w': 418, 'h': 552, 'title': 'The long tail',
       'note': 'Share of each cause’s delays that run past 10 minutes', 'slots': {'chart': (858, 204, 394, 492)}},
    ],
  },
  {
    'name': 'plan', 'display': 'Plan My Ride',
    'panels': [
      {'id': 'pick', 'x': 16, 'y': 16, 'w': 300, 'h': 688, 'plan': True, 'title': 'Plan My Ride',
       'note': 'Pick your station, the type of day and the hour you board. Every real delay in that slot is checked.',
       'slots': {'s_station': (32, 132, 268, 58), 's_day': (32, 204, 268, 92), 's_hour': (32, 310, 268, 58)}},
      {'id': 'verdict', 'x': 332, 'y': 16, 'w': 616, 'h': 200, 'kpi': 'Your verdict for this slot',
       'sub': 'Green light, steady pace or headwind: this slot compared with the usual hour at the same station.',
       'slots': {'card': (348, 56, 584, 112)}},
      {'id': 'buffer', 'x': 964, 'y': 16, 'w': 300, 'h': 200, 'kpi': 'Leave this many minutes early', 'accent': 'yellow',
       'sub': 'The average stop in this slot, rounded up to five minutes.', 'slots': {'card': (976, 56, 276, 112)}},
      {'id': 'r1', 'x': 332, 'y': 232, 'w': 300, 'h': 112, 'kpi': 'Days with a delay in this hour', 'slots': {'card': (344, 256, 276, 80)}},
      {'id': 'r2', 'x': 648, 'y': 232, 'w': 300, 'h': 112, 'kpi': 'Delays logged in this slot', 'slots': {'card': (660, 256, 276, 80)}},
      {'id': 'r3', 'x': 964, 'y': 232, 'w': 300, 'h': 112, 'kpi': 'Average stop, in minutes', 'slots': {'card': (976, 256, 276, 80)}},
      {'id': 'curve', 'x': 332, 'y': 360, 'w': 616, 'h': 344, 'title': 'Your station through the day',
       'note': 'Delays per 100 days of the chosen type, by hour. Red marks the rush hours.', 'slots': {'chart': (344, 412, 592, 284)}},
      {'id': 'why', 'x': 964, 'y': 360, 'w': 300, 'h': 344, 'title': 'What usually causes it',
       'note': 'Causes logged in your slot', 'slots': {'chart': (976, 412, 276, 284)}},
    ],
  },
]
