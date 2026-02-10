leaderboard = {}

def add_win(uid):
    leaderboard[uid] = leaderboard.get(uid, 0) + 1

def top_players():
    return sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
