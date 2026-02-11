from pyrogram import filters

from core.state import games


def register_status(app):
    @app.on_message(filters.command("gamestatus") & filters.group)
    async def status(_, msg):
        game = games.get(msg.chat.id)
        if not game:
            return await msg.reply("ℹ️ No game state found for this chat.")

        players = len(game.get("players", {}))
        alive = len(game.get("alive", []))
        phase = game.get("phase", "idle")
        round_no = game.get("round", 0)
        started = "yes" if game.get("started") else "no"

        await msg.reply(
            "📊 Veil Status\n"
            f"Phase: {phase}\n"
            f"Started: {started}\n"
            f"Round: {round_no}\n"
            f"Players: {players}\n"
            f"Alive: {alive}"
        )
