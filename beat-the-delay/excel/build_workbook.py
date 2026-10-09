import os, json
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.text import RichText
from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties, Font as DFont
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.image import Image as XLImage
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import ColorScaleRule, DataBarRule, FormulaRule, CellIsRule
from openpyxl.utils import get_column_letter as L

PAL = json.load(open("/home/claude/ttc/palette.json"))
C = PAL["colors"]; HEAD = PAL["fonts"]["head"]; BODY = PAL["fonts"]["body"]
LINECOL = {"Line 1": "F8C300", "Line 2": "00923F", "Line 4": "A21A68", "Multiple lines": "8C96A3"}

def fill(c): return PatternFill("solid", fgColor=c)
def f(sz=10, bold=False, color=None, name=None, italic=False):
    return Font(name=name or BODY, size=sz, bold=bold, color=color or C["ink"], italic=italic)
def side(c, s="thin"): return Side(style=s, color=c)
AL = lambda h="left", v="center", **k: Alignment(horizontal=h, vertical=v, **k)

d = pd.read_pickle("/home/claude/ttc/clean.pkl")
codes = pd.read_csv("/home/claude/ttc/raw/codes.csv")
wb = Workbook()
race = wb.active; race.title = "Race Day"
plan = wb.create_sheet("Plan My Ride")
spl = wb.create_sheet("Splits")
data = wb.create_sheet("Delays")
cod = wb.create_sheet("Cause Codes")
readme = wb.create_sheet("Read Me")

# ---------------------------------------------------------------- DATA
cols = ["Date", "Month", "Day", "Hour", "Time", "Line", "Station", "Bound", "Cause", "Code", "Code Description", "Min Delay", "Min Gap"]
data.append(cols)
for r in d.itertuples(index=False):
    row = list(r); row[0] = row[0].to_pydatetime().date(); row[7] = row[7] if isinstance(row[7], str) else ""
    data.append(row)
N = len(d) + 1
for c in data[1]:
    c.font = f(10, True, "FFFFFF"); c.fill = fill(C["ink"]); c.alignment = AL("center")
for i, w in enumerate([11, 9, 11, 6, 7, 13, 30, 7, 28, 9, 46, 10, 9], 1):
    data.column_dimensions[L(i)].width = w
for row in data.iter_rows(min_row=2, max_row=N, min_col=1, max_col=1):
    row[0].number_format = "yyyy-mm-dd"
t = Table(displayName="tblDelays", ref=f"A1:M{N}"); t.tableStyleInfo = TableStyleInfo(name="TableStyleLight15", showRowStripes=True)
data.add_table(t); data.freeze_panes = "A2"
R = lambda col: f"Delays!${col}$2:${col}${N}"
DATE, MON, DAY, HOUR, LINE, STN, CAUSE, MIN = R("A"), R("B"), R("C"), R("D"), R("F"), R("G"), R("I"), R("L")

# Cause code lookup
cod.append(["Code", "Description", "Cause group (my grouping)"])
cmap = d.drop_duplicates("Code").set_index("Code")["Cause"].to_dict()
for code, desc in zip(codes.CODE.str.strip(), codes.DESCRIPTION):
    desc = str(desc).replace("â", "-").strip()
    cod.append([code, " ".join(desc.split()).capitalize(), cmap.get(code, "Not seen in delays since 2025")])
for c in cod[1]: c.font = f(10, True, "FFFFFF"); c.fill = fill(C["ink"])
cod.column_dimensions["A"].width = 10; cod.column_dimensions["B"].width = 60; cod.column_dimensions["C"].width = 32

# ---------------------------------------------------------------- SPLITS (model)
spl["A1"] = "Splits: every number on Race Day and Plan My Ride is calculated here from the Delays tab."
spl["A1"].font = f(11, True)
spl["A3"] = "First day"; spl["B3"] = f"=MIN({DATE})"
spl["A4"] = "Last day"; spl["B4"] = f"=MAX({DATE})"
spl["A5"] = "Days covered"; spl["B5"] = "=B4-B3+1"
spl["A6"] = "Total minutes lost"; spl["B6"] = f"=SUM({MIN})"
spl["A7"] = "Delays that stopped trains"; spl["B7"] = f"=COUNT({MIN})"
for r in (3, 4): spl[f"B{r}"].number_format = "d mmm yyyy"

causes = d.groupby("Cause")["Min Delay"].sum().sort_values(ascending=False).index.tolist()
people = {"Disorderly or security", "Customer illness or injury", "Track-level emergencies", "Alarms with no trouble found", "Unsanitary vehicle"}
spl["A9"] = "Cause"; spl["B9"] = "Minutes"; spl["C9"] = "Delays"; spl["D9"] = "Cumulative share"; spl["E9"] = "People-related?"
for i, cs in enumerate(causes):
    r = 10 + i
    spl[f"A{r}"] = cs
    spl[f"B{r}"] = f'=SUMIFS({MIN},{CAUSE},A{r})'; spl[f"B{r}"].number_format = '#,##0'
    spl[f"C{r}"] = f'=COUNTIFS({CAUSE},A{r})'
    spl[f"D{r}"] = f"=SUM($B$10:B{r})/$B$6"; spl[f"D{r}"].number_format = "0%"
    spl[f"E{r}"] = "Yes" if cs in people else "No"
