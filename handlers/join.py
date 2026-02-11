from pyrogram import filters
from pyrogram.types import CallbackQuery

from core.flow import start_game
from core.state import games


def register_join(app):
    @app.on_callback_query(filters.regex("^join$"))
    async def join(client, cb: CallbackQuery):
        chat_id = cb.message.chat.id
        user = cb.from_user

        game = games[chat_id]

        # Only allow joining during join phase
        if game.get("phase") != "join":
            return await cb.answer("Join phase is closed.", show_alert=True)

        # Prevent duplicate join
        if user.id in game["players"]:
            return await cb.answer("You already joined.", show_alert=True)

        # Add player
        game["players"][user.id] = {
            "name": user.first_name,
            "alive": True,
        }
        game["alive"].add(user.id)

        count = len(game["players"])

        await client.send_message(
            chat_id,
            f"🕯 {user.first_name} joined the game. ({count} players)",
        )

        await cb.answer("Joined!")

        # Auto-start once minimum players reached
        if (
            not game.get("started")
            and count >= game.get("min_players", 3)
        ):
            started = await start_game(app, chat_id)
            if started:
                await client.send_message(
                    chat_id,
                    "⚡ Minimum players reached. Auto-start triggered."
                )
