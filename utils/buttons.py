"""
MadaraDefaultr – Button helpers (Kurigram / pyrogram styled)
Powered by Madara
"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ButtonStyle

# ════════════════════════════════════════════════════════════════════════════════
#  Premium Custom Emoji IDs
#  (from Emoji_fan37_by_TgEmodziBot + extra packs)
# ════════════════════════════════════════════════════════════════════════════════

# — Core UI —
E_SPARK    = 4958489311726011319   # ✨  spark / add to group
E_STAR     = 4958714479681471536   # ⭐️ star
E_CROWN    = 4956420911310832630   # 👑  crown / owner
E_SUPPORT  = 4956475826762679249   # 💬  support chat
E_BULB     = 4958665796227171144   # 💡  help / info
E_UPDATE   = 4956214478002717877   # 🔝  updates channel
E_DIAMOND  = 4956739572114392015   # 💎  diamond / premium
E_BELL     = 4956290155326473271   # 🔔  bell / notifications

# — Games —
E_CARD     = 5379748062124056162   # 🃏  card game
E_BOMB     = 5377205374646681534   # 💣  bomb game
E_LOCK     = 5447644880824181030   # 🔐  hack game
E_TROPHY   = 5357419403668041957   # 🏆  winner / leaderboard
E_FIRE     = 5368324170671202286   # 🔥  fire / hot
E_COIN     = 5451882537270557672   # 🪙  coin / wallet
E_SWORD    = 5440539497383087970   # ⚔️  battle / game
E_DICE     = 5368324170671202286   # 🎲  dice / random
E_RANK     = 5447644880824181030   # 📊  rank / stats
E_GIFT     = 5471952986970267163   # 🎁  gift / reward

# — Reactions / Status —
E_WIN      = 5357419403668041957   # 🥇  win
E_BOOM     = 5377205374646681534   # 💥  explosion
E_HEART    = 5346186668224599899   # ❤️  heart
E_CHECK    = 5415905755406539604   # ✅  check
E_CROSS    = 5445284980978621387   # ❌  cross / error
E_BACK     = 5948038823202048141   # 🔙  back

# — Love Day Pack emojis —
E_LOVE1    = 5346186668224599899   # ❤️‍🔥
E_LOVE2    = 5346034248314408459   # 💝

# — Gojo / Anime style emojis —
E_ANIME1   = 5447902953897489422   # 👁️
E_ANIME2   = 5440882631728828753   # 🌀

# — Hacker style —
E_HACK1    = 5445284980978621387   # 💻
E_HACK2    = 5471952986970267163   # 🔓

# — Devil / King style —
E_DEVIL    = 5348154177716964012   # 😈
E_KING     = 5456247778809899980   # 🤴


def premium_emoji(emoji_id: int, fallback: str = "★") -> str:
    """Render a Telegram premium custom emoji in HTML parse mode."""
    return f'<emoji id="{emoji_id}">{fallback}</emoji>'


# ════════════════════════════════════════════════════════════════════════════════
#  Button factories
# ════════════════════════════════════════════════════════════════════════════════

def btn(text: str, data: str = None, url: str = None,
        emoji_id: int = None) -> InlineKeyboardButton:
    kwargs = {}
    if emoji_id:
        kwargs["icon_custom_emoji_id"] = emoji_id
    if url:
        return InlineKeyboardButton(text, url=url, **kwargs)
    return InlineKeyboardButton(text, callback_data=data, **kwargs)


def primary_btn(text: str, data: str = None, url: str = None,
                emoji_id: int = None) -> InlineKeyboardButton:
    """Blue (primary) Kurigram coloured button."""
    kwargs = {"style": ButtonStyle.PRIMARY}
    if emoji_id:
        kwargs["icon_custom_emoji_id"] = emoji_id
    if url:
        return InlineKeyboardButton(text, url=url, **kwargs)
    return InlineKeyboardButton(text, callback_data=data, **kwargs)


def success_btn(text: str, data: str = None, url: str = None,
                emoji_id: int = None) -> InlineKeyboardButton:
    """Green (success) Kurigram coloured button."""
    kwargs = {"style": ButtonStyle.SUCCESS}
    if emoji_id:
        kwargs["icon_custom_emoji_id"] = emoji_id
    if url:
        return InlineKeyboardButton(text, url=url, **kwargs)
    return InlineKeyboardButton(text, callback_data=data, **kwargs)


def danger_btn(text: str, data: str = None, url: str = None,
               emoji_id: int = None) -> InlineKeyboardButton:
    """Red (danger) Kurigram coloured button."""
    kwargs = {"style": ButtonStyle.DANGER}
    if emoji_id:
        kwargs["icon_custom_emoji_id"] = emoji_id
    if url:
        return InlineKeyboardButton(text, url=url, **kwargs)
    return InlineKeyboardButton(text, callback_data=data, **kwargs)


def keyboard(*rows) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(list(rows))


# ════════════════════════════════════════════════════════════════════════════════
#  Card flip keyboard
# ════════════════════════════════════════════════════════════════════════════════

def flip_keyboard(available_cards: list) -> InlineKeyboardMarkup:
    label_map = {"a": "🅰️ A", "b": "🅱️ B", "c": "🃏 C", "d": "🎴 D"}
    row = [primary_btn(label_map[c], data=f"flip_{c}", emoji_id=E_CARD)
           for c in available_cards]
    return InlineKeyboardMarkup([row])


# ════════════════════════════════════════════════════════════════════════════════
#  Preset keyboards
# ════════════════════════════════════════════════════════════════════════════════

def start_keyboard() -> InlineKeyboardMarkup:
    return keyboard(
        [primary_btn("🎮 Games Menu",  data="games_menu", emoji_id=E_SWORD),
         success_btn("💰 My Wallet",   data="wallet",     emoji_id=E_COIN)],
        [btn("🏆 Leaderboard",         data="leaderboard",emoji_id=E_TROPHY),
         btn("❓ Help",                data="help",       emoji_id=E_BULB)],
        [primary_btn("➕ Add to Group",
                     url="https://t.me/SHRISTI_GAME_PLAYER_bot?startgroup=true",
                     emoji_id=E_SPARK)],
    )


def games_keyboard() -> InlineKeyboardMarkup:
    return keyboard(
        [primary_btn("🃏 Card Game", data="info_card", emoji_id=E_CARD),
         danger_btn("💣 Bomb Game",  data="info_bomb", emoji_id=E_BOMB)],
        [success_btn("🔐 Hack Game", data="info_hack", emoji_id=E_LOCK)],
        [btn("🔙 Back",              data="start",     emoji_id=E_BACK)],
    )
