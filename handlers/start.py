from pyrogram import filters
from core.flow import schedule_join_expiry, start_game
from core.state import games, new_game_state
from utils.keyboards import join_kb


def register_start(app):

    @app.on_message(filters.command("startgame") & filters.group)
    async def start(_, msg):
        chat = msg.chat.id
        games[chat] = new_game_state()
        game = games[chat]
        game["phase"] = "join"

        await msg.reply(
            "🕯 THE VEIL OPENS...\nJoin within 60 seconds.",
            reply_markup=join_kb(),
        )
        await schedule_join_expiry(app, chat, game["join_seconds"])

    @app.on_message(filters.command("forcestart") & filters.group)
    async def force_start(_, msg):
        chat = msg.chat.id
        game = games.get(chat)
        if not game or game.get("phase") != "join":
            return await msg.reply("❌ No join phase is active.")

        ok = await start_game(app, chat)
        if not ok:
            return await msg.reply("❌ Need at least 3 players to force start.")

        await msg.reply("⚡ Force start enabled.")