ce = 9 + len(causes)
spl["A21"] = "People-related share of minutes"; spl["B21"] = f'=SUMIFS(B10:B{ce},E10:E{ce},"Yes")/B6'; spl["B21"].number_format = "0%"

lines = ["Line 1", "Line 2", "Line 4"]
spl["A23"] = "Line"; spl["B23"] = "Minutes"; spl["C23"] = "Delays"; spl["D23"] = "Avg stop (min)"; spl["E23"] = "Hours lost"
for i, ln in enumerate(lines):
    r = 24 + i
    spl[f"A{r}"] = ln; spl[f"B{r}"] = f"=SUMIFS({MIN},{LINE},A{r})"; spl[f"C{r}"] = f"=COUNTIFS({LINE},A{r})"
    spl[f"D{r}"] = f"=B{r}/C{r}"; spl[f"D{r}"].number_format = "0.0"; spl[f"E{r}"] = f"=B{r}/60"; spl[f"E{r}"].number_format = "#,##0"

months = sorted(d.Month.unique())
spl["A29"] = "Month"; spl["B29"] = "Minutes"; spl["C29"] = "Label"
for i, m in enumerate(months):
    r = 30 + i
    spl[f"A{r}"] = m; spl[f"B{r}"] = f"=SUMIFS({MIN},{MON},A{r})"
    y, mo = m.split("-"); spl[f"C{r}"] = pd.Timestamp(int(y), int(mo), 1).strftime("%b %y")
me = 29 + len(months)

st = d.groupby("Station")["Min Delay"].sum().sort_values(ascending=False)
stations = [s for s in st.index if not s.startswith("Line-wide")]
spl["G1"] = "Station"; spl["H1"] = "Minutes"; spl["I1"] = "Delays"; spl["J1"] = "Avg stop"; spl["K1"] = "Main line"
for i, s in enumerate(stations):
    r = 2 + i
    spl[f"G{r}"] = s; spl[f"H{r}"] = f"=SUMIFS({MIN},{STN},G{r})"; spl[f"I{r}"] = f"=COUNTIFS({STN},G{r})"
    spl[f"J{r}"] = f"=H{r}/I{r}"; spl[f"J{r}"].number_format = "0.0"
    spl[f"K{r}"] = d[d.Station == s].Line.value_counts().index[0]
se = 1 + len(stations)
stations_sorted = sorted(stations)

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
hours = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0, 1]
hlab = lambda h: ("12a" if h == 0 else f"{h}a" if h < 12 else "12p" if h == 12 else f"{h-12}p")
spl["M1"] = "Delays by day and hour (all stations)"
for j, h in enumerate(hours): spl.cell(2, 14 + j, h)
for i, dy in enumerate(days):
    spl.cell(3 + i, 13, dy)
    for j, h in enumerate(hours):
        spl.cell(3 + i, 14 + j, f"=COUNTIFS({DAY},$M{3+i},{HOUR},{L(14+j)}$2)")
# weekday counts in the period
spl["M12"] = "Number of each weekday in the period"
for i, dy in enumerate(days):
    spl.cell(13 + i, 13, dy)
    spl.cell(13 + i, 14, f'=SUMPRODUCT(--(WEEKDAY(ROW(INDIRECT($B$3&":"&$B$4)),2)={i+1}))')
hr_minutes_row = 22
spl["M21"] = "Minutes by hour"
for j, h in enumerate(hours):
    spl.cell(21, 14 + j, h)
    spl.cell(22, 14 + j, f"=SUMIFS({MIN},{HOUR},{L(14+j)}21)")
    spl.cell(23, 14 + j, f"=COUNTIFS({HOUR},{L(14+j)}21)")
spl["M22"] = "Minutes"; spl["M23"] = "Delays"

for c in spl[9] + spl[23] + spl[29]:
    if c.value: c.font = f(10, True)
for col, w in zip("ABCDEFGHIJKLM", [32, 12, 10, 14, 14, 2, 34, 10, 9, 9, 10, 2, 26]):
    spl.column_dimensions[col].width = w

# ---------------------------------------------------------------- shared look
def paint(ws, rows, cols, color):
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            ws.cell(r, c).fill = fill(color)

