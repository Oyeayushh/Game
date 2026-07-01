"""
MadaraDefaultr – Entry Point
Powered by Madara

Run:  python3 main.py

Required secrets: BOT_TOKEN, API_ID, API_HASH
"""

import asyncio
import os
from dotenv import load_dotenv

# ── Load .env FIRST so local/VPS runs work the same as Replit secrets ───────
load_dotenv()

# ── Credential check ────────────────────────────────────────────────────────
_required = ["BOT_TOKEN", "API_ID", "API_HASH"]
_missing = [k for k in _required if not os.environ.get(k)]
if _missing:
    raise RuntimeError(
        f"Missing environment secrets: {', '.join(_missing)}\n"
        "Set them in Replit Secrets or a .env file.\n"
        "  BOT_TOKEN → @BotFather on Telegram\n"
        "  API_ID    → https://my.telegram.org\n"
        "  API_HASH  → https://my.telegram.org"
    )

from pyrogram import Client, idle
from database import init_db
from config import API_ID, API_HASH, BOT_TOKEN, BOT_NAME, POWERED_BY


async def main():
    # ── Database ─────────────────────────────────────────────────────────────
    print("🗄  Initialising database…")
    await init_db()
    print("✅ Database ready.")

    # ── Create the Pyrogram/Kurigram client INSIDE the event loop ────────────
    client = Client(
        name="MadaraDefaultr",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        sleep_threshold=60,
        workdir="./sessions",
    )

    # ── Inject into proxy module BEFORE importing plugins ────────────────────
    import MadaraDefaultr as _proxy
    _proxy._client = client

    # ── Load all plugin handlers ──────────────────────────────────────────────
    print("📦 Loading plugins…")
    import plugins.start       # noqa: F401
    import plugins.card_game   # noqa: F401
    import plugins.bomb_game   # noqa: F401
    import plugins.hack_game   # noqa: F401
    print("✅ Plugins loaded.")

    # ── Start the bot ─────────────────────────────────────────────────────────
    print(f"🤖 Connecting {BOT_NAME}…")
    os.makedirs("sessions", exist_ok=True)
    async with client:
        me = await client.get_me()
        print(
            f"\n{'='*52}\n"
            f"  {BOT_NAME} is ONLINE!\n"
            f"  Username : @{me.username}\n"
            f"  Bot ID   : {me.id}\n"
            f"  {POWERED_BY}\n"
            f"{'='*52}\n"
        )
        await idle()


if __name__ == "__main__":
    asyncio.run(main())
