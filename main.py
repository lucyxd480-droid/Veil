from pyrogram import Client
from config import BOT_TOKEN, API_ID, API_HASH

from handlers.join import register_join
from handlers.start import register_start
from handlers.admin import register_admin


app = Client(
    "veil",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

register_join(app)
register_start(app)
register_admin(app)

app.run()
