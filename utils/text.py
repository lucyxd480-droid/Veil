diff --git a/utils/text.py b/utils/text.py
index 728666e8811fa1201100a28f3763d2ceace7fa34..f11889955c961cf9402cc20a274f6b649b872dce 100644
--- a/utils/text.py
+++ b/utils/text.py
@@ -1,49 +1,36 @@
 START_TEXT = (
-    "🕯 **The Veil has opened…**\n\n"
-    "Nothing here is forced.\n"
-    "Nothing here is revealed.\n\n"
-    "Click below if you dare to enter."
+    "🕯 **A new Veil game has been started by {host}!**\n\n"
+    "Shadows are gathering... enter if you dare.\n"
+    "Click **Join The Veil** below to jump into bot DM and join instantly."
 )
 
 DM_JOIN_TEXT = (
     "🕯 **You crossed the Veil.**\n\n"
     "Your name is now a shadow among others.\n"
-    "You will not be seen.\n"
-    "You will not be called.\n\n"
-    "_Wait. Observe. Decide._"
-)
-
-ROUND_DM_TEXT = (
-    "🔹 **A choice stands before you.**\n\n"
-    "🔹 Trust — believe someone else will too.\n"
-    "🔹 Betray — assume trust is a weakness.\n"
-    "🔹 Stay Silent — say nothing, risk nothing.\n\n"
-    "_You have 40 seconds._"
+    "Wait for round start in group..."
 )
 
 GROUP_ROUND_RESULT = [
-    "🕯 A silence lingered longer than expected…",
-    "🕯 Someone trusted. It mattered less than they hoped.",
-    "🕯 A betrayal passed unnoticed.",
-    "🕯 Doubt spread quietly through the group."
+    "🕯 Tension rises. No one is fully trusted.",
+    "🕯 Whispers spread. Someone moved in silence.",
+    "🕯 A risky trust changed the mood.",
+    "🕯 Betrayal leaves marks, even when unseen."
 ]
 
 END_TRUST = (
     "🕯 **The Veil Falls**\n\n"
-    "Trust endured longer than fear.\n"
-    "Not everyone lied.\n"
-    "That was enough."
+    "Trust survived the darkness.\n"
+    "A fragile peace wins tonight."
 )
 
 END_BETRAY = (
     "🕯 **The Veil Falls**\n\n"
-    "Betrayal shaped every step.\n"
-    "Truth never stood a chance."
+    "Betrayal consumed the circle.\n"
+    "Only suspicion remains."
 )
 
 END_SILENT = (
     "🕯 **The Veil Falls**\n\n"
-    "Silence consumed everything.\n"
-    "No truth survived.\n"
-    "No one won."
+    "Silence swallowed every voice.\n"
+    "No one truly wins."
 )
