# Power BI: Will My Vote Count?

A finished Power BI project: four designed pages, a dark theme, a star-schema model with 20 DAX measures, and Power Query that loads straight from this GitHub folder. You open it; you do not build it.

![Command centre page](../assets/powerbi_command.png)

## Open it (Windows on your Mac)

1. **Merge the GitHub branch first.** The model loads its data from `main`, so the files must be there.
2. Install **Power BI Desktop** from the Microsoft Store (free).
3. In Power BI Desktop: **File > Options and settings > Options > Preview features**, tick **Power BI Project (.pbip) save option** and **Store reports using enhanced metadata format (PBIR)** if they are listed, then restart. Newer versions have these on by default.
4. Download this repository (green **Code** button > **Download ZIP**), unzip it, and open `will-my-vote-count/powerbi/project/WillMyVoteCount.pbip`.
5. Click **Refresh**. If asked how to connect to GitHub, choose **Anonymous** and privacy level **Public**.

To work offline or from another folder, change the **DataRoot** parameter (Transform data > Manage parameters).

## Pages

| Page | What it answers | Visuals |
|---|---|---|
| Overview | Where in the process run by INEC (Nigeria's electoral commission) does the fear sit? | KPI cards, journey of one vote by step (the top step turns red), four biggest fears, worst 2023 states |
| Fear explorer | Which fears, on which channels, and when? | Channel, step and month slicers, theme ranking, decomposition tree (theme, then channel, then video), monthly trend, share against breadth scatter |
| 2023 evidence | Was the fear justified? | Problem cards, stacked bar of all 37 states by problem type, treemap of problem types, state table |
| Fix tracker | What should change, and who must act? | Fix counts, timing and owner slicers, full fix table, fixes by owner |

Panel titles and the paper art are drawn into each page background, so the visuals sit on a designed canvas.

## Model

| Table | Role | Rows |
|---|---|---|
| fact_comments | One row per fear comment (month, platform, channel, source, tone) | 1,343 |
| fact_comment_theme | Bridge: comment to theme (a comment can name several) | 1,704 |
| dim_theme | 15 fear themes, step, 2023 baseline share | 15 |
| dim_step | Seven INEC process steps, what fails, evidence | 7 |
| dim_video | Videos, posts and threads sampled, with platform and comments read | 105 |
| fact_results_2023 | 2023 IReV result sheets by state | 37 |
| fact_problem | The same data unpivoted in Power Query by problem type | 111 |
| dim_fix | 15 proposed fixes with owner and timing | 15 |

Relationships: fact_comment_theme to fact_comments (both directions, so theme and step filters reach comments), fact_comment_theme to dim_theme, dim_theme to dim_step, fact_comments to dim_video, fact_problem to fact_results_2023, dim_fix to dim_step.

## Key measures

```DAX
Theme Share =
DIVIDE (
    CALCULATE ( DISTINCTCOUNT ( fact_comment_theme[comment_id] ) ),
    CALCULATE ( DISTINCTCOUNT ( fact_comments[comment_id] ), REMOVEFILTERS ( dim_theme ), REMOVEFILTERS ( dim_step ) )
)

After The Vote Share =
DIVIDE (
    CALCULATE ( DISTINCTCOUNT ( fact_comment_theme[comment_id] ), dim_step[order] IN { 5, 6, 7 } ),
    CALCULATE ( DISTINCTCOUNT ( fact_comments[comment_id] ), REMOVEFILTERS ( dim_theme ), REMOVEFILTERS ( dim_step ) )
)

Step Colour =   // conditional formatting: the most feared step turns red
VAR Top = MAXX ( ALLSELECTED ( dim_step[short], dim_step[order] ), [Theme Share] )
RETURN IF ( [Theme Share] = Top, "#F2563F", "#00B36B" )
```

All measures are in `measures.dax` and inside the model.

## Expected totals (no filters)

Comments collected 4,864; comments raising a specific concern 1,343; after the vote 62%; rigging (mapped to collation) 38%; upload 15%; post-election courts 14%; 2023 problem share 14.1% (24,962 of 176,846 units); fixes 15; quick wins 12. Shares leave out keyword search results (the hidden `searched` flag), so they match the README.

## If something does not open

The project files follow Microsoft's published PBIR schemas and open in Power BI Desktop as they are. If your version reports an error, update Power BI Desktop from the Microsoft Store. As a fallback, `power_query.m` and `measures.dax` hold every query and measure, so the model can be rebuilt in a blank report.
