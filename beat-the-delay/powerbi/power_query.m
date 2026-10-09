// Beat the Delay: Power Query (M) for Power BI
// Get Data > Blank Query > Advanced Editor, paste one block per table, name the query as shown.
// The files are read straight from GitHub, so a scheduled refresh in the Power BI service
// picks up each monthly update with no manual work.

// ---- Query name: BaseUrl  (a text parameter)
"https://raw.githubusercontent.com/JeffreyOkonkwo/JeffreyOkonkwo/main/beat-the-delay/powerbi/"

// ---- Query name: fact_delays
let
    Source = Csv.Document(Web.Contents(BaseUrl & "fact_delays.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Headers, {
        {"Date", type date}, {"Hour", Int64.Type}, {"Line", type text}, {"Station", type text},
        {"Cause", type text}, {"Code", type text}, {"Minutes", Int64.Type}, {"Gap Minutes", Int64.Type}, {"Bound", type text}
    }, "en-CA")
in
    Typed

// ---- Query name: dim_station
let
    Source = Csv.Document(Web.Contents(BaseUrl & "dim_station.csv"), [Delimiter = ",", Encoding = 65001]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true])
in
    Headers

// ---- Query name: dim_cause
let
    Source = Csv.Document(Web.Contents(BaseUrl & "dim_cause.csv"), [Delimiter = ",", Encoding = 65001]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Headers, {{"Cause Sort", Int64.Type}})
in
    Typed

// ---- Query name: dim_line
let
    Source = Csv.Document(Web.Contents(BaseUrl & "dim_line.csv"), [Delimiter = ",", Encoding = 65001]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Headers, {{"Sort", Int64.Type}})
in
    Typed

// ---- Query name: dim_hour
let
    Source = Csv.Document(Web.Contents(BaseUrl & "dim_hour.csv"), [Delimiter = ",", Encoding = 65001]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Headers, {{"Hour", Int64.Type}, {"Service Order", Int64.Type}})
in
    Typed
