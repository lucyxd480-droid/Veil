"""
Role definitions for The Veil.
Keep this file purely declarative (no logic here).
"""

# ===============================
# ROLE DESCRIPTIONS
# ===============================

ROLES = {
    # --- Evil Roles ---
    "traitor": "🩸 Night kill. You are the hidden blade of the dark.",
    "assassin": "🗡 Night kill. Precision hunter who strikes without mercy.",
    "cultist": "🕷 Evil-aligned deceiver. Survive and control the night.",
    "zealot": "🕯 Fanatic evil role feeding on confusion.",
    "mindbreaker": "🧠 Evil role that twists trust and fear.",
    "puppeteer": "🕸 Chaos role (reserved for future events).",

    # --- Neutral / Special (future) ---
    "doppelganger": "🪞 Chaos role (reserved for future events).",

    # --- Good Roles ---
    "guardian": "🛡 Protect one player at night from kill.",
    "watcher": "👁 Watch one player at night and see their aura (role).",
    "innocent": "🤍 No active power. Use discussion and voting wisely.",
}


# ===============================
# ALIGNMENTS
# ===============================

EVIL = {
    "traitor",
    "assassin",
    "cultist",
    "puppeteer",
    "mindbreaker",
    "zealot",
}

GOOD = set(ROLES.keys()) - EVIL
