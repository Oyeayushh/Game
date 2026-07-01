"""
MadaraDefaultr – Start / Help / Wallet handlers
Powered by Madara
"""

import MadaraDefaultr as app
from pyrogram import filters
from pyrogram.types import Message, CallbackQuery
from database import get_or_create_user, get_balance, get_top_users, get_user_rank
from utils.buttons import (
    start_keyboard, games_keyboard, keyboard,
    primary_btn, success_btn, danger_btn, btn, premium_emoji,
    EMOJI_TROPHY, EMOJI_CROWN, EMOJI_COIN,
)
from config import BOT_NAME, POWERED_BY, VERSION


# ═══════════════════════════════════════════════════════════════════════════════
#  /start
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_message(filters.command("start") & filters.private)
async def start_private(_, msg: Message):
    user = await get_or_create_user(msg.from_user.id,
                                    msg.from_user.username or "",
                                    msg.from_user.first_name or "")
    name = msg.from_user.first_name or "Player"
    text = (
        f"<b>🎮 Welcome to {BOT_NAME}, {name}!</b>\n\n"
        f"I'm your ultimate gaming bot. Play card games, bomb passes,\n"
        f"and password-hacking mini-games — win coins and climb the leaderboard!\n\n"
        f"💰 <b>Your Balance:</b> <code>{user['coins']:,}</code> coins\n\n"
        f"<i>{POWERED_BY} | {VERSION}</i>"
    )
    await msg.reply(text, reply_markup=start_keyboard(), parse_mode="html")


@app.on_message(filters.command("start") & filters.group)
async def start_group(_, msg: Message):
    await get_or_create_user(msg.from_user.id,
                             msg.from_user.username or "",
                             msg.from_user.first_name or "")
    text = (
        f"<b>🎮 {BOT_NAME} is here!</b>\n\n"
        f"Use <b>/card</b>, <b>/bomb</b>, or <b>/hack</b> to start a game.\n"
        f"Type /help for all commands.\n\n"
        f"<i>{POWERED_BY}</i>"
    )
    await msg.reply(text, reply_markup=start_keyboard(), parse_mode="html")


# ═══════════════════════════════════════════════════════════════════════════════
#  /help
# ═══════════════════════════════════════════════════════════════════════════════

HELP_TEXT = """
<b>🃏 Card Game</b>
/card — Start a new card game
/bet &lt;amount&gt; — Join an ongoing card game
/flip a/b/c/d — Play your move this round

<b>💣 Bomb Game</b>
/bomb &lt;amount&gt; — Start a bomb game with entry fee
/join &lt;amount&gt; — Join before the game starts
/pass — Pass the bomb to a random player
/rank — Check your or a friend's bomb rank
/leaders — Bomb game leaderboard
/bombcancel — (Admin) Cancel game & refund

<b>🔐 Hack Game</b>
/hack &lt;amount&gt; &lt;digit(3-6)&gt; — Start a hack game
/register &lt;amount&gt; &lt;coins/gems&gt; — Join & register
/guess &lt;password&gt; — Make your guess
/end — (Host only) End the game

<b>💰 Wallet</b>
/balance — Check your coin balance
/wallet — Full wallet overview
/top — Global leaderboard
"""


