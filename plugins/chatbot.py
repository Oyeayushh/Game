"""
MadaraDefaultr – AI Chatbot Plugin (100% MongoDB based)
Powered by Madara

Drop this single file into plugins/ and add `import plugins.chatbot` in main.py.
Everything (on/off state, sticker pool, chat history) lives in MongoDB — no
sqlite, no config.py edits needed.

.env needed:
    MONGO_URI=your_mongodb_connection_string      (required)
    GROQ_API_KEY=your_groq_key                    (optional, else canned replies)
    GROQ_MODEL=llama-3.3-70b-versatile            (optional)

Commands:
    /chatbot on|off|status   -> group admins only (anyone in DM)
    /resetstickers           -> clears this chat's learned sticker pool
"""

import os
import random
import time

import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient

import MadaraDefaultr as app
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from config import POWERED_BY, BOT_NAME, BOT_USERNAME

# ─── Mongo setup ────────────────────────────────────────────────────────────

MONGO_URI    = os.environ.get("MONGO_URI", "mongodb+srv://saranjaat9694:saranjaat435@cluster0.ofptc9e.mongodb.net/?appName=Cluster0")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL   = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"

_mongo    = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=8000) if MONGO_URI else None
_db       = _mongo["madara_chatbot"] if _mongo else None
_settings = _db["chatbot_settings"] if _db else None   # {chat_id, enabled}
_stickers = _db["chatbot_stickers"] if _db else None   # {chat_id, file_id}
_history  = _db["chatbot_history"] if _db else None    # {chat_id, turns:[...]}

STICKER_POOL_CAP = 100
HISTORY_LIMIT    = 8


async def _startup_ping():
    if _mongo is None:
        print("[chatbot] MONGO_URI not set — chatbot will stay disabled.")
        return
    try:
        await _mongo.admin.command("ping")
        print("[chatbot] MongoDB connected OK — /chatbot on|off is ready.")
    except Exception as e:
        print(f"[chatbot] MongoDB connection FAILED: {e}")


try:
    import asyncio
    asyncio.get_event_loop().create_task(_startup_ping())
except RuntimeError:
    pass

SYSTEM_PROMPT = (
    f"You are {BOT_NAME}, a fun, friendly Telegram group chatbot. "
    "Reply in Hinglish (mix of Hindi + English) when the user writes in Hinglish, "
    "otherwise match the user's language. Keep replies short (1-3 sentences), "
    "witty and casual, like a group friend — never robotic or overly formal."
)

_FALLBACK_REPLIES = [
    "haha ✅ sahi baat hai bro!",
    "arre wah, interesting! 😄",
    "hmm samajh gaya, aur batao?",
    "😂 ye toh mast tha!",
    "acha acha, chalte raho baat 👍",
    "kya scene hai bhai? 😎",
    "sahi pakde ho! 🔥",
]


def db_ready() -> bool:
    return _settings is not None


# ─── Mongo helpers ──────────────────────────────────────────────────────────

async def is_enabled(chat_id: int) -> bool:
    if not db_ready():
        return False
    try:
        doc = await _settings.find_one({"chat_id": chat_id})
        return bool(doc and doc.get("enabled", False))
    except Exception as e:
        print(f"[chatbot] mongo error in is_enabled: {e}")
        return False


async def set_enabled(chat_id: int, enabled: bool):
    if not db_ready():
        return
    await _settings.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id, "enabled": enabled}},
        upsert=True,
    )


async def add_sticker(chat_id: int, file_id: str, user_id: int):
    if _stickers is None:
        return
    await _stickers.update_one(
        {"chat_id": chat_id, "file_id": file_id},
        {"$set": {"chat_id": chat_id, "file_id": file_id,
                   "added_by": user_id, "added_at": time.time()}},
        upsert=True,
    )
    count = await _stickers.count_documents({"chat_id": chat_id})
    if count > STICKER_POOL_CAP:
        oldest = _stickers.find({"chat_id": chat_id}).sort("added_at", 1).limit(count - STICKER_POOL_CAP)
        async for doc in oldest:
            await _stickers.delete_one({"_id": doc["_id"]})


