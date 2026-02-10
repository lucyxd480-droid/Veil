from pyrogram import filters
from core.state import games


def register_join(app):
@app.on_callback_query(filters.regex("^join$"))
async def join(_, cb):
chat = cb.message.chat.id
user = cb.from_user
game = games[chat]


if user.id in game["players"]:
return await cb.answer("Already joined", show_alert=True)


game["players"][user.id] = user.first_name
await cb.answer("Joined")
