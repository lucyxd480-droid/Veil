from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from core.flow import resolve_night
from core.state import games
from utils.auth import ensure_admin


ACTIONS = {
    "traitor": "kill",
    "assassin": "kill",
    "guardian": "protect",
    "watcher": "watch",
}


# ─────────────────────────────────────────────
# Send night buttons in DM
# ─────────────────────────────────────────────
async def send_night_action_buttons(app, chat_id: int):
    game = games.get(chat_id)
    if not game:
        return

    alive_ids = list(game.get("alive", []))

    for actor_id, role in game.get("roles", {}).items():
        action = ACTIONS.get(role)

        # Skip if role has no action or player dead
        if not action or actor_id not in alive_ids:
            continue

        rows = []
        for target_id in alive_ids:
            if target_id == actor_id:
                continue

            target_name = game["players"][target_id]["name"]

            rows.append([
                InlineKeyboardButton(
                    f"{action.title()}: {target_name}",
                    callback_data=f"act:{chat_id}:{action}:{target_id}",
                )
            ])

        if not rows:
            continue

        try:
            await app.send_message(
                actor_id,
                f"🌑 Your night ability: {action}\nChoose one target.",
                reply_markup=InlineKeyboardMarkup(rows),
            )
        except Exception:
            # User has not started bot in DM
            pass


# ─────────────────────────────────────────────
# Register Handlers
# ─────────────────────────────────────────────
def register_night_actions(app):

    # ─── Start Night Phase ───
    @app.on_message(filters.command("night") & filters.group)
    async def night(client, msg):
        if not await ensure_admin(client, msg):
            return

        chat_id = msg.chat.id
        game = games.get(chat_id)

        if not game or not game.get("started"):
            return await msg.reply("❌ No active game.")

        if game.get("phase") == "night":
            return await msg.reply("🌑 Night is already active.")

        game["phase"] = "night"
        game.setdefault("night_actions", {})

        await send_night_action_buttons(app, chat_id)
        await msg.reply("🌑 Night falls. Actions sent in DM.")

    # ─── Night Action Pick ───
    @app.on_callback_query(filters.regex(r"^act:\-?\d+:[a-z]+:\d+$"))
    async def action_pick(_, cb: CallbackQuery):

        _, chat_s, action, target_s = cb.data.split(":")
        chat_id = int(chat_s)
        target_id = int(target_s)
        actor_id = cb.from_user.id

        game = games.get(chat_id)

        if not game or game.get("phase") != "night":
            return await cb.answer("Night phase is not active.", show_alert=True)

        role = game.get("roles", {}).get(actor_id)
        expected_action = ACTIONS.get(role)

        if action != expected_action:
            return await cb.answer("You cannot perform this action.", show_alert=True)

        if actor_id not in game["alive"] or target_id not in game["alive"]:
            return await cb.answer("Invalid target.", show_alert=True)

        # Prevent changing action multiple times
        if actor_id in game["night_actions"]:
            return await cb.answer("Action already locked.", show_alert=True)

        game["night_actions"][actor_id] = (action, target_id)

        await cb.answer("🌑 Night action locked.")

        # Optional auto-resolve when all required actions submitted
        required = [
            uid for uid, role in game.get("roles", {}).items()
            if ACTIONS.get(role) and uid in game["alive"]
        ]

        if all(uid in game["night_actions"] for uid in required):
            await resolve_night(_, chat_id)

    # ─── Manual Resolve ───
    @app.on_message(filters.command("resolvenight") & filters.group)
    async def manual_resolve(client, msg):
        if not await ensure_admin(client, msg):
            return

        chat_id = msg.chat.id
        game = games.get(chat_id)

        if not game or game.get("phase") != "night":
            return await msg.reply("❌ Night is not active.")

        await resolve_night(app, chat_id)
        await msg.reply("✅ Night resolved.")
