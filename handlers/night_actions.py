from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.state import games


ACTIONS = {
    "traitor": "kill",
    "guardian": "protect",
    "watcher": "watch"
}


def register_night_actions(app):

    @app.on_message(filters.command("night") & filters.group)
    async def night(_, msg):
        chat = msg.chat.id
        game = games.get(chat)

        if not game:
            return

        game["phase"] = "night"

        for uid, role in game.get("roles", {}).items():
            if role in ACTIONS:
                await app.send_message(
                    uid,
                    f"🌑 Night Action: {ACTIONS[role]}",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Choose target",
                                    callback_data=f"act:{chat}"
                                )
                            ]
                        ]
                    )
                )

        await msg.reply("🌑 Night falls. Actions sent in DM.")
