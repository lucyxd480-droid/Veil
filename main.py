from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.begin import register_begin
from handlers.join import register_join
from handlers.veil import register_veil
from handlers.leaderboard import register_leaderboard

app = Client(
    "veil_v45",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

register_begin(app)
register_join(app)
register_veil(app)
register_leaderboard(app)

app.run()
