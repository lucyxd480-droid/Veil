from pyrogram import filters
from core.state import game
from utils.text import DM_JOIN_TEXT

async def publish_players(app):
    if not game.chat_id:
        return

    lines = []
    for uid, name in game.players.items():
        username = game.usernames.get(uid)
        shown = f"@{username}" if username else f"({name})"
        lines.append(f"• {shown}")

    players_text = "\n".join(lines) if lines else "(none)"
    await app.send_message(
        game.chat_id,
        f"#Players: {len(game.players)}\n{players_text}"
    )

def register_dm_join(app):

    @app.on_message(filters.private & filters.command("start"))
    async def dm_start(_, message):
        text = (message.text or "").strip()
        if text not in {"/start join", "/start"}:
            return

        user = message.from_user

        if not game.join_open:
            return await message.reply("🕯 No active join phase right now.")

        if user.id in game.players:
            return await message.reply("🕯 You are already inside.")

        game.players[user.id] = user.first_name or str(user.id)
        game.usernames[user.id] = user.username
        game.influence[user.id] = 100

        await message.reply(DM_JOIN_TEXT)
        await publish_players(app)

    @app.on_message(filters.private & filters.command(["leavegame", "flee"]))
    async def leave_dm(_, message):
        user = message.from_user
        if user.id not in game.players:
            return await message.reply("🕯 You are not in the game.")

        del game.players[user.id]
        game.influence.pop(user.id, None)
        game.usernames.pop(user.id, None)

        await message.reply("🏃 You fled from the game.")
        await publish_players(app)

    @app.on_message(filters.group & filters.command(["leavegame", "flee"]))
    async def leave_group(_, message):
        user = message.from_user
        if not user or user.id not in game.players:
            return await message.reply("🕯 You are not in the current game.")

        del game.players[user.id]
        game.influence.pop(user.id, None)
        game.usernames.pop(user.id, None)

        await message.reply("🏃 You left the game.")
        await publish_players(app)
