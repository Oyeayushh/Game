"""
MadaraDefaultr – Button helpers (Kurigram styled, small-caps labels)
Powered by Madara
"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ButtonStyle


# ── Factories ────────────────────────────────────────────────────────────────

def btn(text: str, data: str = None, url: str = None) -> InlineKeyboardButton:
    if url:
        return InlineKeyboardButton(text, url=url)
    return InlineKeyboardButton(text, callback_data=data)


def primary_btn(text: str, data: str = None, url: str = None) -> InlineKeyboardButton:
    if url:
        return InlineKeyboardButton(text, url=url, style=ButtonStyle.PRIMARY)
    return InlineKeyboardButton(text, callback_data=data, style=ButtonStyle.PRIMARY)


def success_btn(text: str, data: str = None, url: str = None) -> InlineKeyboardButton:
    if url:
        return InlineKeyboardButton(text, url=url, style=ButtonStyle.SUCCESS)
    return InlineKeyboardButton(text, callback_data=data, style=ButtonStyle.SUCCESS)


def danger_btn(text: str, data: str = None, url: str = None) -> InlineKeyboardButton:
    if url:
        return InlineKeyboardButton(text, url=url, style=ButtonStyle.DANGER)
    return InlineKeyboardButton(text, callback_data=data, style=ButtonStyle.DANGER)


def keyboard(*rows) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(list(rows))


# ── Preset keyboards ─────────────────────────────────────────────────────────

def start_keyboard() -> InlineKeyboardMarkup:
    return keyboard(
        [primary_btn("🎮 ɢᴀᴍᴇs ᴍᴇɴᴜ",   data="games_menu"),
         success_btn("💰 ᴍʏ ᴡᴀʟʟᴇᴛ",     data="wallet")],
        [btn("📖 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs",       data="help_menu"),
         btn("🏆 ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ",           data="leaderboard")],
        [primary_btn("➕ ᴀᴅᴅ ᴛᴏ ɢʀᴏᴜᴘ",
                     url="https://t.me/SHRISTI_GAME_PLAYER_bot?startgroup=true")],
    )


def help_menu_keyboard() -> InlineKeyboardMarkup:
    return keyboard(
        [primary_btn("🎮 ɢᴀᴍᴇs",        data="help_games"),
         success_btn("💰 ᴇᴄᴏɴᴏᴍʏ",      data="help_economy")],
        [btn("💘 sᴏᴄɪᴀʟ & ʀᴏᴍᴀɴᴄᴇ",    data="help_social"),
         danger_btn("⚔️ ʀᴘɢ & ᴄᴏᴍʙᴀᴛ", data="help_combat")],
        [btn("⛩️ ɢʀᴏᴜᴘ ᴍɢᴍᴛ",           data="help_group"),
         btn("🔙 ʙᴀᴄᴋ",                  data="start")],
    )


def games_keyboard() -> InlineKeyboardMarkup:
    return keyboard(
        [primary_btn("🃏 ᴄᴀʀᴅ ɢᴀᴍᴇ",  data="info_card"),
         danger_btn("💣 ʙᴏᴍʙ ɢᴀᴍᴇ",   data="info_bomb")],
        [success_btn("🔐 ʜᴀᴄᴋ ɢᴀᴍᴇ",  data="info_hack")],
        [btn("🔙 ʙᴀᴄᴋ",                data="start")],
    )


def help_back_keyboard(back: str = "help_menu") -> InlineKeyboardMarkup:
    return keyboard([btn("🔙 ʙᴀᴄᴋ ᴛᴏ ʜᴇʟᴘ", data=back)])


def flip_keyboard(available_cards: list) -> InlineKeyboardMarkup:
    label_map = {"a": "🅰️ ᴀ", "b": "🅱️ ʙ", "c": "🃏 ᴄ", "d": "🎴 ᴅ"}
    row = [primary_btn(label_map[c], data=f"flip_{c}") for c in available_cards]
    return InlineKeyboardMarkup([row])


def shop_keyboard() -> InlineKeyboardMarkup:
    return keyboard(
        [primary_btn("🔪 ᴋɴɪғᴇ — 1,000",  data="buy_knife"),
         primary_btn("🔫 ɢᴜɴ — 2,500",     data="buy_gun")],
        [primary_btn("⚔️ sᴡᴏʀᴅ — 5,000",  data="buy_sword")],
        [success_btn("🛡️ sʜɪᴇʟᴅ — 1,500", data="buy_shield"),
         success_btn("🦺 ᴠᴇsᴛ — 3,000",   data="buy_vest")],
        [btn("🔙 ʙᴀᴄᴋ",                   data="help_economy")],
    )
