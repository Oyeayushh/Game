"""
MadaraDefaultr – Start / Help / Wallet handlers
Powered by Madara
"""

import MadaraDefaultr as app
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, CallbackQuery
from database import get_or_create_user, get_top_users, get_user_rank
from utils.buttons import (
    start_keyboard, games_keyboard, keyboard,
    primary_btn, success_btn, danger_btn, btn, premium_emoji,
    E_TROPHY, E_CROWN, E_COIN, E_BULB, E_SWORD, E_CARD, E_BOMB,
    E_LOCK, E_SPARK, E_BACK, E_RANK, E_DIAMOND, E_FIRE, E_STAR,
)
from config import BOT_NAME, POWERED_BY, VERSION


# ═══════════════════════════════════════════════════════════════════════════════
#  /start
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_message(filters.command("start") & filters.private)
async def start_private(_, msg: Message):
    user = await get_or_create_user(
        msg.from_user.id,
        msg.from_user.username or "",
        msg.from_user.first_name or ""
    )
    name = msg.from_user.first_name or "Player"
    crown = premium_emoji(E_CROWN, "👑")
    fire  = premium_emoji(E_FIRE,  "🔥")
    coin  = premium_emoji(E_COIN,  "🪙")
    star  = premium_emoji(E_STAR,  "⭐")
    text = (
        f"{crown} <b>Welcome to {BOT_NAME}, {name}!</b> {crown}\n\n"
        f"{fire} The <b>ultimate gaming bot</b> on Telegram!\n"
        f"Play Card Games, Bomb Passes, Password Hacking — win coins & rule the leaderboard!\n\n"
        f"{coin} <b>Your Balance:</b> <code>{user['coins']:,}</code> coins\n"
        f"{star} <b>Wins:</b> <code>{user['wins']}</code>  "
        f"💔 <b>Losses:</b> <code>{user['losses']}</code>\n\n"
        f"<i>{POWERED_BY} | {VERSION}</i>"
    )
    await msg.reply(text, reply_markup=start_keyboard(), parse_mode=ParseMode.HTML)


@app.on_message(filters.command("start") & filters.group)
async def start_group(_, msg: Message):
    await get_or_create_user(
        msg.from_user.id,
        msg.from_user.username or "",
        msg.from_user.first_name or ""
    )
    fire = premium_emoji(E_FIRE, "🔥")
    text = (
        f"{fire} <b>{BOT_NAME} is here!</b>\n\n"
        f"🃏 /card — Card Flip Game\n"
        f"💣 /bomb — Bomb Passing Game\n"
        f"🔐 /hack — Password Hacking\n"
        f"💰 /balance — Your coins\n\n"
        f"Type /help for all commands.\n\n"
        f"<i>{POWERED_BY}</i>"
    )
    await msg.reply(text, reply_markup=start_keyboard(), parse_mode=ParseMode.HTML)


# ═══════════════════════════════════════════════════════════════════════════════
#  /help
# ═══════════════════════════════════════════════════════════════════════════════

HELP_TEXT = """
<b>🃏 Card Game</b>
/card — Start a new card game
/bet &lt;amount&gt; — Join an ongoing game
/flip a/b/c/d — Play your card this round

<b>💣 Bomb Game</b>
/bomb &lt;amount&gt; — Start with entry fee
/join &lt;amount&gt; — Join before game starts
/pass — Pass the bomb
/rank — Your rank
/leaders — Bomb leaderboard
/bombcancel — (Admin) Cancel & refund

<b>🔐 Hack Game</b>
/hack &lt;amount&gt; &lt;digit 3-6&gt; — Host a hack game
/register &lt;amount&gt; coins — Join the game
/guess &lt;number&gt; — Make your guess
/end — (Host) End the game

<b>💰 Wallet & Stats</b>
/balance — Your coin balance
/wallet — Full wallet overview
/top — Global leaderboard
"""