def bib(ws, r, c, w, label, formula, fmt, sub, strip, num=None):
    """A race-bib KPI: coloured sponsor strip, pin holes, huge condensed number, tear-off line."""
    c2 = c + w - 1
    for rr in range(r, r + 5):
        for cc in range(c, c2 + 1):
            ws.cell(rr, cc).fill = fill(C["bib"])
    for cc in range(c, c2 + 1):
        ws.cell(r, cc).fill = fill(strip)
        ws.cell(r + 4, cc).border = Border(top=Side(style="dashed", color=C["muted"]))
    ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c2)
    s = ws.cell(r, c, label); s.font = f(9, True, "FFFFFF" if strip not in (C["volt"], LINECOL["Line 1"]) else C["ink"], HEAD); s.alignment = AL("center")
    ws.cell(r + 1, c, "●").font = f(7, False, C["pin"]); ws.cell(r + 1, c).alignment = AL("left", "top", indent=0)
    ws.cell(r + 1, c2, "●").font = f(7, False, C["pin"]); ws.cell(r + 1, c2).alignment = AL("right", "top")
    ws.merge_cells(start_row=r + 2, start_column=c, end_row=r + 2, end_column=c2)
    v = ws.cell(r + 2, c, formula); v.font = f(30, True, C["ink"], HEAD); v.number_format = fmt; v.alignment = AL("center")
    ws.merge_cells(start_row=r + 3, start_column=c, end_row=r + 3, end_column=c2)
    t = ws.cell(r + 3, c, sub); t.font = f(8.5, False, C["muted"]); t.alignment = AL("center", "top", wrap_text=True)
    ws.merge_cells(start_row=r + 4, start_column=c, end_row=r + 4, end_column=c2)
    if num: ws.cell(r + 4, c, num).font = f(7.5, True, C["muted"], HEAD); ws.cell(r + 4, c).alignment = AL("center")

def axis_font(ax, sz=900, color=None, bold=False):
    ax.txPr = RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=CharacterProperties(sz=sz, b=bold, solidFill=color or C["muted"], latin=DFont(typeface=BODY))), endParaRPr=CharacterProperties())])

def chart_base(ch, w, h):
    ch.width = w; ch.height = h; ch.style = 2
    ch.graphical_properties = GraphicalProperties(); ch.graphical_properties.noFill = True
    ch.graphical_properties.line.noFill = True
    ch.plot_area.graphicalProperties = GraphicalProperties(); ch.plot_area.graphicalProperties.noFill = True
    return ch

def section(ws, r, c, kicker, title, color=None):
    ws.cell(r, c, kicker).font = f(9, True, C["accent"], HEAD)
    ws.cell(r + 1, c, title).font = f(17, True, color or C["ink"], HEAD)

# ---------------------------------------------------------------- RACE DAY
race.sheet_view.showGridLines = False; race.sheet_view.zoomScale = 100
paint(race, 120, 26, C["ground"])
race.column_dimensions["A"].width = 3
for i in range(2, 26): race.column_dimensions[L(i)].width = 9.2
race.column_dimensions["Z"].width = 3

banner = XLImage("/home/claude/ttc/art/banner.png"); banner.width, banner.height = PAL["banner_px"]
race.add_image(banner, "A1")
top = PAL["banner_rows"] + 1
for r in range(1, top): race.row_dimensions[r].height = 20

# subtitle strip
race.merge_cells(start_row=top, start_column=2, end_row=top, end_column=24)
race.cell(top, 2, '="Every Toronto subway delay that stopped a train, "&TEXT(Splits!B3,"mmmm yyyy")&" to "&TEXT(Splits!B4,"mmmm yyyy")&". Source: City of Toronto Open Data."').font = f(10, False, C["muted"], italic=True)
race.row_dimensions[top].height = 22

# bibs
br = top + 2
bibs = [
    ("MINUTES LOST", "=Splits!B6", "#,##0", '="That is "&TEXT(Splits!B6/60/24,"0")&" full days of stopped trains"', C["track"], "No. 01"),
    ("DELAYS", "=Splits!B7", "#,##0", '="About "&TEXT(Splits!B7/Splits!B5,"0")&" every single day"', C["lane"], "No. 02"),
    ("AVERAGE STOP", "=Splits!B6/Splits!B7", '0.0" min"', '="Half of all stops last "&TEXT(MEDIAN(' + MIN + '),"0")&" min or less"', C["ink"], "No. 03"),
    ("PEOPLE, NOT TRAINS", "=Splits!B21", "0%", '="of lost minutes: security, medical, track-level and false alarms"', C["accent"], "No. 04"),
    ("WORST STATION", f"=INDEX(Splits!G2:G{se},MATCH(MAX(Splits!H2:H{se}),Splits!H2:H{se},0))", "@",
     f'=TEXT(MAX(Splits!H2:H{se}),"#,##0")&" minutes lost"', LINECOL["Line 2"], "No. 05"),
    ("PEAK DELAY HOUR", f'=TEXT(TIME(INDEX(Splits!N21:AH21,MATCH(MAX(Splits!N23:AH23),Splits!N23:AH23,0)),0,0),"h AM/PM")', "@",
     f'=TEXT(MAX(Splits!N23:AH23),"#,##0")&" delays started in this hour"', LINECOL["Line 4"], "No. 06"),
]
for i, (lab, fm, fmt, sub, strip, num) in enumerate(bibs):
    bib(race, br, 2 + i * 4, 3, lab, fm, fmt, sub, strip, num)
