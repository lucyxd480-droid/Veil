from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# ─────────────────────────────
# Core Game Handlers
# ─────────────────────────────
from handlers.start import register_start
from handlers.join import register_join
from handlers.extend import register_extend
from handlers.night_actions import register_night_actions
from handlers.discussion import register_discussion
from handlers.pick import register_pick
from handlers.end import register_end
from handlers.status import register_status

# ─────────────────────────────
# Extra Plugins
# ─────────────────────────────
from handlers.horror import register_horror
from handlers.false_end import register_false_end
from handlers.win import register_win


# ─────────────────────────────
# App Initialization
# ─────────────────────────────
app = Client(
    "veil",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)


def register_all_handlers(application: Client):
    # Core
    register_start(application)
    register_join(application)
    register_extend(application)
    register_night_actions(application)
    register_discussion(application)
    register_pick(application)
    register_end(application)
    register_status(application)

    # Plugins
    register_horror(application)
    register_false_end(application)
    register_win(application)


if __name__ == "__main__":
    print("🕯 Veil Bot starting...")
    register_all_handlers(app)
    print("✅ Handlers registered.")
    app.run()
