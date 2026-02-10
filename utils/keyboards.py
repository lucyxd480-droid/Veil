from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def join_kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🕯 Join Veil", callback_data="join")]])

def enter_kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🕯 Enter Veil (DM)", callback_data="enter")]])

def choice_kb():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🤍 Trust", callback_data="trust"),
        InlineKeyboardButton("🩸 Betray", callback_data="betray"),
        InlineKeyboardButton("🤫 Silent", callback_data="silent"),
    ]])

def vote_kb(players):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(name, callback_data=f"vote_{uid}")]
         for uid, name in players.items()]
    )
