"""Write one HTML file per report page into bg/. shot_bg.mjs then renders each to a 2560 x 1440 PNG.
The page backgrounds carry the panels, titles, notes and the Tayo art; visuals sit on top.
Paths are relative to this script. Set BTD_KIT to the beat-the-delay/powerbi folder if the script
is not inside beat-the-delay/powerbi/project/."""
import base64, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from layout import PAGES

KIT = os.environ.get('BTD_KIT', os.path.join(HERE, '..'))
ROOT = os.path.join(KIT, '..')
os.makedirs(os.path.join(HERE, 'bg'), exist_ok=True)

hero = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(ROOT, 'assets', 'hero.jpg'), 'rb').read()).decode()
neon_path = os.path.join(ROOT, 'assets', 'btd_bg.png')
from PIL import Image as _I; import io as _io
_t = _I.open(os.path.join(ROOT, 'assets', 'hero.jpg')).convert('RGB').crop((960, 50, 1220, 310)).resize((160, 160)); _b = _io.BytesIO(); _t.save(_b, 'JPEG', quality=88)
TAYO = 'data:image/jpeg;base64,' + base64.b64encode(_b.getvalue()).decode()
neon = 'data:image/png;base64,' + base64.b64encode(open(neon_path, 'rb').read()).decode() if os.path.exists(neon_path) else ''
fonts = '\n'.join(re.findall(r"@font-face\{[^}]*\}", open(os.path.join(ROOT, 'dashboard.html'), encoding='utf-8').read()))

BOARD, PANEL, INK, SOFT, FAINT = '#0C0D10', '#15171C', '#F5F6F8', '#A9AFB8', '#6B717B'
RED, YELLOW, GREEN = '#D7322B', '#F8C300', '#00923F'
ACC = {'red': RED, 'yellow': YELLOW, 'green': GREEN}

# small line icons for the command centre KPI tiles (24 x 24 grid, drawn with currentColor)
ICONS = {
    'train': '<rect x="5" y="3" width="14" height="14" rx="3"/><path d="M5 11h14M9 21l-2 -4M15 21l2 -4"/><circle cx="8.5" cy="14" r=".6"/><circle cx="15.5" cy="14" r=".6"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'people': '<circle cx="9" cy="8" r="3"/><path d="M3 20c0 -3.5 2.7 -6 6 -6s6 2.5 6 6"/><circle cx="17" cy="9" r="2.4"/><path d="M16 14.2c2.8 .2 5 2.4 5 5.8"/>',
    'rush': '<path d="M13 2L4 14h7l-1 8 9 -12h-7z"/>',
    'stopwatch': '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 1.5M9.5 2h5M12 2v3M19 6l1.5 -1.5"/>',
    'pin': '<path d="M12 22s-7 -6.6 -7 -12a7 7 0 0 1 14 0c0 5.4 -7 12 -7 12z"/><circle cx="12" cy="10" r="2.6"/>',
}


