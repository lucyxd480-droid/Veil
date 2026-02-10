from pyrogram import filters
from core.state import games
from core.engine import assign_roles

def register_join(app):
    @app.on_callback_query(filters.regex("^join$"))
    async def join(_, cb):
        chat = cb.message.chat.id
        user = cb.from_user
        game = games[chat]

        if user.id in game["players"]:
            return await cb.answer("Already joined")

        game["players"][user.id] = user.first_name
        game["alive"].add(user.id)

        await cb.answer("Joined")

        # AUTO ASSIGN when >= 4
        if len(game["players"]) >= 4:
            game["roles"] = assign_roles(game["players"])

            for uid, role in game["roles"].items():
                if uid not in game.get("role_sent", set()):
                    await cb.message.bot.send_message(
                        uid,
                        f"🩸 YOUR ROLE: {role.upper()}"
                    )
                    game.setdefault("role_sent", set()).add(uid)
