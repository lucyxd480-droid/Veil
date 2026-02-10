from pyrogram import filters
from pyrogram.types import CallbackQuery
from core.state import games


def register_join(app):

    @app.on_callback_query(filters.regex("^join$"))
    async def join(client, cb: CallbackQuery):
        chat_id = cb.message.chat.id
        user = cb.from_user

        game = games.setdefault(chat_id, {
            "players": [],
            "alive": [],
            "roles": {}
        })

        if user.id in game["players"]:
            await cb.answer("You already joined.", show_alert=True)
            return

        game["players"].append(user.id)
        game["alive"].append(user.id)

        await client.send_message(
            chat_id,
            f"🕯 {user.first_name} joined the game."
        )

        await cb.answer()