race.row_dimensions[br].height = 20; race.row_dimensions[br + 1].height = 8
race.row_dimensions[br + 2].height = 46; race.row_dimensions[br + 3].height = 34; race.row_dimensions[br + 4].height = 14
for i in range(len(bibs)):
    race.cell(br + 2, 2 + i * 4 + 0)  # keep
# shrink worst station / hour text so names fit
for i in (4, 5):
    race.cell(br + 2, 2 + i * 4).font = f(20, True, C["ink"], HEAD)

# Lane race (minutes by line)
r0 = br + 7
section(race, r0, 2, "LEG 1", "The lanes: hours lost on each line")
for rr in range(r0 + 2, r0 + 3): race.row_dimensions[rr].height = 6
ch = BarChart(); ch.type = "bar"; ch.gapWidth = 35
ch.add_data(Reference(spl, min_col=5, min_row=23, max_row=26), titles_from_data=True)
ch.set_categories(Reference(spl, min_col=1, min_row=24, max_row=26))
from openpyxl.chart.marker import DataPoint
s = ch.series[0]
for idx, ln in enumerate(lines):
    pt = DataPoint(idx=idx); pt.graphicalProperties.solidFill = LINECOL[ln]; pt.graphicalProperties.line.noFill = True; s.dPt.append(pt)
s.dLbls = DataLabelList(); s.dLbls.showVal = True; s.dLbls.showSerName = False; s.dLbls.showCatName = False; s.dLbls.showLegendKey = False
s.dLbls.numFmt = '#,##0" hrs"'
s.dLbls.txPr = RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=CharacterProperties(sz=1100, b=True, solidFill=C["ink"], latin=DFont(typeface=HEAD))), endParaRPr=CharacterProperties())])
ch.x_axis.scaling.orientation = "maxMin"; ch.y_axis.delete = True; ch.y_axis.majorGridlines = None
ch.x_axis.delete = False; axis_font(ch.x_axis, 1100, C["ink"], True); ch.legend = None
chart_base(ch, 15.5, 6.2); race.add_chart(ch, f"B{r0+3}")

# Cause pareto
section(race, r0, 13, "LEG 2", "What slows the race: causes by minutes lost")
cp = BarChart(); cp.type = "bar"; cp.gapWidth = 30
cp.add_data(Reference(spl, min_col=2, min_row=9, max_row=ce), titles_from_data=True)
cp.set_categories(Reference(spl, min_col=1, min_row=10, max_row=ce))
s = cp.series[0]
for idx, cs in enumerate(causes):
    pt = DataPoint(idx=idx); pt.graphicalProperties.solidFill = C["accent"] if cs in people else C["steel"]; pt.graphicalProperties.line.noFill = True; s.dPt.append(pt)
s.dLbls = DataLabelList(); s.dLbls.showVal = True; s.dLbls.showSerName = False; s.dLbls.showCatName = False; s.dLbls.showLegendKey = False
s.dLbls.txPr = RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=CharacterProperties(sz=850, b=True, solidFill=C["ink"], latin=DFont(typeface=BODY))), endParaRPr=CharacterProperties())])
cp.x_axis.scaling.orientation = "maxMin"; cp.y_axis.delete = True; cp.y_axis.majorGridlines = None
cp.x_axis.delete = False; axis_font(cp.x_axis, 850, C["ink"]); cp.legend = None
chart_base(cp, 18.5, 9.6); race.add_chart(cp, f"M{r0+3}")
race.cell(r0 + 22, 13, "Red bars are people-related causes. Grey bars are equipment, track, operations and other.").font = f(8.5, False, C["muted"], italic=True)

# Split board: monthly minutes
r1 = r0 + 16
section(race, r1, 2, "LEG 3", "Split times: minutes lost each month")
lc = BarChart(); lc.type = "col"; lc.gapWidth = 40
lc.add_data(Reference(spl, min_col=2, min_row=29, max_row=me), titles_from_data=True)
lc.set_categories(Reference(spl, min_col=3, min_row=30, max_row=me))
lc.series[0].graphicalProperties.solidFill = C["lane"]; lc.series[0].graphicalProperties.line.noFill = True
jan = months.index("2026-01")
pt = DataPoint(idx=jan); pt.graphicalProperties.solidFill = C["accent"]; pt.graphicalProperties.line.noFill = True; lc.series[0].dPt.append(pt)
lc.y_axis.delete = False; lc.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill=C["rule"]))
lc.y_axis.number_format = "#,##0"; axis_font(lc.y_axis, 800); axis_font(lc.x_axis, 750); lc.x_axis.delete = False; lc.legend = None
chart_base(lc, 15.5, 6.6); race.add_chart(lc, f"B{r1+3}")
race.cell(r1 + 17, 2, '="January 2026 spike: a two-day snowstorm on 25 and 26 January cost "&TEXT(SUMIFS(' + MIN + ',' + CAUSE + ',"Weather",' + MON + ',"2026-01"),"#,##0")&" weather minutes."').font = f(8.5, False, C["muted"], italic=True)

