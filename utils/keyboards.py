from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def join_kb():
return InlineKeyboardMarkup([
[InlineKeyboardButton("🩸 Join Game", callback_data="join")]
])


def pick_kb(players):
return InlineKeyboardMarkup([
[InlineKeyboardButton(p, callback_data=f"pick:{p}")]
for p in players
])
