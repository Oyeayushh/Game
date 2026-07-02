"""
MadaraDefaultr – Economy & Trading System
Powered by Madara
"""

import time
import MadaraDefaultr as app
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, CallbackQuery
from database import (
    get_or_create_user, get_balance, update_coins,
    get_relationship, get_daily, set_daily,
    get_group_claim, set_group_claim,
    get_inventory, add_item, has_item, get_user_rank
)
from utils.buttons import keyboard, primary_btn, success_btn, danger_btn, btn, shop_keyboard
from config import (
    POWERED_BY, DAILY_BASE, DAILY_COOLDOWN, CLAIM_AMOUNT, CLAIM_COOLDOWN,
    TRANSFER_TAX, TRANSFER_TAX_MARRIED, SHOP_ITEMS
)


# ─── /bal [@user] ─────────────────────────────────────────────────────────────

@app.on_message(filters.command(["bal", "balance", "wallet"]))
async def bal_cmd(_, msg: Message):
    target = msg.reply_to_message.from_user if msg.reply_to_message else msg.from_user
    user   = await get_or_create_user(target.id, target.username or "", target.first_name or "")
    rank   = await get_user_rank(target.id)
    rel    = await get_relationship(target.id)
    name   = target.first_name or "ᴘʟᴀʏᴇʀ"

    married = "💑 ᴍᴀʀʀɪᴇᴅ" if rel["status"] == "married" else "💔 sɪɴɢʟᴇ"

    await msg.reply(
        f"👑 <b>ᴡᴀʟʟᴇᴛ — {name}</b>\n\n"
        f"🪙 ᴄᴏɪɴs: <code>{user['coins']:,}</code>\n"
        f"🏆 ᴡɪɴs: <code>{user['wins']}</code>\n"
        f"💔 ʟᴏssᴇs: <code>{user['losses']}</code>\n"
        f"🎮 ɢᴀᴍᴇs: <code>{user['games_played']}</code>\n"
        f"💎 ʀᴀɴᴋ: <b>#{rank}</b>\n"
        f"❤️ sᴛᴀᴛᴜs: {married}\n\n"
        f"<i>{POWERED_BY}</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard(
            [primary_btn("🏆 ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ", data="leaderboard")],
            [btn("🔙 ʙᴀᴄᴋ", data="start")],
        )
    )


# ─── /give [amount] [@user] ───────────────────────────────────────────────────

