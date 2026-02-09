# Veil Telegram Game Bot

A Telegram social-deduction style game bot built with **Pyrogram**.

## Current game flow (as implemented)

1. Group admin runs `/startgame`.
2. Bot opens a 60-second join phase and posts a join button.
3. Players DM the bot using `/start join` to enter.
4. When join closes with at least 3 players, admin runs `/begin`.
5. Each round, players receive DM options: **Trust**, **Betray**, **Remain Silent**.
6. After choices are collected/timed out, group sees a flavor result message.
7. Group voting can reduce a target player's influence.
8. Game ends by max rounds or trust collapse condition.

## Project structure

- `main.py`: bootstraps bot and registers handlers.
- `core/state.py`: in-memory `GameState` object.
- `handlers/`: command and game-phase logic.
- `utils/`: text blocks and inline keyboards.

## Notes about architecture

- State is currently **in-memory only** (single process, reset on restart).
- Most commands are designed for one active game instance at a time.
- Join and round flows are asynchronous and timer-based.

## Recommended roadmap

### MVP hardening (short term)

- Add admin permission checks for control commands.
- Validate vote eligibility (one vote per player per phase).
- Add explicit round resolution logic based on player choices.
- Add robust async handling (`await` for async send calls, task safety).
- Add logging and basic error reporting.

### Scale-up (mid term)

- Persist game and player data in PostgreSQL/SQLite.
- Support multiple concurrent group games (state keyed by `chat_id`).
- Add reconnect-safe timers/job queue.
- Add anti-spam/rate-limit safeguards.

### Product growth (long term)

- Player profiles, MMR/leaderboards, seasonal stats.
- New roles/events and configurable game modes.
- Economy: rewards, cosmetic unlocks, progression loops.
- Analytics dashboard for retention and balancing.

## Quick start

1. Create `.env` with:

```env
API_ID=...
API_HASH=...
BOT_TOKEN=...
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the bot:

```bash
python main.py
```

## Dependencies

See `requirements.txt`.
