import json
import os

PATH = "data/leaderboard.json"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Initialize leaderboard file if it doesn't exist
if not os.path.exists(PATH):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump({}, f)


def add_win(user_id):
    # Load current leaderboard
    with open(PATH, encoding="utf-8") as f:
        data = json.load(f)

    # Increment wins for the user
    data[str(user_id)] = data.get(str(user_id), 0) + 1

    # Save back to file
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
