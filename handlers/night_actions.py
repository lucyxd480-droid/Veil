from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from core.flow import resolve_night
from core.state import games

ACTIONS = {
    "traitor": "kill",
    "guardian": "protect",
    "watcher": "watch",
}


async def send_night_action_buttons(app, chat_id: int):
    game = games.get(chat_id)
    if not game:
        return

    alive_ids = [uid for uid in game["alive"] if uid in game["players"]]

    for actor_id, role in game.get("roles", {}).items():
        action = ACTIONS.get(role)
        if not action or actor_id not in game["alive"]:
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

        await app.send_message(
            actor_id,
            f"🌑 Your night ability: {action}. Choose one target.",
            reply_markup=InlineKeyboardMarkup(rows),
        )


def register_night_actions(app):

    @app.on_message(filters.command("night") & filters.group)
    async def night(_, msg):
        chat = msg.chat.id
        game = games.get(chat)
        if not game or not game.get("started"):
            return await msg.reply("❌ No active game.")

        game["phase"] = "night"
        await send_night_action_buttons(app, chat)
        await msg.reply("🌑 Night falls. Actions sent in DM.")

    @app.on_callback_query(filters.regex(r"^act:\-?\d+:[a-z]+:\d+$"))
    async def action_pick(_, cb):
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
            return await cb.answer("You cannot do this action.", show_alert=True)

        if actor_id not in game["alive"] or target_id not in game["alive"]:
            return await cb.answer("Invalid target.", show_alert=True)

        game["night_actions"][actor_id] = (action, target_id)
        await cb.answer("Night action locked.")

    @app.on_message(filters.command("resolvenight") & filters.group)
    async def manual_resolve(_, msg):
        await resolve_night(app, msg.chat.id)
        await msg.reply("✅ Night resolved.")
