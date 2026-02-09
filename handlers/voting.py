diff --git a/handlers/voting.py b/handlers/voting.py
index 2ccb17ad4e3481a33734bb6dfd13ea7c70db87bd..aeb2eb9cf3e43b324f9ef0754cf2a1a19921b2ba 100644
--- a/handlers/voting.py
+++ b/handlers/voting.py
@@ -1,23 +1,90 @@
+import asyncio
+import time
+
 from pyrogram import filters
+
 from core.state import game
 
-def start_voting(app):
+VOTE_TIME = 20
+
+
+async def start_voting(app):
+    game.phase = "voting"
     game.votes.clear()
-    app.send_message(
+    game.vote_deadline = time.time() + VOTE_TIME
+
+    await app.send_message(
         game.chat_id,
-        "🗳 Voting phase! Use `/vote @username`"
+        f"🗳 Voting phase started!\nUse `/vote @username` in next {VOTE_TIME} sec."
     )
 
+    asyncio.create_task(voting_timer(app))
+
+
+async def voting_timer(app):
+    await asyncio.sleep(VOTE_TIME)
+
+    if game.phase != "voting":
+        return
+
+    counts = {}
+    for target_id in game.votes.values():
+        counts[target_id] = counts.get(target_id, 0) + 1
+
+    if counts:
+        target_id = max(counts, key=counts.get)
+        game.influence[target_id] = max(0, game.influence.get(target_id, 100) - 20)
+        name = game.players.get(target_id, str(target_id))
+        await app.send_message(
+            game.chat_id,
+            f"⚖️ Vote result: {name} loses 20 influence. Remaining: {game.influence[target_id]}"
+        )
+
+        if game.influence[target_id] <= 0:
+            game.players.pop(target_id, None)
+            game.usernames.pop(target_id, None)
+            game.influence.pop(target_id, None)
+            await app.send_message(game.chat_id, f"💀 {name} has been eliminated.")
+    else:
+        await app.send_message(game.chat_id, "⚖️ No votes were cast this round.")
+
+    from handlers.endgame import check_end
+    from handlers.dm_round import start_round
+
+    if await check_end(app):
+        return
+
+    game.round += 1
+    await start_round(app)
+
+
 def register_voting(app):
 
     @app.on_message(filters.group & filters.command("vote"))
     async def vote(_, msg):
-        if not msg.entities or len(msg.entities) < 2:
-            return await msg.reply("Invalid vote.")
+        if game.phase != "voting":
+            return await msg.reply("Voting is not active right now.")
+
+        voter = msg.from_user
+        if not voter or voter.id not in game.players:
+            return await msg.reply("Only active players can vote.")
+
+        parts = (msg.text or "").split()
+        if len(parts) < 2 or not parts[1].startswith("@"):
+            return await msg.reply("Usage: /vote @username")
+
+        target_username = parts[1][1:].lower()
+        target_id = None
+        for uid, username in game.usernames.items():
+            if username and username.lower() == target_username:
+                target_id = uid
+                break
+
+        if not target_id or target_id not in game.players:
+            return await msg.reply("Invalid target username.")
 
-        target = msg.entities[1].user
-        if not target or target.id not in game.players:
-            return await msg.reply("Invalid target.")
+        if target_id == voter.id:
+            return await msg.reply("You cannot vote yourself.")
 
-        game.influence[target.id] -= 20
-        await msg.reply(f"🕯 Judgment cast on {target.first_name}")
+        game.votes[voter.id] = target_id
+        await msg.reply("✅ Vote recorded.")
