"""
MadaraDefaultr – Main Bot Entry Point
Powered by Madara

Usage:
    python main.py

Environment Variables Required:
    API_ID     – from https://my.telegram.org
    API_HASH   – from https://my.telegram.org
    BOT_TOKEN  – from @BotFather on Telegram
"""

import asyncio
import os
import importlib

from kurigram import Client as MadaraDefaultr
from kurigram import filters

from config import API_ID, API_HASH, BOT_TOKEN, BOT_NAME, POWERED_BY
from database import init_db

# ── Sanity check credentials ────────────────────────────────────────────────
if not API_ID or not API_HASH or not BOT_TOKEN:
    raise RuntimeError(
        "Missing credentials!\n"
        "Please set API_ID, API_HASH, and BOT_TOKEN as environment secrets.\n"
        "Get API_ID & API_HASH from https://my.telegram.org\n"
        "Get BOT_TOKEN from @BotFather on Telegram."
    )

# ── Create the bot client (exported as MadaraDefaultr) ──────────────────────
MadaraDefaultr = MadaraDefaultr(
    name="MadaraDefaultr",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "plugins"},
    sleep_threshold=60,
    workdir="./sessions",
)


async def main():
    print(f"🚀 Initialising database...")
    await init_db()
    print(f"✅ Database ready.")

    print(f"🤖 Starting {BOT_NAME}...")
    async with MadaraDefaultr:
        me = await MadaraDefaultr.get_me()
        print(
            f"\n{'='*50}\n"
            f"  {BOT_NAME} is ONLINE!\n"
            f"  Username : @{me.username}\n"
            f"  Bot ID   : {me.id}\n"
            f"  {POWERED_BY}\n"
            f"{'='*50}\n"
        )
        await MadaraDefaultr.idle()


if __name__ == "__main__":
    asyncio.run(main())
