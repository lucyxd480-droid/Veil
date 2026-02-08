from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def join_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🕯 Enter The Veil",
                    url="https://t.me/Veiltestrobot?start=join"
                )
            ]
        ]
    )


def dm_options_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🕊 Trust", callback_data="choice_trust"),
                InlineKeyboardButton("🗡 Betray", callback_data="choice_betray")
            ],
            [
                InlineKeyboardButton("🌑 Stay Silent", callback_data="choice_silent")
            ]
        ]
    )


def vote_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👍 Yes", callback_data="vote_yes"),
                InlineKeyboardButton("👎 No", callback_data="vote_no")
            ]
        ]
    )
