from pyrogram import filters
from core.false_end import false_end


def register_false_end(app):

    @app.on_message(filters.command("checkend") & filters.group)
    async def check(_, msg):
        if false_end():
            await msg.reply("🕯 GAME OVER... or is it?")
        else:
            await msg.reply("🕯 The game continues.")
