from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def decision_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Trust", callback_data="d_trust"),
            InlineKeyboardButton("Betray", callback_data="d_betray"),
            InlineKeyboardButton("Silent", callback_data="d_silent")
        ]
    ])

def vote_kb(players):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(p.name, callback_data=f"v_{p.user_id}")]
        for p in players.values()
    ])

def join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎃 Join Game", callback_data="join_game")]
    ])
