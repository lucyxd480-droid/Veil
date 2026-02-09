diff --git a/handlers/join_timer.py b/handlers/join_timer.py
index 35da6731363666b3cb8558ae6daf66270f14dcd5..ff0ad3628eb51bb4cdbd4157223b811dedc2641c 100644
--- a/handlers/join_timer.py
+++ b/handlers/join_timer.py
@@ -1,33 +1,41 @@
-import asyncio, time
+import asyncio
+import time
+
 from core.state import game
+from utils.keyboards import join_keyboard
+
 
 async def join_timer(app):
+    me = await app.get_me()
+
     while game.join_open:
         remaining = int(game.join_end_time - time.time())
 
-        if remaining in (15, 10, 5):
+        if remaining == 15 and 15 not in game.join_reminders_sent:
+            game.join_reminders_sent.add(15)
             await app.send_message(
                 game.chat_id,
-                f"⏳ {remaining} seconds left to join!"
+                "⏳ **15 seconds left to join!**",
+                reply_markup=join_keyboard(me.username)
             )
 
         if remaining <= 0:
+            game.join_open = False
+
             if len(game.players) < 3:
-                game.join_open = False
-                game.phase = "idle"
                 await app.send_message(
                     game.chat_id,
-                    "🕯 Not enough players. Cancelling game..."
+                    "🕯 Not enough players, cancelling game!"
                 )
+                game.reset()
                 return
 
-            game.join_open = False
             game.phase = "ready"
             await app.send_message(
                 game.chat_id,
-                f"🔒 Joining closed! {len(game.players)} players joined.\n"
-                f"Admin can now begin the game with /begin"
+                f"🔒 Joining closed! Players joined: {len(game.players)}\n"
+                "Host can now start with /begin"
             )
             return
 
         await asyncio.sleep(1)
