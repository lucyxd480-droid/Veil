from pyrogram import Client
from config import *
from handlers.start import register_start
from handlers.join import register_join
from handlers.extend import register_extend
from handlers.night import register_night
from handlers.discussion import register_discussion
from handlers.pick import register_pick
from handlers.end import register_end


app = Client(
"veil",
api_id=API_ID,
api_hash=API_HASH,
bot_token=BOT_TOKEN
)


register_start(app)
register_join(app)
register_extend(app)
register_night(app)
register_discussion(app)
register_pick(app)
register_end(app)


app.run()
