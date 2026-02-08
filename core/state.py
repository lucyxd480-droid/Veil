diff --git a/core/state.py b/core/state.py
index 00c903b8d72ec16a3a6fee3bec1e5b206d9cfc6f..5c362f32f2e9147677bb478c8daf6af579dac4f4 100644
--- a/core/state.py
+++ b/core/state.py
@@ -1,22 +1,38 @@
 import time
 
+
 class GameState:
     def __init__(self):
         self.reset()
 
     def reset(self):
         self.chat_id = None
-        self.players = {}        # user_id: name
-        self.influence = {}      # user_id: points
+        self.host_id = None
+        self.host_name = None
+
+        self.players = {}          # user_id: display_name
+        self.influence = {}        # user_id: points
+        self.usernames = {}        # user_id: username or None
+
         self.join_open = False
         self.join_duration = 60
         self.join_end_time = None
-        self.join_extended = 0
-        self.phase = "idle"
+        self.join_reminders_sent = set()
+
+        self.phase = "idle"       # idle | join | ready | round | voting
         self.round = 0
-        self.choices = {}        
-        self.votes = {}          
-        self.trust_collapse = 0
         self.max_rounds = 5
 
+        self.choices = {}          # user_id: trust|betray|silent
+        self.choice_deadline = None
+
+        self.votes = {}            # voter_id: target_id
+        self.vote_deadline = None
+
+        self.trust_collapse = 0
+
+    def now(self):
+        return time.time()
+
+
 game = GameState()
