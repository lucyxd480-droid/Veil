diff --git a/handlers/start.py b/handlers/start.py
index 3c8e00131f1fa9791d9c452b08bb2c48b31d9045..5f994d2c47e1d1a13e5c418e0d126df46c81c102 100644
--- a/handlers/start.py
+++ b/handlers/start.py
@@ -1,27 +1,34 @@
+import asyncio
+import time
+
 from pyrogram import filters
+
 from core.state import game
+from handlers.join_timer import join_timer
 from utils.keyboards import join_keyboard
 from utils.text import START_TEXT
-from handlers.join_timer import join_timer
-import asyncio, time
+
 
 def register_start(app):
 
     @app.on_message(filters.group & filters.command("startgame"))
     async def start_game(_, msg):
-        if game.join_open:
-            return await msg.reply("🕯 A game is already forming!")
+        if game.join_open or game.phase in {"ready", "round", "voting"}:
+            return await msg.reply("🕯 A game is already active in this group.")
 
         game.reset()
         game.join_open = True
         game.chat_id = msg.chat.id
+        game.host_id = msg.from_user.id if msg.from_user else None
+        game.host_name = msg.from_user.first_name if msg.from_user else "Unknown"
         game.phase = "join"
         game.join_duration = 60
         game.join_end_time = time.time() + game.join_duration
 
+        me = await app.get_me()
         await msg.reply(
-            START_TEXT,
-            reply_markup=join_keyboard()
+            START_TEXT.format(host=game.host_name),
+            reply_markup=join_keyboard(me.username)
         )
 
         asyncio.create_task(join_timer(app))