async def random_sticker(chat_id: int):
    if _stickers is None:
        return None
    pool = [doc["file_id"] async for doc in _stickers.find({"chat_id": chat_id})]
    return random.choice(pool) if pool else None


async def clear_stickers(chat_id: int):
    if _stickers is not None:
        await _stickers.delete_many({"chat_id": chat_id})


async def push_history(chat_id: int, role: str, content: str):
    if _history is None:
        return
    await _history.update_one(
        {"chat_id": chat_id},
        {"$push": {"turns": {"$each": [{"role": role, "content": content}],
                              "$slice": -HISTORY_LIMIT}}},
        upsert=True,
    )


async def get_history(chat_id: int) -> list:
    if _history is None:
        return []
    doc = await _history.find_one({"chat_id": chat_id})
    return doc.get("turns", []) if doc else []


# ─── GROQ AI reply ──────────────────────────────────────────────────────────

async def get_ai_reply(user_text: str, history: list) -> str:
    if not GROQ_API_KEY:
        return random.choice(_FALLBACK_REPLIES)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in history:
        if turn.get("role") in ("user", "assistant") and turn.get("content"):
            messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": user_text})

    payload = {"model": GROQ_MODEL, "messages": messages, "max_tokens": 200, "temperature": 0.8}
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

    try:
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(GROQ_URL, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    return random.choice(_FALLBACK_REPLIES)
                data = await resp.json()
                return data["choices"][0]["message"]["content"].strip() or random.choice(_FALLBACK_REPLIES)
    except Exception:
        return random.choice(_FALLBACK_REPLIES)


# ─── Admin / addressing helpers ─────────────────────────────────────────────

async def is_admin(chat_id: int, user_id: int) -> bool:
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status.value in ("administrator", "creator")
    except Exception:
        return False


def _is_addressed_to_bot(msg: Message) -> bool:
    if msg.reply_to_message and msg.reply_to_message.from_user and msg.reply_to_message.from_user.is_self:
        return True
    uname = BOT_USERNAME.lstrip("@").lower()
    text = (msg.text or msg.caption or "").lower()
    return f"@{uname}" in text


# ─── /chatbot on|off|status ─────────────────────────────────────────────────

@app.on_message(filters.command("chatbot"))
async def chatbot_cmd(_, msg: Message):
    if not db_ready():
        await msg.reply(f"⚠️ MONGO_URI sᴇᴛ ɴᴀʜɪ ʜᴀɪ, .env ᴍᴇ ᴅᴀᴀʟᴏ!\n\n<i>{POWERED_BY}</i>",
                         parse_mode=ParseMode.HTML)
        return

    if msg.chat.type.name != "PRIVATE" and not await is_admin(msg.chat.id, msg.from_user.id):
        await msg.reply(f"❌ ᴀᴅᴍɪɴs ᴏɴʟʏ!\n\n<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML)
        return

    args = msg.command
    if len(args) < 2 or args[1].lower() not in ("on", "off", "status"):
        await msg.reply(f"ᴜsᴀɢᴇ: /chatbot on | /chatbot off | /chatbot status\n\n<i>{POWERED_BY}</i>",
                         parse_mode=ParseMode.HTML)
        return

    action = args[1].lower()
    if action == "status":
        enabled = await is_enabled(msg.chat.id)
        state = "✅ ᴇɴᴀʙʟᴇᴅ" if enabled else "❌ ᴅɪsᴀʙʟᴇᴅ"
        await msg.reply(f"🤖 ᴄʜᴀᴛʙᴏᴛ: <b>{state}</b>\n\n<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML)
        return

    enable = action == "on"
    try:
        await set_enabled(msg.chat.id, enable)
    except Exception as e:
        print(f"[chatbot] mongo error in set_enabled: {e}")
        await msg.reply(
            f"❌ ᴍᴏɴɢᴏ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ғᴀɪʟᴇᴅ:\n<code>{e}</code>\n\n"
            f"ᴄʜᴇᴄᴋ ʏᴏᴜʀ MONGO_URI ᴀɴᴅ ᴀᴛʟᴀs ɪᴘ ᴡʜɪᴛᴇʟɪsᴛ (0.0.0.0/0).\n\n<i>{POWERED_BY}</i>",
            parse_mode=ParseMode.HTML,
        )
        return
    state = "✅ ᴇɴᴀʙʟᴇᴅ" if enable else "❌ ᴅɪsᴀʙʟᴇᴅ"
    extra = "\n\nᴛᴀʟᴋ ᴛᴏ ᴍᴇ ᴏʀ ᴛᴀɢ ᴍᴇ, ɪ'ʟʟ ʀᴇᴘʟʏ! 🤖" if enable else ""
    await msg.reply(f"🤖 ᴄʜᴀᴛʙᴏᴛ: <b>{state}</b>{extra}\n\n<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML)


@app.on_message(filters.command("resetstickers") & filters.group)
async def reset_stickers_cmd(_, msg: Message):
    if not await is_admin(msg.chat.id, msg.from_user.id):
        await msg.reply(f"❌ ᴀᴅᴍɪɴs ᴏɴʟʏ!\n\n<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML)
        return
    await clear_stickers(msg.chat.id)
    await msg.reply(f"🧹 sᴛɪᴄᴋᴇʀ ᴘᴏᴏʟ ᴄʟᴇᴀʀᴇᴅ!\n\n<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML)


# ─── Sticker: learn + reply ─────────────────────────────────────────────────

@app.on_message(filters.sticker & (filters.group | filters.private))
async def sticker_handler(_, msg: Message):
    if not db_ready() or not msg.from_user or msg.from_user.is_self:
        return
    if not await is_enabled(msg.chat.id):
        return

    await add_sticker(msg.chat.id, msg.sticker.file_id, msg.from_user.id)

    if msg.chat.type.name != "PRIVATE" and not (
        msg.reply_to_message and msg.reply_to_message.from_user and msg.reply_to_message.from_user.is_self
    ):
        return

    sticker_id = await random_sticker(msg.chat.id)
    try:
        if sticker_id:
            await msg.reply_sticker(sticker_id)
        else:
            await msg.reply("nice sticker! send a few more, i'm learning 🎭")
    except Exception:
        pass


# ─── Text: AI chatbot ────────────────────────────────────────────────────────

@app.on_message(
    filters.text
    & ~filters.command([
        "chatbot", "resetstickers", "start", "help", "ping", "stats", "welcome",
        "staff", "bots", "pin", "pinned", "unpin", "ban", "unban", "kick",
        "mute", "unmute", "settitle", "setdescription", "setdesc", "setphoto",
        "removephoto", "zombies", "imposter",
    ])
    & (filters.group | filters.private)
)
async def chatbot_text_handler(_, msg: Message):
    if not db_ready() or not msg.from_user or msg.from_user.is_self:
        return
    if not await is_enabled(msg.chat.id):
        return

    is_private = msg.chat.type.name == "PRIVATE"
    if not is_private and not _is_addressed_to_bot(msg):
        return

    user_text = (msg.text or "").strip()
    if not user_text:
        return

    try:
        await app.send_chat_action(msg.chat.id, "typing")
    except Exception:
        pass

    history = await get_history(msg.chat.id)
    reply_text = await get_ai_reply(user_text, history)

    await push_history(msg.chat.id, "user", user_text)
    await push_history(msg.chat.id, "assistant", reply_text)

    try:
        await msg.reply(reply_text)
    except Exception:
        pass
