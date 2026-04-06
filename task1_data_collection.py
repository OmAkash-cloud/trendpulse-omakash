"""
TrendPulse - Task 1: Data Collection
Fetches trending stories from the HackerNews API and categorises them
by scanning titles for keywords, then saves results as a JSON file.
"""

import requests   # for making HTTP calls to the API
import json       # for saving data as a JSON file
import os         # for creating folders
import time       # for sleep between categories
from datetime import datetime  # for recording when we collected each story

# ── Category keyword map ──────────────────────────────────────────────────────
# Each key is a category name. Each value is a list of words to look for
# in story titles (checked case-insensitively).
CATEGORIES = {
    "technology":    ["AI", "software", "tech", "code", "computer",
                      "data", "cloud", "API", "GPU", "LLM"],
    "worldnews":     ["war", "government", "country", "president",
                      "election", "climate", "attack", "global"],
    "sports":        ["NFL", "NBA", "FIFA", "sport", "game", "team",
                      "player", "league", "championship"],
    "science":       ["research", "study", "space", "physics", "biology",
                      "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game",
                      "book", "show", "award", "streaming"],
}

MAX_PER_CATEGORY = 25   # stop collecting a category once we hit 25 stories
TOP_STORY_LIMIT  = 500  # only look at the first 500 trending IDs

# This header tells HackerNews who is making the request
HEADERS = {"User-Agent": "TrendPulse/1.0"}


def assign_category(title: str):
    """
    Checks the title against every category's keyword list.
    Returns the first matching category name, or None if no match.
    """
    title_lower = title.lower()  # lowercase once so comparisons are easier
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category  # first match wins
    return None  # no category matched


def fetch_top_story_ids():
    """
    Calls HackerNews for the list of top story IDs.
    Returns the first 500 as a list of integers.
    """
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    print("Fetching top story IDs from HackerNews …")

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # crash if status code is 4xx/5xx
        all_ids = response.json()    # parse JSON → Python list
        print(f"  → Got {len(all_ids)} IDs total; using first {TOP_STORY_LIMIT}.")
        return all_ids[:TOP_STORY_LIMIT]
    except requests.RequestException as e:
        print(f"  ✗ Failed to fetch story IDs: {e}")
        return []  # return empty list so the rest of the script handles it


def fetch_story(story_id: int):
    """
    Fetches the details of a single story by its ID.
    Returns a dict, or None if the request fails.
    """
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"  ✗ Could not fetch story {story_id}: {e}")
        return None  # skip this story, don't crash


def collect_stories(story_ids: list):
    """
    Loops through story IDs, fetches each one, assigns a category,
    and builds a list of story records (dicts with 7 fields each).
    Sleeps 2 seconds each time a category reaches its 25-story quota.
    """
    counts    = {cat: 0 for cat in CATEGORIES}  # track count per category
    collected = []

    # Record the time once — all stories in this run share the same timestamp
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\nFetching individual stories …")

    for story_id in story_ids:
        # If every category is full, no need to keep looping
        if all(counts[cat] >= MAX_PER_CATEGORY for cat in CATEGORIES):
            print("  All categories full — stopping early.")
            break

        story = fetch_story(story_id)

        # Skip if the API call failed or if the story has no title
        if not story or "title" not in story:
            continue

        title    = story.get("title", "")
        category = assign_category(title)

        # Skip stories that don't match any category keyword
        if category is None:
            continue

        # Skip if we already have 25 stories for this category
        if counts[category] >= MAX_PER_CATEGORY:
            continue

        # Build the record with exactly the 7 required fields
        record = {
            "post_id":      story.get("id"),
            "title":        title,
            "category":     category,
            "score":        story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author":       story.get("by", "unknown"),
            "collected_at": run_time,
        }

        collected.append(record)
        counts[category] += 1

        print(f"  [{category:<14}] ({counts[category]:>2}/{MAX_PER_CATEGORY}) → {title[:70]}")

        # Sleep 2 seconds once per category, right when quota is reached
        if counts[category] == MAX_PER_CATEGORY:
            print(f"  ✓ '{category}' quota reached — sleeping 2 s …")
            time.sleep(2)

    return collected


def save_to_json(stories: list):
    """
    Creates the data/ folder and writes all stories to a dated JSON file.
    Returns the file path used.
    """
    os.makedirs("data", exist_ok=True)  # create folder if missing
    date_str  = datetime.now().strftime("%Y%m%d")
    file_path = f"data/trends_{date_str}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)

    return file_path


def main():
    story_ids = fetch_top_story_ids()
    if not story_ids:
        print("No story IDs retrieved — exiting.")
        return

    stories   = collect_stories(story_ids)
    file_path = save_to_json(stories)

    # Required output line
    print(f"\nCollected {len(stories)} stories. Saved to {file_path}")


if __name__ == "__main__":
    main()