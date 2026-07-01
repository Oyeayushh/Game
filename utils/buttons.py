"""
MadaraDefaultr – Button helpers (Kurigram styled)
Powered by Madara
"""

from kurigram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ── Premium emoji IDs (Telegram animated sticker IDs) ──────────────────────
EMOJI_FIRE      = "5368324170671202286"   # 🔥
EMOJI_TROPHY    = "5357419403668041957"   # 🏆
EMOJI_GEM       = "5368324170671202286"   # 💎
EMOJI_BOMB      = "5377205374646681534"   # 💣
EMOJI_CARD      = "5379748062124056162"   # 🃏
EMOJI_CROWN     = "5416112976804465315"   # 👑
EMOJI_STAR      = "5368324170671202286"   # ⭐
EMOJI_COIN      = "5368324170671202286"   # 🪙


def premium_emoji(emoji_id: str, fallback: str = "★") -> str:
    """Render a Telegram premium custom emoji."""
    return f'<emoji id="{emoji_id}">{fallback}</emoji>'


def btn(text: str, data: str = None, url: str = None) -> InlineKeyboardButton:
    """Generic inline button."""
    if url:
        return InlineKeyboardButton(text, url=url)
    return InlineKeyboardButton(text, callback_data=data)


def primary_btn(text: str, data: str = None, url: str = None) -> InlineKeyboardButton:
    """Blue (primary) styled button via Kurigram."""
    kwargs = {"button_type": "primary"}
    if url:
        return InlineKeyboardButton(text, url=url, **kwargs)
    return InlineKeyboardButton(text, callback_data=data, **kwargs)


def success_btn(text: str, data: str = None, url: str = None) -> InlineKeyboardButton:
    """Green (success) styled button via Kurigram."""
    kwargs = {"button_type": "success"}
    if url:
        return InlineKeyboardButton(text, url=url, **kwargs)
    return InlineKeyboardButton(text, callback_data=data, **kwargs)


def danger_btn(text: str, data: str = None, url: str = None) -> InlineKeyboardButton:
    """Red (danger) styled button via Kurigram."""
    kwargs = {"button_type": "danger"}
    if url:
        return InlineKeyboardButton(text, url=url, **kwargs)
    return InlineKeyboardButton(text, callback_data=data, **kwargs)


def keyboard(*rows) -> InlineKeyboardMarkup:
    """Build InlineKeyboardMarkup from rows of buttons."""
    return InlineKeyboardMarkup(list(rows))


# ── Preset keyboards ────────────────────────────────────────────────────────

def start_keyboard() -> InlineKeyboardMarkup:
    return keyboard(
        [primary_btn("🎮 Games Menu", data="games_menu"),
         success_btn("💰 My Wallet", data="wallet")],
        [btn("📊 Leaderboard", data="leaderboard"),
         btn("❓ Help", data="help")],
        [btn("➕ Add me to Group", url="https://t.me/SHRISTI_GAME_PLAYER_bot?startgroup=true")],
    )


def games_keyboard() -> InlineKeyboardMarkup:
    return keyboard(
        [primary_btn("🃏 Card Game", data="info_card"),
         danger_btn("💣 Bomb Game", data="info_bomb")],
        [success_btn("🔐 Hack Game", data="info_hack")],
        [btn("🔙 Back", data="start")],
    )


def flip_keyboard(available_cards: list) -> InlineKeyboardMarkup:
    """Show only cards that haven't been flipped yet."""
    label_map = {"a": "🅰️ A", "b": "🅱️ B", "c": "🃏 C", "d": "🎴 D"}
    row = [primary_btn(label_map[c], data=f"flip_{c}") for c in available_cards]
    return InlineKeyboardMarkup([row])


def bomb_join_keyboard(game_id: int) -> InlineKeyboardMarkup:
    return keyboard(
        [success_btn("💥 Join Game", data=f"bomb_join_{game_id}")],
        [danger_btn("❌ Cancel", data=f"bomb_cancel_{game_id}")],
    )


def bomb_pass_keyboard(game_id: int, players: list) -> InlineKeyboardMarkup:
    rows = []
    for uid, name in players:
        rows.append([primary_btn(f"👤 {name}", data=f"bomb_pass_{game_id}_{uid}")])
    return InlineKeyboardMarkup(rows)


def hack_keyboard() -> InlineKeyboardMarkup:
    return keyboard(
        [primary_btn("🔐 Register", data="hack_register"),
         success_btn("❓ How to play", data="hack_howto")],
    )
