"""
MadaraDefaultr – Logger + Broadcast Plugin
Powered by Madara

• Logs a message to LOGGER_ID whenever the bot is added to (or removed from) a group.
• Keeps a `chats` table updated so /broadcast can reach every known group.
• /broadcast <text>  (or reply to a message with /broadcast) — OWNER_ID only.
  Sends the message to every user and every group the bot knows about.

.env needed:
    LOGGER_ID=-100xxxxxxxxxx   (a channel/group id where logs should be sent)
    OWNER_ID=123456789         (your Telegram user id — only you can /broadcast)
"""

import asyncio

import MadaraDefaultr as app
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from config import LOGGER_ID, OWNER_ID, BOT_NAME, POWERED_BY, VERSION
from database import (
    add_chat, remove_chat, get_all_chats, get_all_users,
    get_chat_count, get_user_count,
)


async def _log(text: str):
    """Send a line to the log chat, silently ignoring failures (e.g. LOGGER_ID not set)."""
    if not LOGGER_ID:
        return
    try:
        await app.send_message(LOGGER_ID, text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except Exception as e:
        print(f"[logger] failed to send log: {e}")


async def log_new_user(user_id: int, username: str, first_name: str):
    tag = f"@{username}" if username else (first_name or "Unknown")
    await _log(
        f"🆕 <b>New user started the bot!</b>\n\n"
        f"👤 Name: {first_name or 'Unknown'}\n"
        f"🔗 Username: {tag}\n"
        f"🆔 ID: <code>{user_id}</code>\n\n"
        f"<i>{POWERED_BY}</i>"
    )


# ─── Passive chat tracking (so old groups are also known for /broadcast) ────

@app.on_message(filters.group, group=99)
async def _track_chat(_, msg: Message):
    try:
        await add_chat(msg.chat.id, msg.chat.title or "")
    except Exception:
        pass


# ─── Bot added to / removed from a group ───────────────────────────────────

@app.on_message(filters.new_chat_members)
async def bot_added_to_group(_, msg: Message):
    me = await app.get_me()
    added_ids = [u.id for u in msg.new_chat_members]
    if me.id not in added_ids:
        return  # some other member joined, not us — ignore

    await add_chat(msg.chat.id, msg.chat.title or "")

    adder = msg.from_user
    adder_mention = adder.mention if adder else "Unknown"
    try:
        members_count = await app.get_chat_members_count(msg.chat.id)
    except Exception:
        members_count = "N/A"

    await _log(
        f"➕ <b>Bot added to a new group!</b>\n\n"
        f"👥 Title: <b>{msg.chat.title}</b>\n"
        f"🆔 Chat ID: <code>{msg.chat.id}</code>\n"
        f"👤 Added by: {adder_mention}\n"
        f"👥 Members: <code>{members_count}</code>\n\n"
        f"<i>{POWERED_BY}</i>"
    )


@app.on_message(filters.left_chat_member)
async def bot_removed_from_group(_, msg: Message):
    me = await app.get_me()
    if not msg.left_chat_member or msg.left_chat_member.id != me.id:
        return  # someone else left, not us

    await remove_chat(msg.chat.id)
    await _log(
        f"➖ <b>Bot removed from a group.</b>\n\n"
        f"👥 Title: <b>{msg.chat.title}</b>\n"
        f"🆔 Chat ID: <code>{msg.chat.id}</code>\n\n"
        f"<i>{POWERED_BY}</i>"
    )


# ─── /broadcast ─────────────────────────────────────────────────────────────

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID or 0))
async def broadcast_cmd(_, msg: Message):
    if not msg.reply_to_message and len(msg.command) < 2:
        await msg.reply(
            f"ᴜsᴀɢᴇ:\n"
            f"• <code>/broadcast your message here</code>\n"
            f"• ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ <code>/broadcast</code>\n\n"
            f"<i>{POWERED_BY}</i>",
            parse_mode=ParseMode.HTML,
        )
        return

    users = await get_all_users()
    chats = await get_all_chats()
    targets = users + chats

    status = await msg.reply(
        f"📢 ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴛᴏ <b>{len(users)}</b> ᴜsᴇʀs & <b>{len(chats)}</b> ɢʀᴏᴜᴘs…",
        parse_mode=ParseMode.HTML,
    )

    sent, failed = 0, 0
    for target_id in targets:
        try:
            if msg.reply_to_message:
                await msg.reply_to_message.copy(target_id)
            else:
                text = msg.text.split(None, 1)[1]
                await app.send_message(target_id, text)
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)  # gentle flood control

    await status.edit_text(
        f"✅ <b>Broadcast complete!</b>\n\n"
        f"📨 Sent: <code>{sent}</code>\n"
        f"❌ Failed: <code>{failed}</code>\n\n"
        f"<i>{POWERED_BY}</i>",
        parse_mode=ParseMode.HTML,
    )
