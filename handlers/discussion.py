from pyrogram import filters
from core.flow import start_discussion
from core.state import games


def register_discussion(app):

    @app.on_message(filters.command("discuss") & filters.group)
    async def discuss(_, msg):
        chat = msg.chat.id
        game = games.get(chat)

        # Only allow if game exists and has started
        if not game or not game.get("started"):
            return

        # Trigger discussion phase
        await start_discussion(app, chat)
        await msg.reply("🧠 Discussion manually started.")
