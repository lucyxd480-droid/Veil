from collections import defaultdict


games = defaultdict(lambda: {
"players": {},
"roles": {},
"alive": set(),
"phase": "idle",
"timer": None,
"picks": {},
"role_sent": set()
})