def icon(name, color):
    return (f'<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="{color}" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def neon_panel(p):
    acc = ACC.get(p.get('accent'), INK)
    cls = 'g hd' if p.get('header') else 'g tile' if p.get('tile') else 'g'
    h = f'<div class="{cls}" style="left:{p["x"]}px;top:{p["y"]}px;width:{p["w"]}px;height:{p["h"]}px">'
    if p.get('header'):
        h += f'<img class="av" src="{TAYO}"><div class="logo"><span class="chk"></span>{p["title"]}</div><div class="hsub">{p["note"]}</div>'
        h += '<div class="live"><i></i>Live</div>'
    elif p.get('tile'):
        ic = RED if p.get('accent') == 'red' else YELLOW if p.get('accent') == 'yellow' else INK
        h += f'<div class="ic" style="color:{ic};box-shadow:0 0 12px {"rgba(215,50,43,.45)" if ic == RED else "rgba(248,195,0,.35)" if ic == YELLOW else "rgba(255,255,255,.08)"}">{icon(p["icon"], ic)}</div>'
        h += f'<div class="tl">{p["kpi"]}</div>'
    else:
        h += f'<div class="gt">{p["title"]}</div><div class="gn">{p["note"]}</div>'
    return h + '</div>'


NEON_CSS = '''
body.neon{background:#050506}
.photo{position:absolute;inset:0;background:#050506}
.photo img{width:100%;height:100%;object-fit:cover;object-position:right center;display:block}
.photo::after{content:'';position:absolute;inset:0;background:
  linear-gradient(90deg,rgba(3,3,4,.9) 0%,rgba(3,3,4,.75) 45%,rgba(3,3,4,.3) 75%,rgba(3,3,4,.05) 100%),
  linear-gradient(0deg,rgba(3,3,4,.55),transparent 40%)}
.g{position:absolute;border-radius:12px;background:rgba(10,10,12,.78);border:1px solid rgba(215,50,43,.6);
  box-shadow:0 0 16px rgba(215,50,43,.35),inset 0 1px 0 rgba(255,255,255,.04);overflow:hidden}
.g::before{content:'';position:absolute;right:12px;top:0;width:26px;height:3px;border-radius:0 0 2px 2px;
  background:repeating-linear-gradient(90deg,#F5F6F8 0 4px,#2A2D34 4px 8px);opacity:.6}
.g.hd::before{display:none}
.gt{position:absolute;left:12px;top:9px;font-family:'BTD Hwy';font-size:15px;color:#F5F6F8;letter-spacing:.01em}
.gn{position:absolute;left:12px;top:28px;font-size:10px;color:#8E949D}
.av{position:absolute;left:8px;top:5px;width:42px;height:42px;border-radius:50%;object-fit:cover;border:2px solid #D7322B;box-shadow:0 0 12px rgba(215,50,43,.75)}
.logo{position:absolute;left:60px;top:6px;font-family:'BTD Hwy';font-size:24px;letter-spacing:.06em;color:#F5F6F8;
  text-shadow:0 0 14px rgba(215,50,43,.75),0 0 2px rgba(255,255,255,.4);display:flex;align-items:center;gap:10px}
.chk{width:18px;height:18px;border-radius:3px;display:inline-block;
  background:conic-gradient(#F5F6F8 25%,#1A1B1F 0 50%,#F5F6F8 0 75%,#1A1B1F 0) 0 0/9px 9px;box-shadow:0 0 8px rgba(215,50,43,.6)}
.hsub{position:absolute;left:89px;top:31px;font-size:10px;color:#A9AFB8;letter-spacing:.02em}
.live{position:absolute;left:386px;top:19px;font-size:8px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#D7322B;display:flex;gap:6px;align-items:center}
.live i{width:7px;height:7px;border-radius:50%;background:#D7322B;box-shadow:0 0 8px #D7322B}
.tile .ic{position:absolute;left:11px;top:22px;width:32px;height:32px;border-radius:9px;display:flex;align-items:center;justify-content:center;
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08)}
.tl{position:absolute;left:52px;top:9px;right:10px;font-size:10px;color:#A9AFB8;font-weight:600;line-height:1.2;white-space:nowrap}
'''


def panel(p):
    acc = ACC.get(p.get('accent'), INK)
    cls = 'p hero' if p.get('art') else 'p'
    h = f'<div class="{cls}" style="left:{p["x"]}px;top:{p["y"]}px;width:{p["w"]}px;height:{p["h"]}px">'
    if p.get('art'):
        h += f'<div class="art"><img src="{hero}"><div class="fade"></div></div>'
        h += '<div class="hand" style="left:640px;top:150px">first day. do not be late.</div>'
        h += f'<div class="ht"><div class="eb">{p["eyebrow"]}</div><div class="t1">{p["title"]}</div><div class="n1">{p["note"]}</div></div>'
        h += ('<div class="src">Data: TTC Subway Delay Data, City of Toronto Open Data, Open Government Licence, Toronto. '
              'Not affiliated with the TTC. Built by Jeffrey Okonkwo, CBAP, CSM, PL-300.</div>')
    elif p.get('plan'):
        h += f'<div class="eb" style="left:16px;top:18px;position:absolute">Problem 2: for riders</div>'
        h += f'<div class="pt big">{p["title"]}</div><div class="pn wide">{p["note"]}</div>'
        h += '<div class="lane"></div>'
        h += f'<div class="tayo"><img src="{hero}"><div class="fade2"></div></div>'
        h += '<div class="hand" style="left:18px;bottom:18px;font-size:19px">Tayo starts at 9:00. He leaves early.</div>'
    else:
        if p.get('kpi'):
            h += f'<div class="kpi"><i style="background:{acc};box-shadow:0 0 10px {acc}"></i>{p["kpi"]}</div>'
        if p.get('sub'):
            h += f'<div class="sub">{p["sub"]}</div>'
        if p.get('title'):
            h += f'<div class="pt">{p["title"]}</div>'
        if p.get('note'):
            h += f'<div class="pn">{p["note"]}</div>'
    return h + '</div>'


CSS = f'''{fonts}
html,body{{margin:0;width:1280px;height:720px;overflow:hidden}}
body{{background:radial-gradient(700px 420px at 100% -10%,rgba(215,50,43,.13),transparent 60%),
  radial-gradient(620px 520px at -10% 80%,rgba(248,195,0,.05),transparent 62%),linear-gradient(180deg,#14161B,{BOARD} 60%);
  font-family:'BTD Sans';color:{INK};position:relative}}
body::before{{content:'';position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.018) 0 1px,transparent 1px 64px);pointer-events:none}}
.p{{position:absolute;border-radius:14px;background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.022));
  border:1px solid rgba(255,255,255,.08);box-shadow:0 1px 0 rgba(255,255,255,.05) inset,0 18px 36px -22px rgba(0,0,0,.85);overflow:hidden}}
.p::before{{content:'';position:absolute;left:16px;top:0;width:34px;height:3px;border-radius:0 0 2px 2px;
  background:repeating-linear-gradient(90deg,{INK} 0 5px,#2A2D34 5px 10px);opacity:.75}}
.hero::before{{display:none}}
.pt{{position:absolute;left:16px;top:13px;right:16px;font-family:'BTD Hwy';font-size:19px;letter-spacing:.005em;line-height:1.1}}
.pt.big{{top:40px;font-size:30px}}
.pn{{position:absolute;left:16px;top:35px;right:16px;font-size:11px;color:{SOFT};line-height:1.35}}
.pn.wide{{top:78px;font-size:11.5px;line-height:1.45;right:18px}}
.kpi{{position:absolute;left:14px;top:11px;font-size:11.5px;color:{SOFT};display:flex;gap:7px;align-items:center;font-weight:600}}
.kpi i{{width:7px;height:7px;border-radius:50%;display:inline-block;flex:none}}
.sub{{position:absolute;left:16px;right:16px;bottom:13px;font-size:10.5px;color:{FAINT};line-height:1.35}}
.flt{{position:absolute;right:16px;top:9px;font-size:9px;color:{FAINT};letter-spacing:.14em;text-transform:uppercase;font-weight:700}}
.eb{{font-size:10.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:{RED}}}
.art{{position:absolute;right:0;top:0;bottom:0;width:690px;background:#1A2F8C}}
.art img{{width:100%;height:100%;object-fit:cover;object-position:62% 46%}}
.art{{-webkit-mask-image:linear-gradient(90deg,transparent 0%,rgba(0,0,0,.55) 18%,#000 46%);mask-image:linear-gradient(90deg,transparent 0%,rgba(0,0,0,.55) 18%,#000 46%)}}
.fade{{position:absolute;inset:0;background:linear-gradient(0deg,rgba(12,13,16,.55),transparent 32%)}}
.ht{{position:absolute;left:28px;top:26px;width:560px}}
.t1{{font-family:'BTD Hwy';font-size:35px;line-height:1.04;margin-top:10px;letter-spacing:-.005em}}
.n1{{font-size:12.5px;color:{SOFT};margin-top:12px;line-height:1.5;max-width:520px}}
.src{{position:absolute;left:28px;bottom:14px;font-size:9.5px;color:{FAINT};width:600px;line-height:1.4}}
.hand{{position:absolute;font-family:'BTD Hand';font-size:22px;color:{YELLOW};z-index:3;text-shadow:0 2px 8px rgba(0,0,0,.6)}}
.lane{{position:absolute;left:16px;right:16px;top:118px;border-top:1px dashed rgba(255,255,255,.12)}}
.tayo{{position:absolute;left:0;right:0;bottom:0;height:300px;background:#1A2F8C}}
.tayo img{{width:100%;height:100%;object-fit:cover;object-position:66% 46%}}
.tayo{{-webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 34%);mask-image:linear-gradient(180deg,transparent 0%,#000 34%)}}
.fade2{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(12,13,16,0) 65%,rgba(12,13,16,.7) 100%)}}
'''

for pg in PAGES:
    if pg.get('style') == 'neon':
        body = f'<div class="photo"><img src="{neon}"></div>' + ''.join(neon_panel(p) for p in pg['panels'])
        html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{NEON_CSS}</style></head>'
                f'<body class="neon">{body}</body></html>')
    else:
        body = ''.join(panel(p) for p in pg['panels'])
        html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
    open(os.path.join(HERE, 'bg', pg['name'] + '.html'), 'w', encoding='utf-8').write(html)
print('backgrounds written to', os.path.join(HERE, 'bg'))
