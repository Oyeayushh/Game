<br clear="both">

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=32&duration=3000&pause=1000&color=FF6B6B&center=true&vCenter=true&width=600&lines=🎮+SHRISTI+GAME+PLAYER;⚡+Powered+by+Madara;The+Ultimate+Telegram+Game+Bot" alt="Typing SVG" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Kurigram](https://img.shields.io/badge/Kurigram-2.2.23-0088CC?style=for-the-badge&logo=telegram&logoColor=white)](https://kurigram.icu)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-🟢%20Online-brightgreen?style=for-the-badge)](https://t.me/SHRISTI_GAME_PLAYER_bot)
[![Telegram](https://img.shields.io/badge/Bot-@SHRISTI__GAME__PLAYER__bot-26A5E4?style=for-the-badge&logo=telegram)](https://t.me/SHRISTI_GAME_PLAYER_bot)

<br/>

> **The most feature-rich Telegram gaming bot — built with Kurigram, premium emoji buttons, and ⚡ Powered by Madara**

<br/>

[**Play Now →**](https://t.me/SHRISTI_GAME_PLAYER_bot) · [**Add to Group →**](https://t.me/SHRISTI_GAME_PLAYER_bot?startgroup=true) · [**Support**](#)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎮 Games
- 🃏 **Card Flip Game** — 4 cards, 4 rounds, equal sum fairness
- 💣 **Bomb Game** — pass the bomb, last alive wins
- 🔐 **Password Hacking** — HACKS & GLITCHES feedback system
- ⏱️ **60-second turn timers** with auto-play
- 🤖 **Smart auto-cancel** & admin refund controls

</td>
<td width="50%">

### 💰 Economy
- 🪙 **Coin system** — win coins across all games
- 🏆 **Global leaderboard** — compete with everyone
- 📊 **Per-game stats** — track your wins & losses
- 💎 **Premium emojis** on every button
- 🔵🟢🔴 **Coloured buttons** (primary / success / danger)

</td>
</tr>
</table>

---

## 🎮 Game Guides

<details>
<summary><b>🃏 Card Flip Game</b></summary>

Each player gets **4 hidden cards** labelled A, B, C, D.

| Rule | Detail |
|------|--------|
| **Sum fairness** | All players' cards sum to the same total |
| **Each round** | Pick one card to flip — highest value wins the round |
| **Rounds** | 4 rounds total, highest total score wins the pot 🏆 |
| **Timer** | 60 seconds per turn — auto-play activates if you miss |
| **Tie** | Random winner selected |

**Commands:**
```
/card              → Start a new game (host)
/bet <amount>      → Join the waiting game
/flip a/b/c/d      → Play your card this round
```

</details>

<details>
<summary><b>💣 Bomb Game</b></summary>

Pay the entry fee, get secretly assigned the bomb, and pass it before it blows!

| Rule | Detail |
|------|--------|
| **Entry** | All players pay the same entry fee |
| **Bomb** | Randomly assigned at start — only the holder knows |
| **Explosion** | Random chance each round — higher chance if you don't pass |
| **Winner** | Last player alive takes the pot 💰 |
| **Admin** | `/bombcancel` cancels the game and refunds all entry fees |

**Commands:**
```
/bomb <amount>     → Start game with entry fee
/join <amount>     → Join before game starts
/pass              → Pass the bomb to a random player
/rank              → Check your or a friend's rank
/leaders           → Bomb game leaderboard
/bombcancel        → (Admin) Cancel & refund
```

</details>

<details>
<summary><b>🔐 Password Hacking Mini-Game</b></summary>

Baka has a **secret 3-6 digit password**. Crack it using HACKS and GLITCHES!

| Feedback | Meaning |
|----------|---------|
| 🟢 **HACKS** | Correct digit in the correct position |
| 🟡 **GLITCHES** | Correct digit in the wrong position |
| ❌ **No match** | Digit not in the password at all |

**Example:**
```
Password:  1 2 3 4 5
Your guess: 1 2 4 3 9
Result: HACKS: 2  GLITCHES: 2
```

**Commands:**
```
/hack <reward> <digits 3-6>    → Host starts a hack game
/register <amount> coins       → Join and pay entry fee
/guess <number>                → Make your guess
/end                           → (Host only) End the game
```

</details>

---

## 🤖 All Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot / welcome message |
| `/help` | All commands guide |
| `/balance` | Check your coin balance |
| `/wallet` | Full wallet + stats |
| `/top` | Global leaderboard |
| `/card` | Start a Card Flip game |
| `/bet <amount>` | Join a card game |
| `/flip a/b/c/d` | Flip a card this round |
| `/bomb <amount>` | Start a Bomb game |
| `/join <amount>` | Join a bomb game |
| `/pass` | Pass the bomb |
| `/rank` | Check rank |
| `/leaders` | Bomb leaderboard |
| `/bombcancel` | Admin: cancel bomb game |
| `/hack <amount> <digits>` | Host a Hack game |
| `/register <amount> coins` | Join a hack game |
| `/guess <number>` | Guess the password |
| `/end` | Host: end the hack game |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.11 |
| **Framework** | [Kurigram](https://kurigram.icu) (Pyrogram fork) |
| **Database** | SQLite via `aiosqlite` |
| **Buttons** | `ButtonStyle.PRIMARY` / `SUCCESS` / `DANGER` |
| **Emojis** | Telegram Premium Custom Emoji |
| **Branding** | ⚡ Powered by Madara |

---

## 🚀 Self-Hosting

### Prerequisites
- Python 3.11+
- Telegram API credentials from [my.telegram.org](https://my.telegram.org)
- A bot token from [@BotFather](https://t.me/BotFather)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/ragini19854-prog/new_madara_music
cd new_madara_music

# 2. Install dependencies
pip install kurigram aiosqlite python-dotenv tgcrypto

# 3. Set environment variables
export API_ID=your_api_id
export API_HASH=your_api_hash
export BOT_TOKEN=your_bot_token

# 4. Run the bot
python3 main.py
```

### Environment Variables

| Variable | Where to get |
|----------|-------------|
| `BOT_TOKEN` | [@BotFather](https://t.me/BotFather) → `/newbot` |
| `API_ID` | [my.telegram.org](https://my.telegram.org) → API development tools |
| `API_HASH` | Same page as API_ID |

---

## 📁 Project Structure

```
MadaraDefaultr/
├── main.py              # Entry point — starts the bot
├── MadaraDefaultr.py    # Client proxy module (import as app)
├── config.py            # Bot config & branding constants
├── database.py          # SQLite schema + async helpers
├── plugins/
│   ├── start.py         # /start, /help, /wallet, /top
│   ├── card_game.py     # 🃏 Card Flip Game
│   ├── bomb_game.py     # 💣 Bomb Passing Game
│   └── hack_game.py     # 🔐 Password Hacking Game
└── utils/
    └── buttons.py       # Premium emoji + coloured button factories
```

---

## 🎨 Premium Button Styles

This bot uses **Kurigram's exclusive coloured buttons**:

| Style | Colour | Usage |
|-------|--------|-------|
| `ButtonStyle.PRIMARY` | 🔵 Blue | Main actions (join, play, add to group) |
| `ButtonStyle.SUCCESS` | 🟢 Green | Positive actions (wallet, help, register) |
| `ButtonStyle.DANGER` | 🔴 Red | Destructive / bold actions (bomb, cancel) |

All buttons support **`icon_custom_emoji_id`** for premium animated emoji icons.

---

<div align="center">

## ⚡ Powered by Madara

Made with ❤️ by **Madara**

[![Telegram](https://img.shields.io/badge/Bot-@SHRISTI__GAME__PLAYER__bot-26A5E4?style=for-the-badge&logo=telegram)](https://t.me/SHRISTI_GAME_PLAYER_bot)

*"The best Telegram gaming bot — built to win."*

</div>
