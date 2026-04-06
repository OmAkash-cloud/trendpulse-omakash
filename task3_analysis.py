"""
TrendPulse - Task 3: Analysis with Pandas & NumPy
Loads the clean CSV from Task 2, computes statistics,
adds new columns, and saves an enriched CSV for Task 4.
"""

import pandas as pd
import numpy as np  # for numerical statistics (mean, median, std, etc.)

# ── Step 1: Load and explore ──────────────────────────────────────────────────

df = pd.read_csv("data/trends_clean.csv")

# shape gives us (number of rows, number of columns)
print(f"Loaded data: {df.shape}")

# Show the first 5 rows so we can sanity-check the data looks right
print("\nFirst 5 rows:")
print(df.head())

# Overall averages across all stories
avg_score    = df["score"].mean()
avg_comments = df["num_comments"].mean()
print(f"\nAverage score   : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")

# ── Step 2: NumPy statistics ──────────────────────────────────────────────────

scores = df["score"].to_numpy()  # convert column to a NumPy array

print("\n--- NumPy Stats ---")
print(f"Mean score   : {np.mean(scores):.2f}")
print(f"Median score : {np.median(scores):.2f}")
print(f"Std deviation: {np.std(scores):.2f}")
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# Which category appears most often?
top_category = df["category"].value_counts().idxmax()
top_count    = df["category"].value_counts().max()
print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Which story has the highest comment count?
most_commented = df.loc[df["num_comments"].idxmax()]
print(f"\nMost commented story: \"{most_commented['title']}\" — {most_commented['num_comments']} comments")

# ── Step 3: Add new columns ───────────────────────────────────────────────────

# engagement = how much discussion a story gets relative to its upvotes
# Adding 1 to score prevents division-by-zero
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = True if this story's score is above the average score
df["is_popular"] = df["score"] > avg_score

# ── Step 4: Save the enriched DataFrame ──────────────────────────────────────

output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)
print(f"\nSaved to {output_path}")