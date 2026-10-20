# Amazon Fulfillment Center Employee Voice Analysis

**What do fulfillment-center associates say about their work, and where should a retention effort start?**
A text-analytics and recommendation case study built from public employee reviews and vlogs.

> **Context.** Completed as part of a virtual externship (Extern, Amazon-themed program). The brief stated
> that associate turnover is around 150% per year. That figure was given as context, **it is not derived from
> the data used here.** All data is public third-party content. This is an independent portfolio project and is
> not affiliated with or endorsed by Amazon.
>
> **AI disclosure:** AI tools were used for code and drafting in this project. See [AI assistance](#ai-assistance).

---

## Summary

I analyzed 140 Glassdoor reviews and 10 YouTube vlog transcripts using sentiment analysis, n-gram frequency,
and theme/segment tagging, then proposed a low-cost, four-week pilot.

| Finding | Evidence |
|---|---|
| **Pay and benefits are the strongest positive.** | Highest-rated Glassdoor dimension (3.72 / 5). Mentioned in 78 of 150 items, and 49 of those are positive. |
| **Work-life balance and leadership are the weakest.** | Lowest-rated dimensions (3.08 and 3.12). 34% of raters gave work-life 1–2 stars, versus 15% for pay. |
| **Physical demands and long shifts are the most concrete complaint.** | 28 items (19%). Recurring words: "physically demanding", "long hours", breaks, mandatory overtime. |

**Recommendation:** pilot a **Scheduling Risk Management dashboard** that flags overtime, consecutive long
shifts, workload imbalance and last-minute schedule changes to area managers *before* schedules are finalized.

**Why scheduling, honestly:** the data does not prove scheduling is *the* primary cause of turnover (see
[Limitations](#limitations)). The case for starting there is that it is the most concrete, most actionable,
and cheapest-to-test friction, and a time-boxed pilot would generate the evidence.

---

## Data

| Source | Size | Used for |
|---|---|---|
| Glassdoor reviews of Amazon fulfillment-center roles | 140 | Sentiment, themes, segments, star ratings |
| YouTube warehouse-worker vlog transcripts | 10 | Sentiment, themes (no role information) |

Raw text is not published here (see [`data/README.md`](data/README.md)); aggregated tables are in
[`data/aggregated/`](data/aggregated/).

## Approach

```
raw text → clean (lowercase, stopwords, punctuation) → TextBlob sentiment (±0.1 threshold)
        → n-gram frequencies → theme tagging → segment tagging → recommendation
```

- **Sentiment:** TextBlob polarity. Above 0.1 is positive, below -0.1 is negative, otherwise neutral.
- **Themes (3):** *Pay & benefits*, *Physical demands & shift scheduling*, *Management & HR support*. A review can
  carry more than one. A keyword pass was refined by manual review, and **those manual edits were not logged**, so
  the final labels are not fully reproducible. The keyword code alone reproduces about 69% of them.
- **Segments:** assigned from `employee_status` and job title (Regular, Part-time, Contract, Pickers/Packers,
  Stowers, Managers, Other, Unknown). Glassdoor only, because YouTube has no role information.
- **AI use:** see [AI assistance](#ai-assistance) for exactly what was AI-generated and what I did.

**Guiding question:** *What workplace experiences influence fulfillment-center employees' decisions to stay or leave?*

## Findings

### 1. Employees are mostly positive, especially on Glassdoor
![Sentiment by platform](figures/01_sentiment_by_platform.png)

58% of Glassdoor reviews are positive versus 20% of YouTube items. **YouTube is only 10 videos (2 positive,
6 neutral, 2 negative), so this is a pattern to investigate, not a conclusion.** The hypothesis that employees
speak more freely on YouTube than Glassdoor is plausible but untested here.

### 2. Glassdoor's own star ratings back this up, and show where the friction is
![Sub-ratings](figures/02_glassdoor_subratings.png)

Star ratings are structured data, independent of text sentiment. Pay leads clearly. Work-life, leadership, culture
and career opportunities cluster between 3.1 and 3.3, and with about 85 raters each, differences within that
cluster are small. I treat them as one group of weaker areas, not a ranking.

### 3. Pay dominates the conversation, then physical demands
![Themes](figures/03_theme_counts.png)

Many positive reviews also mention hard work. A typical reviewer pairs "good pay" with the physical toll, which is
why even the demanding-work theme is mostly neutral or positive in tone (12 positive, 14 neutral, 2 negative).

> *"Long hours, minimal light, … mandatory overtime with little to no heads up."* — public Glassdoor review
> *"10-hour shifts and have to deal with heat and rain."* — public Glassdoor review

Top terms are in [`figures/ngrams/`](figures/ngrams/): "good pay" (18), "good benefits" (12),
"physically demanding" (7), "use break time" (3).

### 4. Regular associates are the largest segment, so they are the pilot population
![Segments](figures/04_segments.png)

Regular associates are 32% of Glassdoor reviews (45 of 140). They work alongside every other role (stowers,
pickers, packers, learning ambassadors, area managers), so changes to their schedules propagate.

## Recommendation: a four-week Scheduling Risk pilot

| | |
|---|---|
| **What** | Extend an existing workforce-management system or Power BI/Excel dashboard to flag overtime, consecutive long shifts, workload imbalance and schedule changes, with automated alerts to area managers before schedules are finalized. |
| **Who** | Area managers (act on alerts), Learning Ambassadors (introduce pilot, collect weekly associate feedback), a project lead (reports and scale-up decision). |
| **Where** | One fulfillment center, regular-associate teams. |

| Week | Activity |
|---|---|
| 0 | Configure dashboard in one FC, brief Learning Ambassadors |
| 1–4 | Managers monitor and act on alerts; associates give weekly feedback |
| 5 | Review metrics, decide: scale up, extend with adjustments, or reassess |

**Success criteria:** at least 20% fewer high-risk schedules reaching finalization, at least 50% positive
weekly associate feedback, and consistent manager use of the dashboard (logged weekly check-ins).
Not met: reassess the tool and process before any rollout.

*This is a proposal. It was not implemented, and no impact results exist.*

## AI assistance

I used AI tools throughout this project and want to be specific about where:

| Part | Tool | What I did |
|---|---|---|
| Research questions guiding the analysis | ChatGPT | Drafted five insight questions from my sentiment results and briefing note. I merged them with my own draft into one guiding question. |
| Original notebook code (cleaning, sentiment, n-grams, plots) | AI assistants, mainly ChatGPT | Most of the code was AI-generated. I ran it on my data, chose the thresholds and stopword handling, and assembled the pipeline. |
| Theme and segment labels | Manual (with a keyword first pass) | Final labels were refined by hand. The edits were not logged. |
| Consolidated script `src/analysis.py`, the sensitivity test, the aggregated tables, and the README | Claude (Anthropic) | Drafted from my notebooks, data, deck and notes. Claude also audited the original notebooks (see `notebooks/original/README.md`) and flagged where my deck's claims were stronger than the data. |
| Interpretation and recommendation | Me | The scheduling-pilot recommendation and its framing are mine, and I can explain every method and number in this repository. |

The aim of this section is transparency. Every figure and table can be regenerated with `python src/analysis.py`.

## Limitations

- **Small, non-random samples.** 140 reviews and 10 videos. Review sites skew toward people motivated to post.
- **Turnover is not measured.** Nothing here links sentiment to who actually left. The 150% figure is external context.
- **The "primary driver" claim is not proven.** Pay is mentioned most often. Scheduling matters as the weakest rated and
  most actionable area, but the gap between work-life, leadership and culture ratings is small.
- **Themes are loose.** The *Pay & benefits* keyword list also includes "balance", "opportunity" and "growth", so it
  is broader than pay. 61 of 150 items (41%) received no theme.
- **Sentiment is a lexicon method.** TextBlob misses sarcasm and context. A sensitivity check on raw text (negations
  kept) shifted Glassdoor positives from 58% to 62%, with 90% of individual labels unchanged
  ([figure](figures/05_sentiment_sensitivity.png)), so the main results hold.
- **Data quality.** Glassdoor stores "not rated" as 0 in sub-ratings. These were excluded. Without that, work-life
  would look like 2.1 / 5 instead of 3.1.
- **Root-cause tree.** [`figures/hypothesis/`](figures/hypothesis/) shows an explanatory model of why long shifts
  exist (rate pressure, site design, shift policy, incentives). It is **hypothesis from outside context, not derived
  from this data.**

## What I would do next

1. Log theme and segment rules in code so labels are fully reproducible.
2. Validate theme labels with a second coder and report agreement.
3. Replace the lexicon with a transformer sentiment model and compare.
4. Collect more videos and a larger review sample to test the platform difference properly.
5. Run the pilot and measure.

## Repository

```
src/analysis.py          reproduces all figures and tables
figures/                 charts (ngrams/ and hypothesis/ subfolders)
data/aggregated/         summary tables behind every chart
notebooks/original/      original Colab notebooks, archived (known issues listed inside)
```

Reproduce: `pip install -r requirements.txt` then `python src/analysis.py your_labelled_file.csv`.

---
**Author:** Sayed Ali Shahin
