import random
from core.roles import ROLES


def assign_roles(players):
    """
    Assign balanced roles based on lobby size.
    Ensures:
    - ~25% evil players (minimum 1)
    - At least one Guardian and one Watcher when possible
    - All assigned roles exist in ROLES
    """

    player_ids = list(players)
    random.shuffle(player_ids)

    total = len(player_ids)
    if total == 0:
        return {}

    evil_count = max(1, total // 4)

    # Role pools
    evil_pool = ["traitor", "assassin", "cultist", "mindbreaker", "zealot"]
    good_pool = ["guardian", "watcher", "innocent"]

    assigned = {}

    # --- Assign Evil Roles ---
    for uid in player_ids[:evil_count]:
        assigned[uid] = random.choice(evil_pool)

    # --- Assign Good Roles ---
    good_ids = player_ids[evil_count:]

    for uid in good_ids:
        assigned[uid] = random.choice(good_pool)

    # --- Guarantee key roles if enough players ---
    if total >= 5 and len(good_ids) >= 2:
        assigned[good_ids[0]] = "guardian"
        assigned[good_ids[1]] = "watcher"

    # --- Safety Check: fallback to innocent ---
    for uid, role in assigned.items():
        if role not in ROLES:
            assigned[uid] = "innocent"

    return assigned