# When to ride heatmap
r2 = r1 + 20
section(race, r2, 2, "LEG 4", "When to ride: delays by day and hour (darker means more delays)")
hr = r2 + 3
race.cell(hr, 2, "").fill = fill(C["ground"])
for j, h in enumerate(hours):
    c = race.cell(hr, 4 + j, hlab(h)); c.font = f(8, True, C["muted"], HEAD); c.alignment = AL("center")
for i, dy in enumerate(days):
    race.merge_cells(start_row=hr + 1 + i, start_column=2, end_row=hr + 1 + i, end_column=3)
    c = race.cell(hr + 1 + i, 2, dy); c.font = f(9.5, True, C["ink"], HEAD); c.alignment = AL("left")
    race.row_dimensions[hr + 1 + i].height = 19
    for j in range(len(hours)):
        c = race.cell(hr + 1 + i, 4 + j, f"=Splits!{L(14+j)}{3+i}")
        c.font = f(7.5, False, C["ink"]); c.alignment = AL("center"); c.number_format = "0"
        c.border = Border(left=side(C["ground"], "thin"), right=side(C["ground"], "thin"), top=side(C["ground"], "thin"), bottom=side(C["ground"], "thin"))
for j in range(len(hours)): race.column_dimensions[L(4 + j)].width = max(race.column_dimensions[L(4 + j)].width or 0, 9.2)
heat = f"D{hr+1}:{L(3+len(hours))}{hr+7}"
race.conditional_formatting.add(heat, ColorScaleRule(start_type="min", start_color=C["heat0"], mid_type="percentile", mid_value=60, mid_color=C["heat1"], end_type="max", end_color=C["heat2"]))
race.conditional_formatting.add(heat, FormulaRule(formula=[f"D{hr+1}>=PERCENTILE($D${hr+1}:${L(3+len(hours))}${hr+7},0.75)"], font=Font(color="FFFFFF", bold=True)))
race.cell(hr + 8, 2, "Each square counts delays that started in that hour across the whole period. Weekday rush hours and Sunday mornings stand out.").font = f(8.5, False, C["muted"], italic=True)

# Leaderboard (results board) top 10 stations
r3 = hr + 10
section(race, r3, 2, "LEG 5", "Results board: the ten stations losing the most time")
lb = r3 + 3
heads = ["POS", "STATION", "", "", "LINE", "DELAYS", "MINUTES", "AVG STOP"]
for j, h in enumerate(heads):
    c = race.cell(lb, 2 + j, h); c.font = f(9, True, C["volt"], HEAD); c.fill = fill(C["board"]); c.alignment = AL("center" if j not in (1,) else "left")
race.merge_cells(start_row=lb, start_column=3, end_row=lb, end_column=5)
for k in range(10):
    rr = lb + 1 + k
    race.row_dimensions[rr].height = 19
    vals = [k + 1, f"=Splits!G{2+k}", None, None, f"=Splits!K{2+k}", f"=Splits!I{2+k}", f"=Splits!H{2+k}", f"=Splits!J{2+k}"]
    fm = ["0", "@", None, None, "@", "#,##0", "#,##0", "0.0"]
    for j, v in enumerate(vals):
        c = race.cell(rr, 2 + j)
        if v is not None: c.value = v
        c.fill = fill(C["board"] if k % 2 == 0 else C["board2"])
        c.font = f(10, j in (0, 1, 6), "FFFFFF" if j != 0 else C["volt"], HEAD if j in (0, 1) else BODY)
        c.alignment = AL("center" if j not in (1,) else "left")
        if fm[j]: c.number_format = fm[j]
    race.merge_cells(start_row=rr, start_column=3, end_row=rr, end_column=5)
for k in range(-1, 10):
    rr = lb + 1 + k
    race.merge_cells(start_row=rr, start_column=10, end_row=rr, end_column=12)
    c = race.cell(rr, 10)
    c.fill = fill(C["board"] if k % 2 == 0 or k == -1 else C["board2"])
    if k == -1:
        c.value = "TIME LOST"; c.font = f(9, True, C["volt"], HEAD); c.alignment = AL("left")
    else:
        c.value = f'=REPT("█",ROUND(14*H{rr}/MAX($H${lb+1}:$H${lb+10}),0))'; c.font = f(9, False, C["accent"]); c.alignment = AL("left")
    for cc in (11, 12): race.cell(rr, cc).fill = fill(C["board"] if k % 2 == 0 or k == -1 else C["board2"])
for ln, col in LINECOL.items():
    race.conditional_formatting.add(f"F{lb+1}:F{lb+10}", FormulaRule(formula=[f'$F{lb+1}="{ln}"'], font=Font(color=col, bold=True)))

