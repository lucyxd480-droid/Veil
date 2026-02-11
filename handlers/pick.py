from pyrogram import filters
from core.flow import resolve_vote, start_vote
from core.state import games
from utils.keyboards import pick_kb


def register_pick(app):

    @app.on_message(filters.command("pick") & filters.group)
    async def pick(_, msg):
        chat = msg.chat.id
        game = games.get(chat)

        if not game or not game.get("started"):
            return await msg.reply("❌ No active game.")
        if game.get("phase") not in {"discussion", "vote"}:
            return await msg.reply("❌ Not the right time.")

        alive_names = [
            data["name"] for uid, data in game["players"].items() if uid in game["alive"]
        ]
        if not alive_names:
            return await msg.reply("No players to pick.")

        game["phase"] = "vote"
        await msg.reply("Choose the condemned:", reply_markup=pick_kb(alive_names))

    @app.on_callback_query(filters.regex(r"^pick:.+"))
    async def cast_vote(_, cb):
        voted_name = cb.data.split(":", 1)[1]
        chat = cb.message.chat.id
        voter_id = cb.from_user.id

        game = games.get(chat)
        if not game or game.get("phase") != "vote":
            return await cb.answer("Voting is closed.", show_alert=True)

        if voter_id not in game["alive"]:
            return await cb.answer("Only alive players can vote.", show_alert=True)

        valid_names = {data["name"] for uid, data in game["players"].items() if uid in game["alive"]}
        if voted_name not in valid_names:
            return await cb.answer("Invalid vote target.", show_alert=True)

        game["picks"][voter_id] = voted_name
        await cb.answer(f"Vote locked: {voted_name}")

    @app.on_message(filters.command("resolvevote") & filters.group)
    async def manual_resolve_vote(_, msg):
        await resolve_vote(app, msg.chat.id)
        await msg.reply("✅ Vote resolved.")

    @app.on_message(filters.command("autovote") & filters.group)
    async def trigger_vote(_, msg):
        await start_vote(app, msg.chat.id)
        await msg.reply("⚖️ Auto vote phase started.")
