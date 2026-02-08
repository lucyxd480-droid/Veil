from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Join Game", callback_data="join_game")]
    ])

def dm_options_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💗 Trust", callback_data="c_trust")],
        [InlineKeyboardButton("💔 Betray", callback_data="c_betray")],
        [InlineKeyboardButton("🖤 Remain Silent", callback_data="c_silent")]
    ])
