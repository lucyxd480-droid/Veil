from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def join_keyboard(bot_username: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "Join The Veil",
                url=f"https://t.me/{bot_username}?start=join"
            )
        ]
    ])


def dm_options_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Trust", callback_data="c_trust")],
        [InlineKeyboardButton("Betray", callback_data="c_betray")],
        [InlineKeyboardButton("Remain Silent", callback_data="c_silent")]
    ])


def enter_veil_keyboard(label: str = "Enter Veil"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(label, callback_data="enter_veil")]
    ])
