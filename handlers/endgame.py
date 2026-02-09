diff --git a/handlers/endgame.py b/handlers/endgame.py
index 7805f92034893de514b4dd9c1721174ac8f0441f..8ef142a6056f3d5726d9e02c6ec4357a2b017977 100644
--- a/handlers/endgame.py
+++ b/handlers/endgame.py
@@ -1,20 +1,33 @@
 from core.state import game
-from utils.text import END_TRUST, END_BETRAY, END_SILENT
+from utils.text import END_BETRAY, END_SILENT, END_TRUST
 
-def check_end(app):
-    if game.round > game.max_rounds or game.trust_collapse >= 2:
+
+async def check_end(app):
+    if len(game.players) < 3:
+        await app.send_message(game.chat_id, "🕯 Too few players left. Game ended.")
+        game.reset()
+        return True
+
+    if game.round >= game.max_rounds:
         winner = max(game.influence, key=game.influence.get, default=None)
-        end(app, winner)
+        await end(app, winner, reason="rounds")
+        return True
+
+    if game.trust_collapse >= 2:
+        await end(app, None, reason="collapse")
         return True
 
-    game.round += 1
     return False
 
-def end(app, winner):
-    if winner:
-        end_text = END_TRUST
+
+async def end(app, winner, reason: str):
+    if reason == "collapse":
+        end_text = END_BETRAY
+    elif winner:
+        win_name = game.players.get(winner, "Unknown")
+        end_text = f"{END_TRUST}\n\n🏆 Winner: {win_name}"
     else:
         end_text = END_SILENT
 
-    app.send_message(game.chat_id, end_text)
+    await app.send_message(game.chat_id, end_text)
     game.reset()
