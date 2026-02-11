from pyrogram import filters

from core.flow import schedule_join_expiry, start_game
from core.state import games, new_game_state
from utils.keyboards import join_kb
from utils.auth import ensure_admin


def register_start(app):

    # ─────────────────────────────────────────────
    # Start Join Phase
    # ─────────────────────────────────────────────
    @app.on_message(filters.command("startgame") & filters.group)
    async def start(client, msg):

        if not await ensure_admin(client, msg):
            return

        chat_id = msg.chat.id
        existing = games.get(chat_id)

        # Prevent overwriting active game
        if existing and existing.get("started"):
            return await msg.reply("❌ A game is already running.")

        # Cancel old join task if exists
        if existing:
            join_task = existing.get("join_task")
            if join_task and not join_task.done():
                join_task.cancel()

        # Create fresh game state
        games[chat_id] = new_game_state()
        game = games[chat_id]
        game["phase"] = "join"

        seconds = game["join_seconds"]

        await msg.reply(
            f"🕯 THE VEIL OPENS...\nJoin within {seconds} seconds.",
            reply_markup=join_kb(),
        )

        await schedule_join_expiry(app, chat_id, seconds)

    # ─────────────────────────────────────────────
    # Force Start (Admin)
    # ─────────────────────────────────────────────
    @app.on_message(filters.command("forcestart") & filters.group)
    async def force_start(client, msg):

        if not await ensure_admin(client, msg):
            return

        chat_id = msg.chat.id
        game = games.get(chat_id)

        if not game or game.get("phase") != "join":
            return await msg.reply("❌ No active join phase.")

        # Cancel join timer before starting
        join_task = game.get("join_task")
        if join_task and not join_task.done():
            join_task.cancel()

        ok = await start_game(app, chat_id)

        if not ok:
            return await msg.reply(
                f"❌ Need at least {game.get('min_players', 3)} players."
            )

        await msg.reply("⚡ Force start successful.")
