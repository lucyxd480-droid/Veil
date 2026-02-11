from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def join_kb():
    """Join button shown during join phase."""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Join Game", callback_data="join")]
        ]
    )


def pick_kb(alive_names):
    """Voting keyboard for alive players."""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(name, callback_data=f"pick:{name}")]
            for name in alive_names
        ]
    )
