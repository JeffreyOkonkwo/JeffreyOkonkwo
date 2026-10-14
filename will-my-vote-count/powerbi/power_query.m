// Power Query (M). Paste each block into a Blank Query named after the table.
// Reads straight from the GitHub repository, so Refresh picks up any update.
let
    Base = "https://raw.githubusercontent.com/JeffreyOkonkwo/JeffreyOkonkwo/main/will-my-vote-count/powerbi/",
    Load = (name as text) as table =>
        let
            Source = Csv.Document(Web.Contents(Base & name & ".csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
            Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true])
        in
            Promoted
in
    Load

// fact_comments
// = Table.TransformColumnTypes(LoadCsv("fact_comments"), {{"tone", type number}})
// fact_comment_theme  = LoadCsv("fact_comment_theme")
// dim_theme           = Table.TransformColumnTypes(LoadCsv("dim_theme"), {{"y2023_share", type number}})
// dim_step            = Table.TransformColumnTypes(LoadCsv("dim_step"), {{"order", Int64.Type}})
// dim_video           = Table.TransformColumnTypes(LoadCsv("dim_video"), {{"comments_read", Int64.Type}, {"fear_comments", Int64.Type}})
// fact_results_2023   = Table.TransformColumnTypes(LoadCsv("fact_results_2023"), {{"polling_units", Int64.Type}, {"readable", Int64.Type}, {"never_uploaded", Int64.Type}, {"unreadable", Int64.Type}, {"wrong_document", Int64.Type}, {"cancelled", Int64.Type}, {"missing_signature_or_stamp", Int64.Type}})
// dim_fix             = LoadCsv("dim_fix")
// Name the first block LoadCsv, then create each table as a Blank Query using the line shown.
