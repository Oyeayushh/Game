"""
MadaraDefaultr – Safe messaging helpers
Powered by Madara

Use safe_send / safe_edit inside timers and background tasks where the
original trigger message may have been deleted by the time the coroutine
runs.  Falls back to chat send_message so coins / state are never silently
lost.
"""

import MadaraDefaultr as app
from pyrogram.enums import ParseMode


async def safe_send(chat_id: int, text: str, **kwargs) -> None:
    """Send a message to chat_id; never raises — logs errors instead."""
    kwargs.setdefault("parse_mode", ParseMode.HTML)
    try:
        await app.send_message(chat_id, text, **kwargs)
    except Exception as e:
        print(f"[safe_send] chat={chat_id} error={e}")


async def safe_reply(msg, text: str, **kwargs) -> None:
    """
    Try msg.reply(); if it fails (message deleted / chat unavailable)
    fall back to send_message on the same chat.
    """
    kwargs.setdefault("parse_mode", ParseMode.HTML)
    try:
        await msg.reply(text, **kwargs)
    except Exception:
        try:
            await app.send_message(msg.chat.id, text, **kwargs)
        except Exception as e:
            print(f"[safe_reply] chat={msg.chat.id} error={e}")


async def safe_edit(cq, text: str, **kwargs) -> None:
    """
    Try cq.edit_message_text(); if it fails fall back to answering the
    callback query with an alert so the user isn't left hanging.
    """
    kwargs.setdefault("parse_mode", ParseMode.HTML)
    try:
        await cq.edit_message_text(text, **kwargs)
    except Exception:
        try:
            await cq.answer(text[:200], show_alert=True)
        except Exception as e:
            print(f"[safe_edit] error={e}")
