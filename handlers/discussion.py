from pyrogram import filters
from core.state import games


def register_discussion(app):

    @app.on_message(filters.command("discuss") & filters.group)
    async def discuss(_, msg):
        chat = msg.chat.id
        game = games.get(chat)

        if not game:
            return

        game["phase"] = "discussion"

        await msg.reply(
            "🧠 Discuss.\nJudgment is coming.\nChoose wisely."
        )
