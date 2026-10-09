# Build Beat the Delay in Power BI

Everything you need is in this folder: four small dimension tables, one fact table, the DAX measures,
a colour theme and the Power Query script. Budget about 45 minutes the first time.

## Which route to take

| You are on | Route |
|---|---|
| Windows, or a Mac with Parallels or a Windows 365 cloud PC | Power BI Desktop (full build below) |
| A Mac, browser only | Power BI service at app.powerbi.com: create a semantic model from the files, then open it with "Open data model" to add relationships and measures. Desktop-only features (custom themes on import, some formatting) may be limited. |

A Power BI account needs a work or school email; a Gmail address is not accepted.

## Steps (Power BI Desktop)

1. **Load the data.** Get Data > Blank Query > Advanced Editor. Paste each block from `power_query.m`
   (BaseUrl first). Because the queries read from GitHub, Refresh always pulls the latest month.
2. **Create the date table.** Modeling > New table > paste `dim_date` from `measures.dax`. Mark it as a date table.
3. **Relationships** (Model view, many to one, single direction):
   `fact_delays[Date] -> dim_date[Date]`, `[Station] -> dim_station[Station]`, `[Cause] -> dim_cause[Cause]`,
   `[Line] -> dim_line[Line]`, `[Hour] -> dim_hour[Hour]`.
4. **Sort columns.** dim_hour[Hour Label] by Service Order, dim_cause[Cause] by Cause Sort,
   dim_date[Weekday] by Weekday Number, dim_date[Month] by Month Start.
5. **Measures.** Home > Enter data > table named `_Measures`. Add every measure from `measures.dax`.
6. **Theme.** View > Themes > Browse for themes > `BeatTheDelay.theme.json`.

## Page 1: Race Day

| Visual | Fields |
|---|---|
| Slicer (tiles) | dim_line[Line] |
| Six cards | Hours Lost, Delays, Average Stop (min), People Share, Worst Station, Peak Delay Hour |
| Bar chart: what slows the race | Y: dim_cause[Cause], X: Minutes Lost, colour by dim_cause[Cause Type] (red for People-related) |
| Area chart: course profile | X: dim_hour[Hour Label], Y: Minutes Lost |
| Matrix heatmap: when to ride | Rows: dim_date[Weekday], Columns: dim_hour[Hour Label], Values: Delays, background colour scale |
| Column chart: split times | X: dim_date[Month], Y: Minutes Lost, tooltip: Weather Minutes |
| Table: results board | Station, Delays, Minutes Lost (data bars), Average Stop; Top N 10 by Minutes Lost |

## Page 2: Plan My Ride

Slicers for dim_station[Station], dim_date[Weekday] and dim_hour[Hour Label] (single select).
Cards: Verdict (font colour from the Verdict Colour measure), Delays, Delay Rate per 100 Days,
Average Stop (min), Buffer (min). Add a column chart of Delays by Hour Label filtered to the chosen station.

## Check your numbers

With no filters you should see 2,033 hours lost, 15,800 delays, a 7.7 minute average stop and a 51% people share.
If a number differs, check the relationships and that Minutes is a whole number.
