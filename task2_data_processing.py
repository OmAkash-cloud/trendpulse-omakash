"""
TrendPulse - Task 2: Data Cleaning
Loads the raw JSON from Task 1, cleans it up using Pandas,
and saves a tidy CSV file for Task 3 to use.
"""

import pandas as pd  # for loading, cleaning, and saving tabular data
import glob          # for finding the JSON file without knowing the exact date
import os

# ── Step 1: Load the JSON file ────────────────────────────────────────────────

# glob finds files matching a pattern — we don't know the exact date in the name
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON file found in data/ — run Task 1 first.")
    exit()

# If multiple files exist, use the most recent one
json_file = sorted(json_files)[-1]

# pd.read_json loads the JSON array directly into a DataFrame (like a table)
df = pd.read_json(json_file)
print(f"Loaded {len(df)} stories from {json_file}")

# ── Step 2: Clean the data ────────────────────────────────────────────────────

# --- Remove duplicate stories (same post_id appearing more than once) ---
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# --- Drop rows where important fields are missing ---
# If a story has no ID, title, or score it's not useful
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# --- Fix data types ---
# score and num_comments should be whole numbers (integers), not floats
df["score"]        = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)
# fillna(0) first because num_comments can be missing (story with no comments)

# --- Remove low-quality stories ---
# Stories with fewer than 5 upvotes are likely irrelevant
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# --- Clean up whitespace in titles ---
# Strip leading/trailing spaces from every title
df["title"] = df["title"].str.strip()

# ── Step 3: Save as CSV ───────────────────────────────────────────────────────

output_path = "data/trends_clean.csv"

# index=False means don't write the row numbers (0, 1, 2...) as a column
df.to_csv(output_path, index=False)
print(f"\nSaved {len(df)} rows to {output_path}")

# --- Print how many stories came from each category ---
print("\nStories per category:")
category_counts = df["category"].value_counts()
for category, count in category_counts.items():
    print(f"  {category:<16} {count}")