"""
Reproduces every number and chart in the README from the labelled review file.

Usage:
    python src/analysis.py path/to/Employee_Segment_P5_combined_with_themes.csv

The raw review data is NOT included in this repository (see data/README.md).
Outputs: figures/*.png and data/aggregated/*.csv
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from textblob import TextBlob

ROOT = Path(__file__).resolve().parents[1]
FIG, AGG = ROOT / "figures", ROOT / "data" / "aggregated"
FIG.mkdir(exist_ok=True); AGG.mkdir(parents=True, exist_ok=True)

BLUE, LIGHT, GREY = "#2f6f9f", "#9cc0d8", "#8a8f98"
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})

THEMES = {
    "Competitive Payment & Benefits": "Pay & benefits",
    "Intense Physical Demands & Shift Scheduling": "Physical demands & shifts",
    "Management Favoritism and HR poor support": "Management & HR support",
}
SUBRATINGS = {
    "rating_compensation_benefits": "Compensation & benefits",
    "rating_diversity_inclusion": "Diversity & inclusion",
    "rating_career_opportunities": "Career opportunities",
    "rating_culture_values": "Culture & values",
    "rating_senior_leadership": "Senior leadership",
    "rating_work_life": "Work-life balance",
}


def label(score, t=0.1):
    return "positive" if score > t else "negative" if score < -t else "neutral"


def main(path):
    df = pd.read_csv(path)
    gd = df[df.platform == "Glassdoor"].copy()
    yt = df[df.platform == "YouTube"].copy()
    order = ["positive", "neutral", "negative"]

    # 1. Sentiment by platform -------------------------------------------------
    rows = []
    for name, d in [("Glassdoor", gd), ("YouTube", yt)]:
        vc = d.sentiment_label.value_counts()
        for s in order:
            rows.append({"platform": name, "sentiment": s, "count": int(vc.get(s, 0)),
                         "share_pct": round(100 * vc.get(s, 0) / len(d), 1), "n": len(d)})
    sp = pd.DataFrame(rows); sp.to_csv(AGG / "sentiment_by_platform.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 4))
    w = 0.38
    for i, (name, c) in enumerate([("Glassdoor", BLUE), ("YouTube", LIGHT)]):
        sub = sp[sp.platform == name].set_index("sentiment").loc[order]
        b = ax.bar([x + (i - .5) * w for x in range(3)], sub.share_pct, w,
                   label=f"{name} (n={sub.n.iloc[0]})", color=c)
        ax.bar_label(b, fmt="%.0f%%", padding=2, fontsize=9)
    ax.set_xticks(range(3)); ax.set_xticklabels(order); ax.set_ylabel("% of items")
    ax.set_title("Sentiment by platform (TextBlob, ±0.1 threshold)"); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(FIG / "01_sentiment_by_platform.png", dpi=160); plt.close(fig)

    # 2. Glassdoor sub-ratings (0 = "not rated" in the source, excluded) -------
    rows = []
    for col, nice in SUBRATINGS.items():
        s = gd[col][gd[col] > 0]
        rows.append({"dimension": nice, "n_rated": len(s), "mean": round(s.mean(), 2),
                     "pct_low_1_2": round(100 * (s <= 2).mean()), "pct_high_4_5": round(100 * (s >= 4).mean())})
    sr = pd.DataFrame(rows).sort_values("mean"); sr.to_csv(AGG / "glassdoor_subratings.csv", index=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    cols = [BLUE if m == sr["mean"].max() else LIGHT for m in sr["mean"]]
    b = ax.barh(sr.dimension, sr["mean"], color=cols)
    ax.bar_label(b, fmt="%.2f", padding=3, fontsize=9); ax.set_xlim(0, 5)
    ax.axvline(gd.rating_overall.mean(), ls="--", color=GREY, lw=1)
    ax.text(gd.rating_overall.mean() + .05, -0.65, f"overall {gd.rating_overall.mean():.2f}", color=GREY, fontsize=9)
    ax.set_title("Glassdoor star ratings by dimension\n(1–5 scale, unrated excluded)", loc="left")
    fig.tight_layout(); fig.savefig(FIG / "02_glassdoor_subratings.png", dpi=160); plt.close(fig)

    # 3. Theme counts (multi-label) and sentiment within theme -----------------
    themed = df[df.Theme.notna()]
    rows = []
    for full, short in THEMES.items():
        m = df.Theme.fillna("").str.contains(full, regex=False)
        vc = df[m].sentiment_label.value_counts()
        rows.append({"theme": short, "reviews": int(m.sum()),
                     "pct_of_all_150": round(100 * m.sum() / len(df), 1),
                     "pct_of_themed_89": round(100 * m.sum() / len(themed), 1),
                     **{f"n_{s}": int(vc.get(s, 0)) for s in order}})
    rows.append({"theme": "(no theme assigned)", "reviews": int(df.Theme.isna().sum()),
                 "pct_of_all_150": round(100 * df.Theme.isna().mean(), 1)})
    th = pd.DataFrame(rows); th.to_csv(AGG / "theme_counts.csv", index=False)
    t3 = th.iloc[:3].sort_values("reviews")
    fig, ax = plt.subplots(figsize=(7, 3.4))
    b = ax.barh(t3.theme, t3.reviews, color=BLUE); ax.bar_label(b, padding=3)
    ax.set_title(f"Reviews mentioning each theme (of {len(df)}; a review can have 2 themes)")
    fig.tight_layout(); fig.savefig(FIG / "03_theme_counts.png", dpi=160); plt.close(fig)

    # 4. Segments (Glassdoor only: YouTube has no role information) ------------
    seg = gd.Segment.value_counts().rename_axis("segment").reset_index(name="reviews")
    seg["pct_of_glassdoor"] = (100 * seg.reviews / len(gd)).round(1)
    seg.to_csv(AGG / "segment_counts_glassdoor.csv", index=False)
    s = seg.sort_values("reviews")
    fig, ax = plt.subplots(figsize=(7, 4))
    b = ax.barh(s.segment, s.reviews, color=[BLUE if x == "Regular Associates" else LIGHT for x in s.segment])
    ax.bar_label(b, padding=3); ax.set_title(f"Glassdoor reviews by worker segment (n={len(gd)})")
    fig.tight_layout(); fig.savefig(FIG / "04_segments.png", dpi=160); plt.close(fig)

    # 5. Sensitivity: does removing stopwords (incl. 'not', 'no') change sentiment?
    raw = gd[["summary", "review_pros", "review_cons", "advice_to_management"]].fillna("").astype(str).agg(" ".join, axis=1)
    gd["raw_label"] = raw.apply(lambda x: label(TextBlob(x).sentiment.polarity))
    cmp = pd.DataFrame({"cleaned_text (original)": gd.sentiment_label.value_counts(normalize=True) * 100,
                        "raw_text (negations kept)": gd.raw_label.value_counts(normalize=True) * 100}).loc[order].round(1)
    cmp.to_csv(AGG / "sentiment_sensitivity_glassdoor.csv")
    agree = (gd.sentiment_label == gd.raw_label).mean()
    ax = cmp.plot(kind="bar", figsize=(7, 4), color=[LIGHT, BLUE], rot=0)
    ax.set_ylabel("% of Glassdoor reviews"); ax.legend(frameon=False)
    ax.set_title(f"Sentiment is robust to preprocessing ({agree:.0%} of labels unchanged)")
    ax.figure.tight_layout(); ax.figure.savefig(FIG / "05_sentiment_sensitivity.png", dpi=160); plt.close(ax.figure)

    print(sp.to_string(index=False)); print(sr.to_string(index=False)); print(th.to_string(index=False))
    print(seg.to_string(index=False)); print(cmp); print(f"label agreement cleaned vs raw: {agree:.3f}")


if __name__ == "__main__":
    main(sys.argv[1])
