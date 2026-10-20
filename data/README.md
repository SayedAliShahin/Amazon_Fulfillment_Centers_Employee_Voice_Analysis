# Data

**Raw data is intentionally not in this repository.**

The analysis used 140 public Glassdoor reviews and 10 YouTube vlog transcripts about
Amazon fulfillment-center work. Both are third-party content, so republishing the raw
text may breach the platforms' terms and the authors' rights.

`aggregated/` contains the summary tables behind every chart in the README.

To reproduce locally, place your own labelled file anywhere and run:

    python src/analysis.py path/to/your_file.csv

Expected columns: `platform`, `sentiment_label`, `Theme`, `Segment`, `employee_job_title`,
`employee_status`, `rating_overall`, the `rating_*` sub-ratings, and the raw text columns
`summary`, `review_pros`, `review_cons`, `advice_to_management`.
