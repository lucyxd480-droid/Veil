diff --git a/utils/keyboards.py b/utils/keyboards.py
index d0ab6d2b5befe00cb8b82848c2fbe34704cf4003..6d7e9bf8cbdd04e650c95336daceca3a47513cc5 100644
--- a/utils/keyboards.py
+++ b/utils/keyboards.py
@@ -1,13 +1,15 @@
 from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
 
-def join_keyboard():
+
+def join_keyboard(bot_username: str):
     return InlineKeyboardMarkup([
-        [InlineKeyboardButton("Join Game", callback_data="join_game")]
+        [InlineKeyboardButton("Join The Veil", url=f"https://t.me/@Veiltestrobot?start=join")]
     ])
 
+
 def dm_options_keyboard():
     return InlineKeyboardMarkup([
         [InlineKeyboardButton("Trust", callback_data="c_trust")],
         [InlineKeyboardButton("Betray", callback_data="c_betray")],
         [InlineKeyboardButton("Remain Silent", callback_data="c_silent")]
     ])