from openpyxl.chart import AreaChart
for j, h in enumerate(hours): spl.cell(24, 14 + j, hlab(h))
spl["M24"] = "Label"
section(race, r3, 14, "LEG 6", "Course profile: minutes lost by hour of day")
ac = AreaChart(); ac.grouping = "standard"
ac.add_data(Reference(spl, min_col=13, max_col=13 + len(hours), min_row=22), from_rows=True, titles_from_data=True)
ac.set_categories(Reference(spl, min_col=14, max_col=13 + len(hours), min_row=24))
ac.series[0].graphicalProperties.solidFill = C["track"]; ac.series[0].graphicalProperties.line.solidFill = C["board"]
ac.y_axis.delete = False; ac.x_axis.delete = False; ac.y_axis.number_format = "#,##0"
ac.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill=C["rule"]))
axis_font(ac.y_axis, 800); axis_font(ac.x_axis, 800); ac.legend = None
chart_base(ac, 17.5, 6.4); race.add_chart(ac, f"N{r3+3}")
race.cell(lb + 12, 14, "The 5 a.m. peak is start-of-service track and signal trouble; the 4 to 6 p.m. climb is the evening rush.").font = f(8.5, False, C["muted"], italic=True)

# Finish: what to do with it
fx = lb + 13
race.merge_cells(start_row=fx, start_column=2, end_row=fx + 2, end_column=24)
c = race.cell(fx, 2, '="The finish line: "&TEXT(Splits!B21,"0%")&" of lost time is about people, not machines. Faster medical response, more station staff and clearer alarm education would win back more minutes than train repairs alone. To plan your own ride, open the Plan My Ride tab."')
c.font = f(11, True, "FFFFFF", HEAD); c.fill = fill(C["track"]); c.alignment = AL("left", "center", wrap_text=True, indent=1)
for rr in range(fx, fx + 3):
    for cc in range(2, 25): race.cell(rr, cc).fill = fill(C["track"])
race.cell(fx + 4, 2, "Built by Jeffrey Okonkwo, CBAP, CSM, PL-300. Not affiliated with the TTC. Data: TTC Subway Delay Data, City of Toronto Open Data, Open Government Licence - Toronto.").font = f(8, False, C["muted"])
race.print_area = f"A1:Z{fx+4}"
race.page_setup.orientation = "portrait"; race.page_setup.fitToWidth = 1; race.page_setup.fitToHeight = 0
race.sheet_properties.pageSetUpPr.fitToPage = True
race.sheet_properties.tabColor = C["accent"]

# ---------------------------------------------------------------- PLAN MY RIDE
plan.sheet_view.showGridLines = False
paint(plan, 60, 16, C["ground"])
plan.column_dimensions["A"].width = 3
for i in range(2, 16): plan.column_dimensions[L(i)].width = 11
ic = XLImage("/home/claude/ttc/art/tayo_badge.png"); ic.width, ic.height = PAL["badge_px"]
plan.add_image(ic, "B2")
plan["E2"] = "Plan My Ride"; plan["E2"].font = f(30, True, C["ink"], HEAD); plan["E2"].alignment = AL("left","bottom")
plan["E4"] = "Pick your station, day and the hour you usually board. Tayo checks 20 months of real delays and tells you how much buffer to leave."
plan["E4"].font = f(10.5, False, C["muted"]); plan.merge_cells("E4:N5"); plan["E4"].alignment = AL("left", "top", wrap_text=True)
for r in range(1, 7): plan.row_dimensions[r].height = 22
plan.row_dimensions[2].height = 42

# lists for dropdowns
lst = wb.create_sheet("Lists")
for i, s in enumerate(stations_sorted, 1): lst.cell(i, 1, s)
for i, dy in enumerate(days, 1): lst.cell(i, 2, dy)
for i, h in enumerate(hours, 1):
    lst.cell(i, 3, f'{(h % 12) or 12}:00 {"AM" if h < 12 else "PM"}'); lst.cell(i, 4, h)
lst.sheet_state = "hidden"

inputs = [("YOUR STATION", "Bloor-Yonge", f"=Lists!$A$1:$A${len(stations_sorted)}"),
          ("YOUR DAY", "Monday", f"=Lists!$B$1:$B$7"),
          ("YOU BOARD AROUND", "8:00 AM", f"=Lists!$C$1:$C${len(hours)}")]
for i, (lab, val, src) in enumerate(inputs):
    c0 = 2 + i * 4
    plan.merge_cells(start_row=8, start_column=c0, end_row=8, end_column=c0 + 2)
    plan.cell(8, c0, lab).font = f(9, True, C["accent"], HEAD)
    plan.merge_cells(start_row=9, start_column=c0, end_row=10, end_column=c0 + 2)
    v = plan.cell(9, c0, val); v.font = f(16, True, C["ink"], HEAD); v.alignment = AL("center")
    for rr in (9, 10):
        for cc in range(c0, c0 + 3):
            plan.cell(rr, cc).fill = fill(C["bib"])
            plan.cell(rr, cc).border = Border(top=side(C["ink"], "medium") if rr == 9 else None, bottom=side(C["ink"], "medium") if rr == 10 else None,
                                             left=side(C["ink"], "medium") if cc == c0 else None, right=side(C["ink"], "medium") if cc == c0 + 2 else None)
    dv = DataValidation(type="list", formula1=src, allow_blank=False); dv.prompt = "Choose from the list"; dv.promptTitle = lab.title()
    plan.add_data_validation(dv); dv.add(plan.cell(9, c0).coordinate)
