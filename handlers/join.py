from pyrogram import filters
from pyrogram.types import CallbackQuery
from core.state import games


def register_join(app):

    @app.on_callback_query(filters.regex("^join$"))
    async def join(client, cb: CallbackQuery):
        chat_id = cb.message.chat.id
        user = cb.from_user
        game = games[chat_id]

        # Only allow joining during the join phase
        if game.get("phase") != "join":
            await cb.answer("Join phase is closed.", show_alert=True)
            return

        # Check if already joined
        if user.id in game["players"]:
            await cb.answer("You already joined.", show_alert=True)
            return

        # Add player
        game["players"][user.id] = {"name": user.first_name, "alive": True}
        game["alive"].add(user.id)

        await client.send_message(
            chat_id, f"🕯 {user.first_name} joined the game. ({len(game['players'])} players)"
        )
        await cb.answer("Joined!")
