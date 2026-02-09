diff --git a/handlers/dm_join.py b/handlers/dm_join.py
index 994db74b6325eb16d86c0bc1d756c4d1f1022bdd..f41defb0679b5cdf5973bd10b2b412fc42120778 100644
--- a/handlers/dm_join.py
+++ b/handlers/dm_join.py
@@ -1,40 +1,71 @@
 from pyrogram import filters
+
 from core.state import game
 from utils.text import DM_JOIN_TEXT
 
+
+async def publish_players(app):
+    if not game.chat_id:
+        return
+
+    lines = []
+    for uid, name in game.players.items():
+        username = game.usernames.get(uid)
+        shown = f"@{username}" if username else f"({name})"
+        lines.append(f"• {shown}")
+
+    players_text = "\n".join(lines) if lines else "(none)"
+    await app.send_message(
+        game.chat_id,
+        f"#Players: {len(game.players)}\n{players_text}"
+    )
+
+
 def register_dm_join(app):
 
     @app.on_message(filters.private & filters.command("start"))
     async def dm_start(_, message):
-        if message.text != "/start join":
+        text = (message.text or "").strip()
+        if text not in {"/start join", "/start"}:
             return
 
         user = message.from_user
 
         if not game.join_open:
-            await message.reply("🕯 The Veil is closed.")
-            return
+            return await message.reply("🕯 No active join phase right now.")
 
         if user.id in game.players:
             return await message.reply("🕯 You are already inside.")
 
-        game.players[user.id] = user.first_name or f"({user.id})"
+        game.players[user.id] = user.first_name or str(user.id)
+        game.usernames[user.id] = user.username
         game.influence[user.id] = 100
 
         await message.reply(DM_JOIN_TEXT)
+        await publish_players(app)
 
-        players = "\n".join(f"• {n}" for n in game.players.values())
-        await app.send_message(
-            game.chat_id,
-            f"#Players: {len(game.players)}\n{players}"
-        )
-
-    @app.on_message(filters.private & filters.command("leavegame"))
+    @app.on_message(filters.private & filters.command(["leavegame", "flee"]))
     async def leave_dm(_, message):
         user = message.from_user
-        if user.id in game.players:
-            del game.players[user.id]
-            del game.influence[user.id]
-            await message.reply("🕯 You left the game.")
-        else:
-            await message.reply("🕯 You are not in the game.")
+        if user.id not in game.players:
+            return await message.reply("🕯 You are not in the game.")
+
+        del game.players[user.id]
+        game.influence.pop(user.id, None)
+        game.usernames.pop(user.id, None)
+
+        await message.reply("🏃 You fled from the game.")
+        await publish_players(app)
+
+    @app.on_message(filters.group & filters.command(["leavegame", "flee"]))
+    async def leave_group(_, message):
+        user = message.from_user
+        if not user or user.id not in game.players:
+            return await message.reply("🕯 You are not in the current game.")
+
+        del game.players[user.id]
+        game.influence.pop(user.id, None)
+        game.usernames.pop(user.id, None)
+
+        await message.reply("🏃 You left the game.")
+        await publish_players(app)
