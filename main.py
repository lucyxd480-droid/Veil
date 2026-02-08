from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.admin import register_admin
from handlers.join import register_join
from handlers.callbacks import register_callbacks

app = Client("veil_bot", API_ID, API_HASH, bot_token=BOT_TOKEN)

register_admin(app)
register_join(app)
register_callbacks(app)

app.run()

