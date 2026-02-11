from collections import defaultdict


def new_game_state():
    return {
        "players": {},
        "roles": {},
        "alive": set(),
        "phase": "idle",
        "join_task": None,
        "phase_task": None,
        "picks": {},
        "night_actions": {},
        "role_sent": set(),
        "round": 0,
        "join_seconds": 60,
        "min_players": 3,
        "started": False,
    }


# All games stored here, auto-initialized with new_game_state
games = defaultdict(new_game_state)