@app.on_message(filters.command("give") & filters.group)
async def give_cmd(_, msg: Message):
    if not msg.reply_to_message:
        await msg.reply(
            f"💸 ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ + /give <amount>\n\n<i>{POWERED_BY}</i>",
            parse_mode=ParseMode.HTML
        )
        return

    sender = msg.from_user
    recvr  = msg.reply_to_message.from_user

    if recvr.is_bot or recvr.id == sender.id:
        await msg.reply(f"❌ ɪɴᴠᴀʟɪᴅ ᴛᴀʀɢᴇᴛ!\n\n<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML)
        return

    args = msg.command
    if len(args) < 2:
        await msg.reply(
            f"ᴜsᴀɢᴇ: /give <amount> (ʀᴇᴘʟʏ ᴛᴏ ᴛᴀʀɢᴇᴛ)\n\n<i>{POWERED_BY}</i>",
            parse_mode=ParseMode.HTML
        )
        return

    try:
        amount = int(args[1])
        assert amount > 0
    except (ValueError, AssertionError):
        await msg.reply(f"❌ ɪɴᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ!\n\n<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML)
        return

    s_user = await get_or_create_user(sender.id, sender.username or "", sender.first_name or "")
    await get_or_create_user(recvr.id, recvr.username or "", recvr.first_name or "")

    if s_user["coins"] < amount:
        await msg.reply(
            f"❌ ɪɴsᴜғғɪᴄɪᴇɴᴛ ʙᴀʟᴀɴᴄᴇ!\n"
            f"🪙 ʏᴏᴜ ʜᴀᴠᴇ: <code>{s_user['coins']:,}</code>\n\n"
            f"<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML
        )
        return

    # Married = 5% tax, else 10%
    rel   = await get_relationship(sender.id)
    is_married = (rel["status"] == "married" and rel["partner_id"] == recvr.id)
    tax   = TRANSFER_TAX_MARRIED if is_married else TRANSFER_TAX
    fee   = int(amount * tax)
    net   = amount - fee

    await update_coins(sender.id, -amount)
    await update_coins(recvr.id,   net)

    await msg.reply(
        f"💸 <b>ᴛʀᴀɴsғᴇʀ ᴄᴏᴍᴘʟᴇᴛᴇ!</b>\n\n"
        f"👤 ғʀᴏᴍ: <b>{sender.first_name}</b>\n"
        f"👤 ᴛᴏ: <b>{recvr.first_name}</b>\n"
        f"💰 ᴀᴍᴏᴜɴᴛ: <code>{amount:,}</code>\n"
        f"💸 ᴛᴀx ({int(tax*100)}%): <code>{fee:,}</code>\n"
        f"✅ ɴᴇᴛ ʀᴇᴄᴇɪᴠᴇᴅ: <code>{net:,}</code>\n\n"
        f"<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML
    )


# ─── /claim ───────────────────────────────────────────────────────────────────

@app.on_message(filters.command("claim") & filters.group)
async def claim_cmd(_, msg: Message):
    uid     = msg.from_user.id
    chat_id = msg.chat.id
    await get_or_create_user(uid, msg.from_user.username or "", msg.from_user.first_name or "")

    last   = await get_group_claim(uid, chat_id)
    now    = time.time()
    elapsed = now - last

    if elapsed < CLAIM_COOLDOWN:
        left_h = int((CLAIM_COOLDOWN - elapsed) // 3600)
        left_m = int(((CLAIM_COOLDOWN - elapsed) % 3600) // 60)
        await msg.reply(
            f"⏳ ᴀʟʀᴇᴀᴅʏ ᴄʟᴀɪᴍᴇᴅ! ᴄᴏᴍᴇ ʙᴀᴄᴋ ɪɴ <b>{left_h}h {left_m}m</b>.\n\n"
            f"<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML
        )
        return

    await update_coins(uid, CLAIM_AMOUNT)
    await set_group_claim(uid, chat_id)

    await msg.reply(
        f"🎁 <b>ɢʀᴏᴜᴘ ʙᴏɴᴜs ᴄʟᴀɪᴍᴇᴅ!</b>\n\n"
        f"💰 <code>+{CLAIM_AMOUNT:,}</code> ᴄᴏɪɴs ᴀᴅᴅᴇᴅ!\n"
        f"⏰ ɴᴇxᴛ ᴄʟᴀɪᴍ ɪɴ 24 ʜᴏᴜʀs.\n\n"
        f"<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML
    )


# ─── /daily ───────────────────────────────────────────────────────────────────

@app.on_message(filters.command("daily"))
async def daily_cmd(_, msg: Message):
    uid  = msg.from_user.id
    await get_or_create_user(uid, msg.from_user.username or "", msg.from_user.first_name or "")
    d    = await get_daily(uid)
    now  = time.time()
    elapsed = now - d["last_daily"]

    if elapsed < DAILY_COOLDOWN:
        left_h = int((DAILY_COOLDOWN - elapsed) // 3600)
        left_m = int(((DAILY_COOLDOWN - elapsed) % 3600) // 60)
        await msg.reply(
            f"⏳ ᴀʟʀᴇᴀᴅʏ ᴄʟᴀɪᴍᴇᴅ ᴛᴏᴅᴀʏ!\n"
            f"⏰ ᴄᴏᴍᴇ ʙᴀᴄᴋ ɪɴ <b>{left_h}h {left_m}m</b>.\n"
            f"🔥 sᴛʀᴇᴀᴋ: <code>{d['streak']}</code> ᴅᴀʏs\n\n"
            f"<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML
        )
        return

    # Streak: reset if >48h gap
    streak = (d["streak"] + 1) if elapsed < 172800 else 1
    reward = DAILY_BASE + (streak - 1) * 250
    if streak % 7 == 0:
        reward += 1000  # weekly bonus

    await update_coins(uid, reward)
    await set_daily(uid, streak)

    streak_bar = "🔥" * min(streak, 7) + "⬜" * max(0, 7 - streak)

    await msg.reply(
        f"📅 <b>ᴅᴀɪʟʏ ʀᴇᴡᴀʀᴅ ᴄʟᴀɪᴍᴇᴅ!</b>\n\n"
        f"💰 ʀᴇᴡᴀʀᴅ: <code>+{reward:,}</code> ᴄᴏɪɴs\n"
        f"🔥 sᴛʀᴇᴀᴋ: <code>{streak}</code> ᴅᴀʏs\n"
        f"{streak_bar}\n"
        + (f"🎉 ᴡᴇᴇᴋʟʏ ʙᴏɴᴜs +1,000!\n" if streak % 7 == 0 else "") +
        f"\n<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML
    )


# ─── /shop ────────────────────────────────────────────────────────────────────

@app.on_message(filters.command("shop"))
async def shop_cmd(_, msg: Message):
    lines = []
    for key, item in SHOP_ITEMS.items():
        lines.append(f"{item['name']} — <code>{item['price']:,}</code> ᴄᴏɪɴs\n  ↳ {item['desc']}")

    await msg.reply(
        f"🛒 <b>ᴍᴀᴅᴀʀᴀ sʜᴏᴘ</b>\n\n" +
        "\n\n".join(lines) +
        f"\n\n<i>ᴛᴀᴘ ᴀ ʙᴜᴛᴛᴏɴ ᴛᴏ ʙᴜʏ:</i>\n\n{POWERED_BY}",
        parse_mode=ParseMode.HTML,
        reply_markup=shop_keyboard()
    )


@app.on_callback_query(filters.regex(r"^buy_(\w+)$"))
async def cb_buy(_, cq: CallbackQuery):
    item_key = cq.matches[0].group(1)
    if item_key not in SHOP_ITEMS:
        await cq.answer("❌ ɪᴛᴇᴍ ɴᴏᴛ ғᴏᴜɴᴅ!", show_alert=True)
        return

    item = SHOP_ITEMS[item_key]
    uid  = cq.from_user.id
    user = await get_or_create_user(uid, cq.from_user.username or "", cq.from_user.first_name or "")

    if await has_item(uid, item_key):
        await cq.answer(f"ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ᴏᴡɴ {item['name']}!", show_alert=True)
        return

    if user["coins"] < item["price"]:
        await cq.answer(
            f"❌ ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴄᴏɪɴs! ɴᴇᴇᴅ {item['price']:,}", show_alert=True
        )
        return

    await update_coins(uid, -item["price"])
    await add_item(uid, item_key)
    await cq.answer(f"✅ ᴘᴜʀᴄʜᴀsᴇᴅ {item['name']}!", show_alert=True)


# ─── /inventory ───────────────────────────────────────────────────────────────

@app.on_message(filters.command("inventory"))
async def inventory_cmd(_, msg: Message):
    uid   = msg.from_user.id
    name  = msg.from_user.first_name or "ᴘʟᴀʏᴇʀ"
    await get_or_create_user(uid, msg.from_user.username or "", msg.from_user.first_name or "")
    items = await get_inventory(uid)

    if not items:
        await msg.reply(
            f"🎒 <b>ɪɴᴠᴇɴᴛᴏʀʏ — {name}</b>\n\n"
            f"ᴇᴍᴘᴛʏ! ᴠɪsɪᴛ /shop ᴛᴏ ʙᴜʏ ɪᴛᴇᴍs.\n\n"
            f"<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML
        )
        return

    lines = []
    for it in items:
        info = SHOP_ITEMS.get(it, {"name": it, "desc": ""})
        lines.append(f"• {info['name']} — {info['desc']}")

    await msg.reply(
        f"🎒 <b>ɪɴᴠᴇɴᴛᴏʀʏ — {name}</b>\n\n" +
        "\n".join(lines) +
        f"\n\n<i>{POWERED_BY}</i>", parse_mode=ParseMode.HTML
    )
