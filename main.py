from pyrogram import Client
from config import *

from handlers.start import register_start
from handlers.join import register_join
from handlers.extend import register_extend

# 🔥 Night system with buttons
from handlers.night_actions import register_night_actions

from handlers.discussion import register_discussion
from handlers.pick import register_pick
from handlers.end import register_end

# Plugins
from handlers.horror import register_horror
from handlers.false_end import register_false_end
from handlers.win import register_win


app = Client(
    "veil",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

register_start(app)
register_join(app)
register_extend(app)

register_night_actions(app)   # 🌑 NIGHT BUTTON SYSTEM

register_discussion(app)
register_pick(app)
register_end(app)

# Extra plugins
register_horror(app)
register_false_end(app)
register_win(app)

app.run()
