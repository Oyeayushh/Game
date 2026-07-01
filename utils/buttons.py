"""
MadaraDefaultr – Button helpers (Kurigram / pyrogram styled)
Powered by Madara
"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ButtonStyle

# ── Premium emoji IDs (Telegram animated custom emojis) ────────────────────
EMOJI_FIRE      = "5368324170671202286"
EMOJI_TROPHY    = "5357419403668041957"
EMOJI_BOMB      = "5377205374646681534"
EMOJI_CARD      = "5379748062124056162"
EMOJI_CROWN     = "5416112976804465315"
EMOJI_COIN      = "5368324170671202286"


def premium_emoji(emoji_id: str, fallback: str = "★") -> str:
    """Render a Telegram premium custom emoji (requires bot to have Premium)."""
    return f'<emoji id="{emoji_id}">{fallback}</emoji>'


# ── Button factories ────────────────────────────────────────────────────────

def btn(text: str, data: str = None, url: str = None) -> InlineKeyboardButton:
    if url:
        return InlineKeyboardButton(text, url=url)
    return InlineKeyboardButton(text, callback_data=data)


def primary_btn(text: str, data: str = None, url: str = None) -> InlineKeyboardButton:
    """Blue (primary) Kurigram coloured button."""
    if url:
        return InlineKeyboardButton(text, url=url, style=ButtonStyle.PRIMARY)
    return InlineKeyboardButton(text, callback_data=data, style=ButtonStyle.PRIMARY)


def success_btn(text: str, data: str = None, url: str = None) -> InlineKeyboardButton:
    """Green (success) Kurigram coloured button."""
    if url:
        return InlineKeyboardButton(text, url=url, style=ButtonStyle.SUCCESS)
    return InlineKeyboardButton(text, callback_data=data, style=ButtonStyle.SUCCESS)


def danger_btn(text: str, data: str = None, url: str = None) -> InlineKeyboardButton:
    """Red (danger) Kurigram coloured button."""
    if url:
        return InlineKeyboardButton(text, url=url, style=ButtonStyle.DANGER)
    return InlineKeyboardButton(text, callback_data=data, style=ButtonStyle.DANGER)


def keyboard(*rows) -> InlineKeyboardMarkup:
    """Build InlineKeyboardMarkup from rows of buttons."""
    return InlineKeyboardMarkup(list(rows))


# ── Card flip keyboard ──────────────────────────────────────────────────────

def flip_keyboard(available_cards: list) -> InlineKeyboardMarkup:
    label_map = {"a": "🅰️ A", "b": "🅱️ B", "c": "🃏 C", "d": "🎴 D"}
    row = [primary_btn(label_map[c], data=f"flip_{c}") for c in available_cards]
    return InlineKeyboardMarkup([row])


# ── Preset keyboards ────────────────────────────────────────────────────────

def start_keyboard() -> InlineKeyboardMarkup:
    return keyboard(
        [primary_btn("🎮 Games Menu", data="games_menu"),
         success_btn("💰 My Wallet", data="wallet")],
        [btn("📊 Leaderboard", data="leaderboard"),
         btn("❓ Help", data="help")],
        [btn("➕ Add me to Group",
             url="https://t.me/SHRISTI_GAME_PLAYER_bot?startgroup=true")],
    )


def games_keyboard() -> InlineKeyboardMarkup:
    return keyboard(
        [primary_btn("🃏 Card Game", data="info_card"),
         danger_btn("💣 Bomb Game",  data="info_bomb")],
        [success_btn("🔐 Hack Game", data="info_hack")],
        [btn("🔙 Back", data="start")],
    )


def bomb_join_keyboard(game_id: int) -> InlineKeyboardMarkup:
    return keyboard(
        [success_btn("💥 Join Game", data=f"bomb_join_{game_id}")],
        [danger_btn("❌ Cancel",     data=f"bcancel_{game_id}")],
    )
