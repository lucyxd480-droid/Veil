import random

def apply_choice(player, choice):
    if choice == "trust":
        player.influence += random.randint(1, 3)
        player.silent_streak = 0

    elif choice == "betray":
        player.influence += random.randint(-6, 12)
        player.silent_streak = 0

    elif choice == "silent":
        player.silent_streak += 1
        if player.silent_streak > 1:
            player.influence -= 1

    player.influence = max(0, min(100, player.influence))
