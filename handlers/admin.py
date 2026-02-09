diff --git a/handlers/admin.py b/handlers/admin.py
index 9d46a90d234cb1539310f303329ecef13521c5a8..2f3941f1495287bda2e2f91a5118d971fc43ca41 100644
--- a/handlers/admin.py
+++ b/handlers/admin.py
@@ -1,21 +1,30 @@
+import time
+
 from pyrogram import filters
+
 from core.state import game
-import time
+
 
 def register_admin(app):
 
     @app.on_message(filters.group & filters.command("extend"))
     async def extend(_, msg):
         if not game.join_open:
             return await msg.reply("🕯 No active join phase to extend.")
 
-        parts = msg.text.split()
-        extra = int(parts[1]) if len(parts) > 1 else 15
+        parts = (msg.text or "").split()
+        if len(parts) < 2 or not parts[1].isdigit():
+            return await msg.reply("Usage: /extend <seconds>")
+
+        extra = int(parts[1])
+        if extra <= 0:
+            return await msg.reply("Seconds must be greater than 0.")
 
         game.join_end_time += extra
-        await msg.reply(f"Joining time extended by {extra} sec! Total left: {int(game.join_end_time - time.time())} sec")
+        left = max(0, int(game.join_end_time - time.time()))
+        await msg.reply(f"⏳ Join time extended by {extra} sec! {left} sec left to join.")
 
     @app.on_message(filters.group & filters.command("cancel"))
     async def cancel(_, msg):
         game.reset()
-        await msg.reply("🕯 The Veil has been cancelled.")
+        await msg.reply("🕯 The Veil game has been cancelled.")
