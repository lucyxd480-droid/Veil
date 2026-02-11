from pyrogram import filters
from pyrogram.types import CallbackQuery

from core.flow import resolve_vote, start_vote
from core.state import games
from utils.keyboards import pick_kb
from utils.auth import ensure_admin


def register_pick(app):

    # ─────────────────────────────────────────────
    # Start Vote Phase (Manual Pick)
    # ─────────────────────────────────────────────
    @app.on_message(filters.command("pick") & filters.group)
    async def pick(client, msg):
        if not await ensure_admin(client, msg):
            return

        chat_id = msg.chat.id
        game = games.get(chat_id)

        if not game or not game.get("started"):
            return await msg.reply("❌ No active game.")

        if game.get("phase") not in {"discussion", "vote"}:
            return await msg.reply("❌ Not the right time.")

        if game.get("phase") == "vote":
            return await msg.reply("⚖️ Vote already in progress.")

        alive_players = {
            uid: data["name"]
            for uid, data in game["players"].items()
            if uid in game["alive"]
        }

        if not alive_players:
            return await msg.reply("❌ No alive players to vote.")

        game["phase"] = "vote"
        game["picks"] = {}

        await msg.reply(
            "⚖️ Choose the condemned:",
            reply_markup=pick_kb(list(alive_players.values()))
        )

    # ─────────────────────────────────────────────
    # Cast Vote
    # ─────────────────────────────────────────────
    @app.on_callback_query(filters.regex(r"^pick:.+"))
    async def cast_vote(_, cb: CallbackQuery):

        voted_name = cb.data.split(":", 1)[1]
        chat_id = cb.message.chat.id
        voter_id = cb.from_user.id

        game = games.get(chat_id)

        if not game or game.get("phase") != "vote":
            return await cb.answer("Voting is closed.", show_alert=True)

        if voter_id not in game["alive"]:
            return await cb.answer("Only alive players can vote.", show_alert=True)

        alive_names = {
            data["name"]
            for uid, data in game["players"].items()
            if uid in game["alive"]
        }

        if voted_name not in alive_names:
            return await cb.answer("Invalid vote target.", show_alert=True)

        # Prevent vote changing
        if voter_id in game["picks"]:
            return await cb.answer("Vote already locked.", show_alert=True)

        game["picks"][voter_id] = voted_name
        await cb.answer(f"⚖️ Vote locked: {voted_name}")

        # ─── Auto Resolve When All Alive Voted ───
        alive_voters = [uid for uid in game["alive"]]

        if all(uid in game["picks"] for uid in alive_voters):
            await resolve_vote(_, chat_id)

    # ─────────────────────────────────────────────
    # Manual Resolve Vote
    # ─────────────────────────────────────────────
    @app.on_message(filters.command("resolvevote") & filters.group)
    async def manual_resolve_vote(client, msg):
        if not await ensure_admin(client, msg):
            return

        chat_id = msg.chat.id
        game = games.get(chat_id)

        if not game or game.get("phase") != "vote":
            return await msg.reply("❌ Vote is not active.")

        await resolve_vote(app, chat_id)
        await msg.reply("✅ Vote resolved.")

    # ─────────────────────────────────────────────
    # Force Start Vote (Admin)
    # ─────────────────────────────────────────────
    @app.on_message(filters.command("autovote") & filters.group)
    async def trigger_vote(client, msg):
        if not await ensure_admin(client, msg):
            return

        chat_id = msg.chat.id
        game = games.get(chat_id)

        if not game or not game.get("started"):
            return await msg.reply("❌ No active game.")

        if game.get("phase") == "vote":
            return await msg.reply("⚖️ Vote already active.")

        await start_vote(app, chat_id)
        await msg.reply("⚖️ Vote phase started.")
