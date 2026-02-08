from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

from handlers.start import register_start
from handlers.dm_join import register_dm_join
from handlers.admin import register_admin
from handlers.begin import register_begin
from handlers.dm_round import register_dm_round
from handlers.voting import register_voting

app = Client(
    "veil",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

register_start(app)
register_dm_join(app)
register_admin(app)
register_begin(app)
register_dm_round(app)
register_voting(app)

app.run()