@app.on_message(filters.command("help"))
async def help_cmd(_, msg: Message):
    bulb = premium_emoji(E_BULB, "💡")
    await msg.reply(
        f"{bulb} <b>{BOT_NAME} — Command Guide</b>\n{HELP_TEXT}\n<i>{POWERED_BY}</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard(
            [primary_btn("🎮 Games", data="games_menu", emoji_id=E_SWORD)],
            [btn("🔙 Back to Start", data="start", emoji_id=E_BACK)],
        )
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  /balance  /wallet
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_message(filters.command(["balance", "wallet"]))
async def wallet_cmd(_, msg: Message):
    user = await get_or_create_user(
        msg.from_user.id,
        msg.from_user.username or "",
        msg.from_user.first_name or ""
    )
    rank = await get_user_rank(msg.from_user.id)
    name = msg.from_user.first_name or "Player"
    crown   = premium_emoji(E_CROWN,   "👑")
    coin    = premium_emoji(E_COIN,    "🪙")
    trophy  = premium_emoji(E_TROPHY,  "🏆")
    diamond = premium_emoji(E_DIAMOND, "💎")
    text = (
        f"{crown} <b>Wallet — {name}</b>\n\n"
        f"{coin} <b>Coins:</b> <code>{user['coins']:,}</code>\n"
        f"{trophy} <b>Wins:</b> <code>{user['wins']}</code>\n"
        f"💔 <b>Losses:</b> <code>{user['losses']}</code>\n"
        f"🎮 <b>Games Played:</b> <code>{user['games_played']}</code>\n"
        f"{diamond} <b>Global Rank:</b> #{rank}\n\n"
        f"<i>{POWERED_BY}</i>"
    )
    await msg.reply(text, parse_mode=ParseMode.HTML, reply_markup=keyboard(
        [primary_btn("🏆 Leaderboard", data="leaderboard", emoji_id=E_TROPHY)],
        [btn("🔙 Back", data="start", emoji_id=E_BACK)],
    ))


# ═══════════════════════════════════════════════════════════════════════════════
#  /top
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_message(filters.command("top"))
async def top_cmd(_, msg: Message):
    users = await get_top_users(10)
    medals = ["🥇", "🥈", "🥉"] + ["🔸"] * 7
    lines = []
    for i, u in enumerate(users):
        n = u["first_name"] or u["username"] or "Unknown"
        lines.append(f"{medals[i]} <b>{n}</b> — <code>{u['coins']:,}</code> coins")
    trophy = premium_emoji(E_TROPHY, "🏆")
    text = (
        f"{trophy} <b>Global Leaderboard</b>\n\n"
        + "\n".join(lines)
        + f"\n\n<i>{POWERED_BY}</i>"
    )
    await msg.reply(text, parse_mode=ParseMode.HTML)


# ═══════════════════════════════════════════════════════════════════════════════
#  Callback – navigation
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_callback_query(filters.regex("^start$"))
async def cb_start(_, cq: CallbackQuery):
    user = await get_or_create_user(
        cq.from_user.id,
        cq.from_user.username or "",
        cq.from_user.first_name or ""
    )
    name  = cq.from_user.first_name or "Player"
    crown = premium_emoji(E_CROWN, "👑")
    coin  = premium_emoji(E_COIN,  "🪙")
    fire  = premium_emoji(E_FIRE,  "🔥")
    text = (
        f"{crown} <b>Welcome back, {name}!</b>\n\n"
        f"{fire} <b>{BOT_NAME}</b>\n\n"
        f"{coin} <b>Balance:</b> <code>{user['coins']:,}</code> coins\n\n"
        f"<i>{POWERED_BY} | {VERSION}</i>"
    )
    await cq.edit_message_text(text, reply_markup=start_keyboard(), parse_mode=ParseMode.HTML)


@app.on_callback_query(filters.regex("^games_menu$"))
async def cb_games(_, cq: CallbackQuery):
    sword = premium_emoji(E_SWORD, "⚔️")
    await cq.edit_message_text(
        f"{sword} <b>Choose Your Game</b>\n\n"
        f"🃏 <b>Card Game</b> — flip cards, highest wins\n"
        f"💣 <b>Bomb Game</b> — pass the bomb, last alive wins\n"
        f"🔐 <b>Hack Game</b> — guess the secret password\n\n"
        f"<i>{POWERED_BY}</i>",
        reply_markup=games_keyboard(), parse_mode=ParseMode.HTML
    )


@app.on_callback_query(filters.regex("^wallet$"))
async def cb_wallet(_, cq: CallbackQuery):
    user = await get_or_create_user(
        cq.from_user.id,
        cq.from_user.username or "",
        cq.from_user.first_name or ""
    )
    rank    = await get_user_rank(cq.from_user.id)
    name    = cq.from_user.first_name or "Player"
    crown   = premium_emoji(E_CROWN,   "👑")
    coin    = premium_emoji(E_COIN,    "🪙")
    trophy  = premium_emoji(E_TROPHY,  "🏆")
    diamond = premium_emoji(E_DIAMOND, "💎")
    text = (
        f"{crown} <b>Wallet — {name}</b>\n\n"
        f"{coin} Coins: <code>{user['coins']:,}</code>\n"
        f"{trophy} Wins: <code>{user['wins']}</code>\n"
        f"💔 Losses: <code>{user['losses']}</code>\n"
        f"🎮 Games: <code>{user['games_played']}</code>\n"
        f"{diamond} Rank: #{rank}\n\n"
        f"<i>{POWERED_BY}</i>"
    )
    await cq.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard(
        [primary_btn("🏆 Leaderboard", data="leaderboard", emoji_id=E_TROPHY)],
        [btn("🔙 Back", data="start", emoji_id=E_BACK)],
    ))


