import json
import os
from threading import Lock

PATH = "data/leaderboard.json"
_lock = Lock()

os.makedirs("data", exist_ok=True)


def _load():
    """Load leaderboard safely."""
    if not os.path.exists(PATH):
        return {}

    try:
        with open(PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save(data):
    """Save leaderboard safely."""
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_win(user_id):
    """Add a win to a user."""
    with _lock:
        data = _load()
        uid = str(user_id)
        data[uid] = data.get(uid, 0) + 1
        _save(data)


def get_leaderboard():
    """Return leaderboard sorted by wins."""
    data = _load()
    return sorted(data.items(), key=lambda x: x[1], reverse=True)