plan.cell(11, 2, "Change the three outlined boxes. Everything below updates.").font = f(8.5, False, C["muted"], italic=True)

# model cells (hidden columns P..)
plan["P1"] = "hour"; plan["Q1"] = '=INDEX(Lists!$D:$D,MATCH($J$9,Lists!$C:$C,0))'
plan["P2"] = "delays here"; plan["Q2"] = f'=COUNTIFS({STN},$B$9,{DAY},$F$9,{HOUR},$Q$1)'
plan["P3"] = "days of this weekday"; plan["Q3"] = '=INDEX(Splits!$N$13:$N$19,MATCH($F$9,Splits!$M$13:$M$19,0))'
plan["P4"] = "per 100 trips"; plan["Q4"] = "=IFERROR(100*Q2/Q3,0)"
plan["P5"] = "avg stop here at this hour"; plan["Q5"] = f'=IFERROR(AVERAGEIFS({MIN},{STN},$B$9,{HOUR},$Q$1),IFERROR(AVERAGEIFS({MIN},{STN},$B$9),0))'
plan["P6"] = "station avg per 100 slots"; plan["Q6"] = f'=IFERROR(100*COUNTIFS({STN},$B$9)/(Splits!$B$5*19),0)'
plan["P7"] = "risk ratio"; plan["Q7"] = "=IFERROR(Q4/Q6,0)"
plan["P8"] = "buffer"; plan["Q8"] = '=IF(Q2=0,0,MAX(5,CEILING(ROUND(Q5,0),5)))'
plan["P9"] = "line"; plan["Q9"] = f'=INDEX(Splits!$K$2:$K${se},MATCH($B$9,Splits!$G$2:$G${se},0))'
plan.column_dimensions["P"].hidden = True; plan.column_dimensions["Q"].hidden = True
for k, cs in enumerate(causes):
    plan.cell(20 + k, 16, cs); plan.cell(20 + k, 17, f'=COUNTIFS({STN},$B$9,{CAUSE},P{20+k})')
cause_end = 19 + len(causes)

# verdict banner
plan.merge_cells("B13:M15")
v = plan["B13"]
v.value = ('=IF(Q7<0.75,"GREEN LIGHT: this is one of the calmer times to ride from "&B9&".",'
           'IF(Q7<1.5,"STEADY PACE: about normal for "&B9&". Leave a small buffer.",'
           '"HEADWIND: delays cluster at this time at "&B9&". Leave early or shift your trip."))')
v.font = f(15, True, "FFFFFF", HEAD); v.alignment = AL("left", "center", wrap_text=True, indent=1)
for rr in range(13, 16):
    for cc in range(2, 14): plan.cell(rr, cc).fill = fill(C["ink"])
plan.conditional_formatting.add("B13:M15", FormulaRule(formula=["$Q$7<0.75"], fill=fill(LINECOL["Line 2"])))
plan.conditional_formatting.add("B13:M15", FormulaRule(formula=["AND($Q$7>=0.75,$Q$7<1.5)"], fill=fill(C["lane"])))
plan.conditional_formatting.add("B13:M15", FormulaRule(formula=["$Q$7>=1.5"], fill=fill(C["track"])))

pbibs = [
    ("DELAYS IN THIS SLOT", "=Q2", "0", '="Over "&Q3&" "&F9&"s since "&TEXT(Splits!B3,"mmm yyyy")', C["lane"]),
    ("DELAY RATE", "=Q4", '0" per 100"', '="Delays per 100 "&F9&"s at this hour"', C["track"]),
    ("TYPICAL STOP", "=Q5", '0" min"', '="When a delay happens here"', C["ink"]),
    ("LEAVE THIS EARLY", "=Q8", '0" min"', '="Buffer to beat a typical delay"', C["accent"]),
]
for i, (lab, fm, fmt, sub, strip) in enumerate(pbibs):
    bib(plan, 17, 2 + i * 3, 3, lab, fm, fmt, sub, strip)
for r, h in zip(range(17, 22), [20, 8, 46, 30, 12]): plan.row_dimensions[r].height = h

plan["B23"] = "MOST COMMON REASON AT THIS STATION"; plan["B23"].font = f(9, True, C["accent"], HEAD)
plan.merge_cells("B24:M24")
plan["B24"] = f'=IF(MAX(Q20:Q{cause_end})=0,"No delays recorded",INDEX(P20:P{cause_end},MATCH(MAX(Q20:Q{cause_end}),Q20:Q{cause_end},0))&"  ("&MAX(Q20:Q{cause_end})&" of "&SUM(Q20:Q{cause_end})&" delays)")'
plan["B24"].font = f(16, True, C["ink"], HEAD)

plan["B26"] = "YOUR STATION, HOUR BY HOUR ON THIS DAY (number of delays)"; plan["B26"].font = f(9, True, C["accent"], HEAD)
for j, h in enumerate(hours):
    col = 2 + (j % 11) * 1
