import time

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.chat_id = None
        self.host_id = None
        self.host_name = None

        self.players = {}          # user_id: display_name
        self.influence = {}        # user_id: points
        self.usernames = {}        # user_id: username or None

        self.join_open = False
        self.join_duration = 60
        self.join_end_time = None
        self.join_reminders_sent = set()

        self.phase = "idle"        # idle | join | ready | round | voting
        self.round = 0

        self.choices = {}          # user_id: trust|betray|silent
        self.choice_deadline = None

        self.votes = {}            # voter_id: target_id
        self.vote_deadline = None

        self.trust_collapse = 0
        self.max_rounds = 5

    def now(self):
        return time.time()


# single instance of game state
game = GameState()
