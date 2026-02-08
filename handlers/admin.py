from pyrogram import filters
from core.state import game
import time

def register_admin(app):

    @app.on_message(filters.group & filters.command("extend"))
    async def extend(_, msg):
        if not game.join_open:
            return await msg.reply("🕯 No active join phase to extend.")

        parts = msg.text.split()
        extra = int(parts[1]) if len(parts) > 1 else 15

        game.join_end_time += extra
        await msg.reply(f"Joining time extended by {extra} sec! Total left: {int(game.join_end_time - time.time())} sec")

    @app.on_message(filters.group & filters.command("cancel"))
    async def cancel(_, msg):
        game.reset()
        await msg.reply("🕯 The Veil has been cancelled.")
