from pyrogram import filters
from core.state import game

MIN_PLAYERS = 6


def register_start(app):

    @app.on_message(filters.command("start"))
    async def start_handler(client, message):

        if game.active:
            await message.reply("🎮 Game already started.")
            return

        if game.join_open:
            await message.reply("⏳ Joining is still open.")
            return

        if len(game.players) < MIN_PLAYERS:
            await message.reply(
                f"❌ Not enough players ({len(game.players)}/{MIN_PLAYERS})"
            )
            return

        game.start_game()

        await message.reply(
            "🐺 **The game has begun!**\n"
            f"👥 Players: {len(game.players)}\n"
            f"🔁 Round: {game.round}"
        )
