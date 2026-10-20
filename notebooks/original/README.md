# Original working notebooks (archived, unedited except outputs cleared)

These are the exploratory Colab notebooks as written during the project. Cell outputs were
stripped so no review text is published. They read from a private Google Drive, so they are
**not runnable as-is**. The reproducible version of the analysis is `src/analysis.py`.

Known issues, kept for transparency and fixed or tested in `src/analysis.py`:

| Notebook | Issue |
|---|---|
| `Combined_with_theme` | Keyword list mixes upper/lower case, but text is lowercased before matching, so some keywords never match. Output reproduces only ~69% of the final `Theme` labels (final labels were refined manually). |
| `Glassdoor_Sentiment_Analysis` | First scores a `cleaned_text` column that is never created, then overwrites it with `merged_all`. |
| `Glassdoor_keyword_analysis` | `str.replace('get', '')` also corrupts words containing "get"; uses `updated_freq_df`, which is never defined. |
| `Comparison_Sentiment_Analysis` | Stray cells reference an undefined `df` and would overwrite `Youtube_sentiment.csv`. |
| All notebooks | Most code was AI-generated and then run and adjusted by the author. See "AI assistance" in the main README. |
