"""
Project: Zombie Waves AI Strategy Codex
Source: r/ZombieWaves
Objective: Extract game-mechanic synergies for non-commercial AI fine-tuning.
Compliance: Adheres to Reddit Responsible Builder Policy (60 RPM Limit) & Privacy Standards.
"""

import praw
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# 1. LOAD CONFIGURATION
# We use .env to keep secrets like Client ID and Passwords off GitHub.
load_dotenv()

# --- COMPLIANCE & PATH CONSTANTS ---
# We use a 2-second sleep (30 RPM) to stay 50% below the 60 RPM limit.
REQUEST_DELAY = 2  
# Update this path to your external SSD drive letter
SSD_PATH = os.getenv("SSD_DATA_PATH", "E:/ZombieWavesProject/data/raw_reddit_data.jsonl")

def get_reddit_instance():
    """
    Initializes the PRAW Reddit instance using secure environment variables.
    The User-Agent is unique and descriptive to comply with Reddit's API rules.
    """
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=f"windows:ProjectCodex:v1.0 (by u/{os.getenv('REDDIT_USERNAME')})",
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD")
    )

def anonymize_data(submission, comments):
    """
    COMPLIANCE BLOCK: PRIVACY & USER DELETION
    Strips PII (Personally Identifiable Information).
    The 'source_id' is retained specifically for Deletion-Compliance:
    If a user deletes their post on Reddit, we can use this ID to find
    and purge it from our local SSD in the future.
    """
    return {
        "source_id": submission.id,
        "title": submission.title,
        "context": submission.selftext,
        "top_advice": comments,
        "author": "REDACTED_FOR_PRIVACY",
        "ingested_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "is_public_content": True
    }

def sync_deletion_compliance(existing_ids):
    """
    COMPLIANCE BLOCK: DATA HYGIENE
    Placeholder for the weekly sync script. This function will eventually
    re-check the status of IDs and remove any that return a 404 or [deleted].
    """
    print("Running compliance check for deleted content...")
    # Future logic: reddit.info(fullnames=existing_ids)
    pass

def scrape_subreddit_synergies(subreddit_name, query_list, limit=10):
    """
    Core engine to search r/ZombieWaves for meta-strategies and synergies.
    Includes rate-limiting and anonymization for policy compliance.
    """
    reddit = get_reddit_instance()
    subreddit = reddit.subreddit(subreddit_name)
    
    # Ensure the directory on the SSD exists
    os.makedirs(os.path.dirname(SSD_PATH), exist_ok=True)
    
    print(f"Starting compliant scrape for r/{subreddit_name}...")

    with open(SSD_PATH, "a", encoding="utf-8") as f:
        for query in query_list:
            print(f"Searching for: '{query}'")
            # Using .search() allows us to target specific 'exploit' or 'synergy' discussions
            for submission in subreddit.search(query, limit=limit):
                
                # Expand 'MoreComments' objects to get deeper thread advice
                # Limit=0 means we only get the most relevant top-level comments
                submission.comments.replace_more(limit=0)
                all_comments = [c.body for c in submission.comments.list()[:5]]

                # COMPLIANCE: Anonymize data before it is written to the SSD
                clean_data = anonymize_data(submission, all_comments)
                
                # Save each entry as a JSON line (JSONL format)
                f.write(json.dumps(clean_data) + "\n")
                
                # COMPLIANCE: Hard-coded rate-limiting sleep
                print(f"  > Ingested Post ID: {submission.id}. Compliance pause...")
                time.sleep(REQUEST_DELAY)

if __name__ == "__main__":
    # Core strategy keywords based on our game research
    zombie_waves_queries = [
        "MX Hero build synergies",
        "Mini-clip weapon reload exploit",
        "Virtual Battleground 2026 meta strategies",
        "Best S-tier robot combinations for survival"
    ]
    
    try:
        scrape_subreddit_synergies("ZombieWaves", zombie_waves_queries)
        print(f"\nSuccess! Data lake updated at: {SSD_PATH}")
    except Exception as e:
        print(f"\nError during execution: {e}")
        print("Tip: Check your .env credentials and internet connection.")