from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.state import game

def register_start(app):

    @app.on_message(filters.command("start") & filters.group)
    async def group_start(_, msg):
        game.chat_id = msg.chat.id

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🕯 Click to Join The Veil",
                    url="https://t.me/Veiltestrobot?start=veil_join"
                )
            ]
        ])

        await msg.reply(
            "🕯 **The Veil is forming…**\n\n"
            "Tap below to step inside.\n"
            "_Your choice will remain unseen._",
            reply_markup=keyboard
        )
