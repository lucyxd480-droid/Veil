import json
import os


PATH = "data/leaderboard.json"


if not os.path.exists(PATH):
with open(PATH, "w") as f:
json.dump({}, f)




def add_win(user_id):
with open(PATH) as f:
data = json.load(f)
data[str(user_id)] = data.get(str(user_id), 0) + 1
with open(PATH, "w") as f:
json.dump(data, f, indent=2)
