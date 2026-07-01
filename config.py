"""
MadaraDefaultr Bot Configuration
Powered by Madara
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Telegram credentials ────────────────────────────────────────────────────
API_ID   = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# ── Bot branding ────────────────────────────────────────────────────────────
BOT_NAME      = "SHRISTI GAME PLAYER"
BOT_USERNAME  = "@SHRISTI_GAME_PLAYER_bot"
POWERED_BY    = "⚡ Powered by Madara"
VERSION       = "v1.0"

# ── Database ────────────────────────────────────────────────────────────────
DATABASE_PATH = "madara.db"

# ── Game settings ───────────────────────────────────────────────────────────
CARD_TURN_TIMEOUT  = 60   # seconds per turn
BOMB_ROUND_TIMEOUT = 30   # seconds to pass bomb
HACK_GUESS_TIMEOUT = 300  # 5 min to guess password

# ── Starting coins for new users ────────────────────────────────────────────
STARTING_COINS = 5000
