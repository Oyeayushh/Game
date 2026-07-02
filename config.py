"""
MadaraDefaultr Bot Configuration
Powered by Madara
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Telegram credentials ────────────────────────────────────────────────────
API_ID    = int(os.environ.get("API_ID", 0))
API_HASH  = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# ── Bot branding ────────────────────────────────────────────────────────────
BOT_NAME      = "sʜʀɪsᴛɪ ɢᴀᴍᴇ ᴘʟᴀʏᴇʀ"
BOT_USERNAME  = "@SHRISTI_GAME_PLAYER_bot"
POWERED_BY    = "⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴍᴀᴅᴀʀᴀ"
VERSION       = "v2.0"

# ── Database ────────────────────────────────────────────────────────────────
DATABASE_PATH = "madara.db"

# ── Assets ──────────────────────────────────────────────────────────────────
START_IMAGE = "assets/start.jpg"
PING_IMAGE  = "assets/ping.jpg"

# ── Game settings ───────────────────────────────────────────────────────────
CARD_TURN_TIMEOUT  = 60
BOMB_ROUND_TIMEOUT = 30
HACK_GUESS_TIMEOUT = 300

# ── Economy settings ────────────────────────────────────────────────────────
STARTING_COINS    = 5000
DAILY_BASE        = 500          # coins for day 1
CLAIM_AMOUNT      = 2000         # /claim group bonus
CLAIM_COOLDOWN    = 86400        # 24 h in seconds
DAILY_COOLDOWN    = 86400
DIVORCE_COST      = 2000
PROTECT_COST      = 1000         # per day
REVIVE_COST       = 500
TRANSFER_TAX      = 0.10         # 10 %
TRANSFER_TAX_MARRIED = 0.05      # 5 % if married

# ── RPG settings ────────────────────────────────────────────────────────────
KILL_COOLDOWN     = 3600         # 1 h between kills
KILL_SUCCESS_RATE = 0.50
KILL_LOOT_MIN     = 0.20
KILL_LOOT_MAX     = 0.40

# ── Shop items ──────────────────────────────────────────────────────────────
SHOP_ITEMS = {
    "knife":  {"name": "🔪 ᴋɴɪғᴇ",   "price": 1000,  "type": "weapon", "desc": "ᴇɴᴀʙʟᴇs /ʀᴏʙ ᴄᴏᴍᴍᴀɴᴅ"},
    "gun":    {"name": "🔫 ɢᴜɴ",     "price": 2500,  "type": "weapon", "desc": "+10% ʀᴏʙ sᴜᴄᴄᴇss"},
    "sword":  {"name": "⚔️ sᴡᴏʀᴅ",  "price": 5000,  "type": "weapon", "desc": "+20% ᴋɪʟʟ ʟᴏᴏᴛ"},
    "shield": {"name": "🛡️ sʜɪᴇʟᴅ", "price": 1500,  "type": "armor",  "desc": "-10% ᴅᴀᴍᴀɢᴇ ᴛᴀᴋᴇɴ"},
    "vest":   {"name": "🦺 ᴠᴇsᴛ",    "price": 3000,  "type": "armor",  "desc": "-20% ᴅᴀᴍᴀɢᴇ ᴛᴀᴋᴇɴ"},
}