for j, h in enumerate(hours):
    row = 27 if j < 11 else 30
    cc = 2 + (j if j < 11 else j - 11)
    a = plan.cell(row, cc, hlab(h)); a.font = f(8, True, C["muted"], HEAD); a.alignment = AL("center")
    b = plan.cell(row + 1, cc, f'=COUNTIFS({STN},$B$9,{DAY},$F$9,{HOUR},{h})'); b.font = f(11, True, C["ink"], HEAD); b.alignment = AL("center")
    b.border = Border(left=side(C["ground"], "medium"), right=side(C["ground"], "medium"))
    plan.cell(row + 1, cc).number_format = "0"
    plan.conditional_formatting.add(b.coordinate, FormulaRule(formula=[f"$Q$1={h}"], fill=fill(C["accent"]), font=Font(color="FFFFFF", bold=True), border=Border(top=side(C["ink"], "thick"), bottom=side(C["ink"], "thick"), left=side(C["ink"], "thick"), right=side(C["ink"], "thick"))))
plan["P12"] = "max hour"; plan["Q12"] = "=MAX(MAX(B28:L28),MAX(B31:K31),1)"
for rng in ("B28:L28", "B31:K31"):
    plan.conditional_formatting.add(rng, FormulaRule(formula=[f"{rng[:3]}>=0.6*$Q$12"], font=Font(color="FFFFFF")))
    plan.conditional_formatting.add(rng, ColorScaleRule(start_type="num", start_value=0, start_color=C["heat0"], mid_type="formula", mid_value="$Q$12*0.5", mid_color=C["heat1"], end_type="formula", end_value="$Q$12", end_color=C["heat2"]))
plan.row_dimensions[28].height = 26; plan.row_dimensions[31].height = 26
plan["B33"] = "The red square is the hour you picked. Lighter squares are calmer hours to travel from this station."
plan["B33"].font = f(8.5, False, C["muted"], italic=True)
plan["B35"] = "How it works: counts are real delays from the Delays tab for this station, weekday and hour. Delay rate = delays in the slot for every 100 of that weekday in the period. The verdict compares this slot with the station's average hour. Buffer = typical stop rounded up to the next 5 minutes."
plan.merge_cells("B35:M37"); plan["B35"].font = f(8.5, False, C["muted"]); plan["B35"].alignment = AL("left", "top", wrap_text=True)
plan.sheet_properties.tabColor = LINECOL["Line 2"]
plan.print_area = "A1:O38"; plan.page_setup.fitToWidth = 1; plan.page_setup.fitToHeight = 1; plan.sheet_properties.pageSetUpPr.fitToPage = True

# ---------------------------------------------------------------- READ ME
readme.sheet_view.showGridLines = False
readme.column_dimensions["B"].width = 110
rm = [
    ("Beat the Delay", f(22, True, C["ink"], HEAD)),
    ("What it is", f(12, True, C["accent"], HEAD)),
    ("A race-day view of every Toronto subway delay that stopped a train since January 2025, plus a daily trip planner. Built in Excel from the City of Toronto open data feed, ready to load into Power BI.", f(10)),
    ("The problem it tackles", f(12, True, C["accent"], HEAD)),
    ("Riders lose thousands of hours to delays, and most fixes focus on trains and track. This shows that about half of the lost time comes from people-related incidents, which points to staffing, medical response and alarm education as the fastest wins.", f(10)),
    ("How to use it every day", f(12, True, C["accent"], HEAD)),
    ("Open Plan My Ride, choose your station, day and boarding hour, and read the verdict and the buffer to leave.", f(10)),
    ("How it is built", f(12, True, C["accent"], HEAD)),
    ("1. Delays tab: the raw open data, filtered to delays longer than zero minutes and to Lines 1, 2 and 4. Station names were standardised (for example, Bloor and Yonge on Line 2 became Bloor-Yonge).", f(10)),
    ("2. Cause Codes tab: each TTC delay code grouped into ten plain-English causes. The grouping is my own and is listed in full.", f(10)),
    ("3. Splits tab: every number is a live SUMIFS or COUNTIFS on the Delays tab. Paste a newer month of data into the table and the dashboard updates.", f(10)),
    ("Data and licence", f(12, True, C["accent"], HEAD)),
    ("TTC Subway Delay Data (since 2025), City of Toronto Open Data, Open Government Licence - Toronto. https://open.toronto.ca/dataset/ttc-subway-delay-data/ . Not affiliated with or endorsed by the TTC.", f(10)),
    ("Character", f(12, True, C["accent"], HEAD)),
    ("Tayo, the commuter racing the train, is an original character drawn for this project.", f(10)),
]
for i, (txt, ft) in enumerate(rm, 2):
    c = readme.cell(i, 2, txt); c.font = ft; c.alignment = AL("left", "top", wrap_text=True)

wb.move_sheet("Lists", offset=10)
out = os.environ.get("OUT", "/mnt/user-data/outputs/Beat_the_Delay_TTC.xlsx")
wb.save(out); print(out, N)
