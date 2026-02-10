import random
from core.roles import ROLES, EVIL


def assign_roles(players):
    roles = list(ROLES.keys())
    random.shuffle(roles)

    assigned = {}
    evil_count = max(1, len(players) // 4)

    for i, user_id in enumerate(players):
        if i < evil_count:
            assigned[user_id] = random.choice(list(EVIL))
        else:
            assigned[user_id] = "innocent"

    return assigned
