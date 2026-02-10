from pyrogram import filters
from core.state import games
from utils.keyboards import pick_kb


def register_pick(app):

    @app.on_message(filters.command("pick") & filters.group)
    async def pick(_, msg):
        chat = msg.chat.id
        game = games.get(chat)

        if not game:
            return

        if game.get("phase") != "discussion":
            return await msg.reply("❌ Not the right time.")

        players = [
            name for uid, name in game["players"].items()
            if uid in game["alive"]
        ]

        if not players:
            return await msg.reply("No players to pick.")

        await msg.reply(
            "Choose the condemned:",
            reply_markup=pick_kb(players)
        )