@app.on_callback_query(filters.regex("^leaderboard$"))
async def cb_leaderboard(_, cq: CallbackQuery):
    users  = await get_top_users(10)
    medals = ["🥇", "🥈", "🥉"] + ["🔸"] * 7
    lines  = []
    for i, u in enumerate(users):
        n = u["first_name"] or u["username"] or "Unknown"
        lines.append(f"{medals[i]} <b>{n}</b> — <code>{u['coins']:,}</code>")
    trophy = premium_emoji(E_TROPHY, "🏆")
    text   = f"{trophy} <b>Global Leaderboard</b>\n\n" + "\n".join(lines) + f"\n\n<i>{POWERED_BY}</i>"
    await cq.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard(
        [btn("🔙 Back", data="start", emoji_id=E_BACK)],
    ))


@app.on_callback_query(filters.regex("^help$"))
async def cb_help(_, cq: CallbackQuery):
    bulb = premium_emoji(E_BULB, "💡")
    await cq.edit_message_text(
        f"{bulb} <b>{BOT_NAME} — Command Guide</b>\n{HELP_TEXT}\n<i>{POWERED_BY}</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard([btn("🔙 Back", data="start", emoji_id=E_BACK)])
    )


@app.on_callback_query(filters.regex("^info_card$"))
async def cb_info_card(_, cq: CallbackQuery):
    card = premium_emoji(E_CARD, "🃏")
    await cq.edit_message_text(
        f"{card} <b>Card Game Rules</b>\n\n"
        "• Each player gets 4 hidden cards: A, B, C, D\n"
        "• Cards sum is equal for all players — only strategy wins!\n"
        "• Each round, flip one card — highest card wins the round\n"
        "• 4 rounds total — highest score wins the pot 🏆\n"
        "• 60-second timer per turn (auto-play if you miss)\n"
        "• Each card can only be used once\n"
        "• Tie = random winner\n\n"
        "<b>Commands:</b>\n"
        "/card — Start | /bet &lt;amount&gt; — Join | /flip a/b/c/d — Play\n\n"
        f"<i>{POWERED_BY}</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard([btn("🔙 Back", data="games_menu", emoji_id=E_BACK)])
    )


@app.on_callback_query(filters.regex("^info_bomb$"))
async def cb_info_bomb(_, cq: CallbackQuery):
    bomb = premium_emoji(E_BOMB, "💣")
    await cq.edit_message_text(
        f"{bomb} <b>Bomb Game Rules</b>\n\n"
        "• Pay entry fee to join\n"
        "• A bomb is secretly assigned to one player\n"
        "• Use /pass to pass it — bomb explodes randomly each round 💥\n"
        "• Last player alive wins the pot!\n"
        "• Admins: /bombcancel to cancel & refund\n\n"
        "<b>Commands:</b>\n"
        "/bomb &lt;amount&gt; — Start | /join &lt;amount&gt; — Join\n"
        "/pass — Pass | /rank — Rank | /leaders — Leaderboard\n\n"
        f"<i>{POWERED_BY}</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard([btn("🔙 Back", data="games_menu", emoji_id=E_BACK)])
    )


@app.on_callback_query(filters.regex("^info_hack$"))
async def cb_info_hack(_, cq: CallbackQuery):
    lock = premium_emoji(E_LOCK, "🔐")
    await cq.edit_message_text(
        f"{lock} <b>Hack Game Rules</b>\n\n"
        "• Host sets a secret password (3-6 digits) + reward\n"
        "• Players register with an entry fee\n"
        "• Guess with /guess &lt;number&gt;\n"
        "• After each guess:\n"
        "  🟢 <b>HACKS</b> = correct digit, correct position\n"
        "  🟡 <b>GLITCHES</b> = correct digit, wrong position\n"
        "• First to crack it wins the pot!\n\n"
        "<b>Commands:</b>\n"
        "/hack &lt;amount&gt; &lt;digits&gt; — Host | /register &lt;amount&gt; — Join\n"
        "/guess &lt;pass&gt; — Guess | /end — End\n\n"
        f"<i>{POWERED_BY}</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard([btn("🔙 Back", data="games_menu", emoji_id=E_BACK)])
    )
