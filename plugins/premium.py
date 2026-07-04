"""
MadaraDefaultr – Premium Plugin
Powered by Madara

Commands:
  /addpremium <days>       (reply to a user)  -> OWNER_ID only. days=0 = lifetime
  /removepremium           (reply to a user)  -> OWNER_ID only
  /premium                 -> check your own (or replied user's) premium status
  /premiumlist             -> OWNER_ID only, list all premium users

Perks for premium users (applied in plugins/economy.py):
  • 2x /daily reward
  • Half /claim cooldown
"""

import MadaraDefaultr as app
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from config import OWNER_ID, POWERED_BY
from database import (
    add_premium, remove_premium, get_premium, get_all_premium,
    get_or_create_user,
)


def _fmt_expiry(row: dict) -> str:
    if not row["expires_at"]:
        return "♾️ ʟɪғᴇᴛɪᴍᴇ"
    import datetime
    dt = datetime.datetime.fromtimestamp(row["expires_at"])
    return f"📅 ᴜɴᴛɪʟ <code>{dt.strftime('%d %b %Y, %H:%M')}</code>"


# ─── /addpremium <days> (reply) ─────────────────────────────────────────────

@app.on_message(filters.command("addpremium") & filters.user(OWNER_ID or 0))
async def addpremium_cmd(_, msg: Message):
    if not msg.reply_to_message:
        await msg.reply(
            f"ᴜsᴀɢᴇ: ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴡɪᴛʜ <code>/addpremium &lt;days&gt;</code>\n"
            f"(ᴜsᴇ <code>0</code> ғᴏʀ ʟɪғᴇᴛɪᴍᴇ)\n\n<i>{POWERED_BY}</i>",
            parse_mode=ParseMode.HTML,
        )
        return

    args = msg.command
    try:
        days = int(args[1]) if len(args) >= 2 else 30
    except ValueError:
        await msg.reply(f"❌ ɪɴᴠᴀʟɪᴅ ᴅᴀʏs!\n\n<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML)
        return

    target = msg.reply_to_message.from_user
    await get_or_create_user(target.id, target.username or "", target.first_name or "")
    await add_premium(target.id, days, added_by=msg.from_user.id)

    duration = "♾️ ʟɪғᴇᴛɪᴍᴇ" if days <= 0 else f"{days} ᴅᴀʏs"
    await msg.reply(
        f"✅ <b>{target.first_name}</b> ɪs ɴᴏᴡ ᴘʀᴇᴍɪᴜᴍ!\n"
        f"⏳ ᴅᴜʀᴀᴛɪᴏɴ: <b>{duration}</b>\n\n"
        f"ᴘᴇʀᴋs: 2x /daily ʀᴇᴡᴀʀᴅ, ʜᴀʟғ /claim ᴄᴏᴏʟᴅᴏᴡɴ 💎\n\n<i>{POWERED_BY}</i>",
        parse_mode=ParseMode.HTML,
    )


# ─── /removepremium (reply) ─────────────────────────────────────────────────

@app.on_message(filters.command("removepremium") & filters.user(OWNER_ID or 0))
async def removepremium_cmd(_, msg: Message):
    if not msg.reply_to_message:
        await msg.reply(
            f"ᴜsᴀɢᴇ: ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴡɪᴛʜ <code>/removepremium</code>\n\n<i>{POWERED_BY}</i>",
            parse_mode=ParseMode.HTML,
        )
        return

    target = msg.reply_to_message.from_user
    await remove_premium(target.id)
    await msg.reply(
        f"❌ ᴘʀᴇᴍɪᴜᴍ ʀᴇᴍᴏᴠᴇᴅ ғᴏʀ <b>{target.first_name}</b>.\n\n<i>{POWERED_BY}</i>",
        parse_mode=ParseMode.HTML,
    )


# ─── /premium (self or reply) ────────────────────────────────────────────────

@app.on_message(filters.command("premium"))
async def premium_cmd(_, msg: Message):
    target = msg.reply_to_message.from_user if msg.reply_to_message else msg.from_user
    row = await get_premium(target.id)
    name = target.first_name or "ᴘʟᴀʏᴇʀ"

    if not row:
        await msg.reply(
            f"❌ <b>{name}</b> ɪs ɴᴏᴛ ᴘʀᴇᴍɪᴜᴍ.\n\n<i>{POWERED_BY}</i>",
            parse_mode=ParseMode.HTML,
        )
        return

    await msg.reply(
        f"💎 <b>{name} ɪs ᴘʀᴇᴍɪᴜᴍ!</b>\n\n"
        f"{_fmt_expiry(row)}\n\n"
        f"ᴘᴇʀᴋs: 2x /daily ʀᴇᴡᴀʀᴅ, ʜᴀʟғ /claim ᴄᴏᴏʟᴅᴏᴡɴ ⚡\n\n<i>{POWERED_BY}</i>",
        parse_mode=ParseMode.HTML,
    )


# ─── /premiumlist ───────────────────────────────────────────────────────────

@app.on_message(filters.command("premiumlist") & filters.user(OWNER_ID or 0))
async def premiumlist_cmd(_, msg: Message):
    rows = await get_all_premium()
    if not rows:
        await msg.reply(f"📃 ɴᴏ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ʏᴇᴛ.\n\n<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML)
        return

    lines = [f"• <code>{r['user_id']}</code> — {_fmt_expiry(r)}" for r in rows]
    await msg.reply(
        f"💎 <b>ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ({len(rows)})</b>\n\n" + "\n".join(lines) + f"\n\n<i>{POWERED_BY}</i>",
        parse_mode=ParseMode.HTML,
    )