@app.on_message(filters.command("help"))
async def help_cmd(_, msg: Message):
    await msg.reply(
        f"<b>📋 {BOT_NAME} — All Commands</b>\n{HELP_TEXT}\n<i>{POWERED_BY}</i>",
        parse_mode="html",
        reply_markup=keyboard(
            [primary_btn("🎮 Games", data="games_menu")],
            [btn("🔙 Back to Start", data="start")],
        )
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  /balance  /wallet
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_message(filters.command(["balance", "wallet"]))
async def wallet_cmd(_, msg: Message):
    user = await get_or_create_user(msg.from_user.id,
                                    msg.from_user.username or "",
                                    msg.from_user.first_name or "")
    rank = await get_user_rank(msg.from_user.id)
    name = msg.from_user.first_name or "Player"
    text = (
        f"<b>💰 Wallet — {name}</b>\n\n"
        f"🪙 <b>Coins:</b> <code>{user['coins']:,}</code>\n"
        f"🏆 <b>Wins:</b> <code>{user['wins']}</code>\n"
        f"💔 <b>Losses:</b> <code>{user['losses']}</code>\n"
        f"🎮 <b>Games Played:</b> <code>{user['games_played']}</code>\n"
        f"📊 <b>Global Rank:</b> #{rank}\n\n"
        f"<i>{POWERED_BY}</i>"
    )
    await msg.reply(text, parse_mode="html", reply_markup=keyboard(
        [primary_btn("🔝 Leaderboard", data="leaderboard")],
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
    text = (
        f"<b>🏆 Global Leaderboard</b>\n\n"
        + "\n".join(lines)
        + f"\n\n<i>{POWERED_BY}</i>"
    )
    await msg.reply(text, parse_mode="html")


# ═══════════════════════════════════════════════════════════════════════════════
#  Callback – navigation buttons
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_callback_query(filters.regex("^start$"))
async def cb_start(_, cq: CallbackQuery):
    user = await get_or_create_user(cq.from_user.id,
                                    cq.from_user.username or "",
                                    cq.from_user.first_name or "")
    name = cq.from_user.first_name or "Player"
    text = (
        f"<b>🎮 Welcome to {BOT_NAME}, {name}!</b>\n\n"
        f"💰 <b>Balance:</b> <code>{user['coins']:,}</code> coins\n\n"
        f"<i>{POWERED_BY} | {VERSION}</i>"
    )
    await cq.edit_message_text(text, reply_markup=start_keyboard(), parse_mode="html")


@app.on_callback_query(filters.regex("^games_menu$"))
async def cb_games(_, cq: CallbackQuery):
    await cq.edit_message_text(
        f"<b>🎮 Choose a game</b>\n\n"
        f"🃏 <b>Card Game</b> – flip cards, highest wins\n"
        f"💣 <b>Bomb Game</b> – pass the bomb, last alive wins\n"
        f"🔐 <b>Hack Game</b> – guess the secret password\n\n"
        f"<i>{POWERED_BY}</i>",
        reply_markup=games_keyboard(), parse_mode="html"
    )


@app.on_callback_query(filters.regex("^wallet$"))
async def cb_wallet(_, cq: CallbackQuery):
    user = await get_or_create_user(cq.from_user.id,
                                    cq.from_user.username or "",
                                    cq.from_user.first_name or "")
    rank = await get_user_rank(cq.from_user.id)
    name = cq.from_user.first_name or "Player"
    text = (
        f"<b>💰 Wallet — {name}</b>\n\n"
        f"🪙 Coins: <code>{user['coins']:,}</code>\n"
        f"🏆 Wins: <code>{user['wins']}</code>\n"
        f"💔 Losses: <code>{user['losses']}</code>\n"
        f"🎮 Games: <code>{user['games_played']}</code>\n"
        f"📊 Rank: #{rank}\n\n"
        f"<i>{POWERED_BY}</i>"
    )
    await cq.edit_message_text(text, parse_mode="html", reply_markup=keyboard(
        [primary_btn("🔝 Leaderboard", data="leaderboard")],
        [btn("🔙 Back", data="start")],
    ))


@app.on_callback_query(filters.regex("^leaderboard$"))
async def cb_leaderboard(_, cq: CallbackQuery):
    users = await get_top_users(10)
    medals = ["🥇", "🥈", "🥉"] + ["🔸"] * 7
    lines = []
    for i, u in enumerate(users):
        n = u["first_name"] or u["username"] or "Unknown"
        lines.append(f"{medals[i]} <b>{n}</b> — <code>{u['coins']:,}</code>")
    text = "<b>🏆 Global Leaderboard</b>\n\n" + "\n".join(lines) + f"\n\n<i>{POWERED_BY}</i>"
    await cq.edit_message_text(text, parse_mode="html", reply_markup=keyboard(
        [btn("🔙 Back", data="start")],
    ))


@app.on_callback_query(filters.regex("^help$"))
async def cb_help(_, cq: CallbackQuery):
    await cq.edit_message_text(
        f"<b>📋 {BOT_NAME} — All Commands</b>\n{HELP_TEXT}\n<i>{POWERED_BY}</i>",
        parse_mode="html",
        reply_markup=keyboard([btn("🔙 Back", data="start")])
    )


@app.on_callback_query(filters.regex("^info_card$"))
async def cb_info_card(_, cq: CallbackQuery):
    await cq.edit_message_text(
        "<b>🃏 Card Game Rules</b>\n\n"
        "• Each player gets 4 hidden cards: A, B, C, D\n"
        "• Sum of all 4 cards is equal for every player (fair!)\n"
        "• Each round, pick one card to flip — highest card wins the round\n"
        "• 4 rounds total — highest total score wins 🏆\n"
        "• 60-second timer per turn (auto-play if you miss)\n"
        "• Each card can only be used once\n"
        "• Tie = random winner\n\n"
        "<b>Commands:</b>\n"
        "/card — Start game | /bet &lt;amount&gt; — Join | /flip a/b/c/d — Play\n\n"
        f"<i>{POWERED_BY}</i>",
        parse_mode="html",
        reply_markup=keyboard([btn("🔙 Back", data="games_menu")])
    )


@app.on_callback_query(filters.regex("^info_bomb$"))
async def cb_info_bomb(_, cq: CallbackQuery):
    await cq.edit_message_text(
        "<b>💣 Bomb Game Rules</b>\n\n"
        "• Pay entry fee to join\n"
        "• A bomb is randomly assigned to one player\n"
        "• Use /pass to pass the bomb to another player\n"
        "• Bomb explodes randomly every round 💥\n"
        "• Last player alive wins the pot!\n"
        "• Admins can cancel with /bombcancel (entry fees refunded)\n\n"
        "<b>Commands:</b>\n"
        "/bomb &lt;amount&gt; — Start | /join &lt;amount&gt; — Join\n"
        "/pass — Pass bomb | /rank — Your rank | /leaders — Leaderboard\n\n"
        f"<i>{POWERED_BY}</i>",
        parse_mode="html",
        reply_markup=keyboard([btn("🔙 Back", data="games_menu")])
    )


@app.on_callback_query(filters.regex("^info_hack$"))
async def cb_info_hack(_, cq: CallbackQuery):
    await cq.edit_message_text(
        "<b>🔐 Hack Game Rules</b>\n\n"
        "• Host sets a secret password (3-6 digits) and a reward\n"
        "• Players register to join the game\n"
        "• Make guesses with /guess &lt;number&gt;\n"
        "• After each guess you get:\n"
        "  🟢 <b>HACKS</b> = digits in the right position\n"
        "  🟡 <b>GLITCHES</b> = digits in wrong position\n"
        "• First to guess correctly wins the reward!\n"
        "• Only the host can end the game with /end\n\n"
        "<b>Commands:</b>\n"
        "/hack &lt;amount&gt; &lt;digits&gt; — Start | /register &lt;amount&gt; — Join\n"
        "/guess &lt;pass&gt; — Guess | /end — End game\n\n"
        f"<i>{POWERED_BY}</i>",
        parse_mode="html",
        reply_markup=keyboard([btn("🔙 Back", data="games_menu")])
    )
