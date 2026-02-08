from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Join Game", callback_data="join_game")]
    ])
