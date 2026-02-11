"""
Game state storage.
Each chat (group) gets its own independent game state.
"""

from collections import defaultdict


def new_game_state():
    """Create a fresh game state dictionary."""
    return {
        # Players
        "players": {},          # {user_id: {"name": str, "alive": bool}}
        "roles": {},            # {user_id: role_name}
        "alive": set(),         # {user_id}

        # Phase control
        "phase": "idle",        # idle | join | night | discussion | vote
        "started": False,
        "round": 0,

        # Timers / async tasks
        "join_task": None,
        "phase_task": None,

        # Voting & actions
        "picks": {},            # {voter_id: voted_name}
        "night_actions": {},    # {actor_id: (action, target_id)}

        # Utility
        "role_sent": set(),     # prevent double role DM
        "join_seconds": 60,
        "min_players": 3,
    }


# Auto-create state per chat_id
games = defaultdict(new_game_state)
