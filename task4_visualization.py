"""
TrendPulse - Task 4: Visualisation
Loads the analysed CSV from Task 3 and produces 3 charts
plus a combined dashboard, all saved as PNG files.
"""

import pandas as pd
import matplotlib.pyplot as plt  # for creating charts
import os

# ── Setup ─────────────────────────────────────────────────────────────────────

df = pd.read_csv("data/trends_analysed.csv")

# Create the outputs/ folder to store chart images
os.makedirs("outputs", exist_ok=True)

# ── Chart 1: Top 10 Stories by Score (horizontal bar chart) ──────────────────

# Sort by score descending and take the top 10
top10 = df.nlargest(10, "score")

# Shorten titles longer than 50 characters so the chart stays readable
top10 = top10.copy()
top10["short_title"] = top10["title"].apply(
    lambda t: t[:50] + "…" if len(t) > 50 else t
)

fig1, ax1 = plt.subplots(figsize=(10, 6))

# barh = horizontal bar chart; invert y so highest score is at the top
ax1.barh(top10["short_title"], top10["score"], color="steelblue")
ax1.invert_yaxis()

ax1.set_title("Top 10 Stories by Score")
ax1.set_xlabel("Score (upvotes)")
ax1.set_ylabel("Story Title")

plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png", dpi=150)  # save BEFORE show
plt.show()
print("Saved outputs/chart1_top_stories.png")

# ── Chart 2: Stories per Category (vertical bar chart) ───────────────────────

category_counts = df["category"].value_counts()

# Use a different colour for each bar
colors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"]

fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.bar(category_counts.index, category_counts.values, color=colors)

ax2.set_title("Number of Stories per Category")
ax2.set_xlabel("Category")
ax2.set_ylabel("Number of Stories")

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png", dpi=150)
plt.show()
print("Saved outputs/chart2_categories.png")

# ── Chart 3: Score vs Comments (scatter plot) ─────────────────────────────────

# Separate popular and non-popular stories to colour them differently
popular     = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

fig3, ax3 = plt.subplots(figsize=(8, 6))

ax3.scatter(not_popular["score"], not_popular["num_comments"],
            color="gray",   alpha=0.6, label="Not Popular")
ax3.scatter(popular["score"],     popular["num_comments"],
            color="tomato", alpha=0.7, label="Popular")

ax3.set_title("Score vs Number of Comments")
ax3.set_xlabel("Score (upvotes)")
ax3.set_ylabel("Number of Comments")
ax3.legend()

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png", dpi=150)
plt.show()
print("Saved outputs/chart3_scatter.png")

# ── BONUS: Combined Dashboard ─────────────────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle("TrendPulse Dashboard", fontsize=16, fontweight="bold")

# --- Repeat Chart 1 on axes[0] ---
axes[0].barh(top10["short_title"], top10["score"], color="steelblue")
axes[0].invert_yaxis()
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")

# --- Repeat Chart 2 on axes[1] ---
axes[1].bar(category_counts.index, category_counts.values, color=colors)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Count")
axes[1].tick_params(axis="x", rotation=15)

# --- Repeat Chart 3 on axes[2] ---
axes[2].scatter(not_popular["score"], not_popular["num_comments"],
                color="gray",   alpha=0.6, label="Not Popular")
axes[2].scatter(popular["score"],     popular["num_comments"],
                color="tomato", alpha=0.7, label="Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend()

plt.tight_layout()
plt.savefig("outputs/dashboard.png", dpi=150)
plt.show()
print("Saved outputs/dashboard.png")