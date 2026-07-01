# MadaraDefaultr – Telegram Game Bot

**Bot username:** @SHRISTI_GAME_PLAYER_bot  
**Powered by Madara**

## Stack
- Python 3.11
- [Kurigram](https://github.com/KurigramBot/Kurigram) – Pyrogram fork with coloured buttons & premium emoji support
- aiosqlite – async SQLite database
- python-dotenv – environment variable loading

## Project Structure

```
main.py            – Bot entry point (client named MadaraDefaultr)
config.py          – Configuration & branding constants
database.py        – SQLite schema + helpers
plugins/
  start.py         – /start, /help, /balance, /wallet, /top + nav callbacks
  card_game.py     – 🃏 Card Flip Game (/card, /bet, /flip)
  bomb_game.py     – 💣 Bomb Game (/bomb, /join, /pass, /rank, /leaders, /bombcancel)
  hack_game.py     – 🔐 Password Hacking Game (/hack, /register, /guess, /end)
utils/
  buttons.py       – Kurigram coloured buttons (primary/success/danger) + premium emoji helpers
```

## Required Secrets
Set these in Replit Secrets (not in code):

| Secret      | Where to get it                         |
|-------------|------------------------------------------|
| `BOT_TOKEN` | @BotFather on Telegram                  |
| `API_ID`    | https://my.telegram.org → App           |
| `API_HASH`  | https://my.telegram.org → App           |

## How to Run
The workflow `Run Bot` executes `python main.py`.

## Games

### 🃏 Card Game
- `/card` – Start game (in group)
- `/bet <amount>` – Join game
- `/flip a/b/c/d` – Play your card this round
- 4 rounds, 4 hidden cards per player, same sum for all — strategy wins!

### 💣 Bomb Game
- `/bomb <amount>` – Start game with entry fee
- `/join <amount>` – Join before game starts
- `/pass` – Pass the bomb
- `/rank` – Check rank
- `/leaders` – Leaderboard
- `/bombcancel` – Admin cancel + refund

### 🔐 Hack Game (Password Hacking)
- `/hack <reward> <digits 3-6>` – Host starts game
- `/register <amount> coins` – Join the game
- `/guess <number>` – Make a guess (HACKS = right pos, GLITCHES = wrong pos)
- `/end` – Host ends game

### 💰 General
- `/balance` or `/wallet` – Check coins
- `/top` – Global leaderboard

## User Preferences
- Import name: `MadaraDefaultr` (used as bot client variable)
- Branding: "Powered by Madara" on all messages
- Bot: @SHRISTI_GAME_PLAYER_bot
- Premium emojis enabled (bot has Telegram Premium)
- Kurigram coloured buttons: primary (blue), success (green), danger (red)
