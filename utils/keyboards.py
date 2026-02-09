from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_USERNAME = "Veiltestrobot"  # your bot username

def join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "Join The Veil",
            url=f"https://t.me/{BOT_USERNAME}?start=join"
        )]
    ])


def dm_options_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Trust", callback_data="c_trust")],
        [InlineKeyboardButton("Betray", callback_data="c_betray")],
        [InlineKeyboardButton("Remain Silent", callback_data="c_silent")]
    ])
