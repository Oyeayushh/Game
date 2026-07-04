"""
MadaraDefaultr – Database Layer (SQLite / aiosqlite)
Powered by Madara
"""

import time
import aiosqlite
from config import DATABASE_PATH, STARTING_COINS

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id      INTEGER PRIMARY KEY,
    username     TEXT    DEFAULT '',
    first_name   TEXT    DEFAULT '',
    coins        INTEGER DEFAULT 5000,
    gems         INTEGER DEFAULT 0,
    wins         INTEGER DEFAULT 0,
    losses       INTEGER DEFAULT 0,
    games_played INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS bomb_stats (
    user_id   INTEGER PRIMARY KEY,
    wins      INTEGER DEFAULT 0,
    losses    INTEGER DEFAULT 0,
    coins_won INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS card_stats (
    user_id   INTEGER PRIMARY KEY,
    wins      INTEGER DEFAULT 0,
    losses    INTEGER DEFAULT 0,
    coins_won INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS hack_stats (
    user_id   INTEGER PRIMARY KEY,
    wins      INTEGER DEFAULT 0,
    losses    INTEGER DEFAULT 0,
    coins_won INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS relationships (
    user_id    INTEGER PRIMARY KEY,
    partner_id INTEGER DEFAULT 0,
    status     TEXT    DEFAULT 'single'
);
CREATE TABLE IF NOT EXISTS inventory (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER,
    item      TEXT,
    bought_at REAL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS combat (
    user_id          INTEGER PRIMARY KEY,
    kills            INTEGER DEFAULT 0,
    deaths           INTEGER DEFAULT 0,
    protection_until REAL    DEFAULT 0,
    last_kill        REAL    DEFAULT 0
);
CREATE TABLE IF NOT EXISTS daily (
    user_id    INTEGER PRIMARY KEY,
    last_daily REAL    DEFAULT 0,
    streak     INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS group_claims (
    user_id    INTEGER,
    chat_id    INTEGER,
    last_claim REAL DEFAULT 0,
    PRIMARY KEY (user_id, chat_id)
);
CREATE TABLE IF NOT EXISTS welcome_settings (
    chat_id INTEGER PRIMARY KEY,
    enabled INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS chats (
    chat_id  INTEGER PRIMARY KEY,
    title    TEXT DEFAULT '',
    added_at REAL DEFAULT 0
);
"""


async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()


# ─── Users ───────────────────────────────────────────────────────────────────

async def get_or_create_user(user_id: int, username: str = "", first_name: str = "") -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name, coins) VALUES (?,?,?,?)",
            (user_id, username, first_name, STARTING_COINS)
        )
        await db.execute(
            "UPDATE users SET username=?, first_name=? WHERE user_id=?",
            (username, first_name, user_id)
        )
        await db.commit()
        async with db.execute("SELECT * FROM users WHERE user_id=?", (user_id,)) as cur:
            return dict(await cur.fetchone())


async def get_balance(user_id: int) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT coins FROM users WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0


async def update_coins(user_id: int, delta: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET coins=MAX(0, coins+?) WHERE user_id=?", (delta, user_id)
        )
        await db.commit()


async def set_coins(user_id: int, amount: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("UPDATE users SET coins=? WHERE user_id=?", (amount, user_id))
        await db.commit()


async def record_win(user_id: int, table: str, coins_won: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(f"INSERT OR IGNORE INTO {table} (user_id) VALUES (?)", (user_id,))
        await db.execute(
            f"UPDATE {table} SET wins=wins+1, coins_won=coins_won+? WHERE user_id=?",
            (coins_won, user_id)
        )
        await db.execute(
            "UPDATE users SET wins=wins+1, games_played=games_played+1 WHERE user_id=?",
            (user_id,)
        )
        await db.commit()


async def record_loss(user_id: int, table: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(f"INSERT OR IGNORE INTO {table} (user_id) VALUES (?)", (user_id,))
        await db.execute(f"UPDATE {table} SET losses=losses+1 WHERE user_id=?", (user_id,))
        await db.execute(
            "UPDATE users SET losses=losses+1, games_played=games_played+1 WHERE user_id=?",
            (user_id,)
        )
        await db.commit()


async def get_top_users(limit: int = 10) -> list:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users ORDER BY coins DESC LIMIT ?", (limit,)) as cur:
            return [dict(r) for r in await cur.fetchall()]


async def get_bomb_leaderboard(limit: int = 10) -> list:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """SELECT u.first_name,u.username,b.wins,b.losses,b.coins_won
               FROM bomb_stats b JOIN users u ON b.user_id=u.user_id
               ORDER BY b.wins DESC LIMIT ?""", (limit,)
        ) as cur:
            return [dict(r) for r in await cur.fetchall()]


async def get_user_rank(user_id: int) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT COUNT(*)+1 FROM users WHERE coins>(SELECT coins FROM users WHERE user_id=?)",
            (user_id,)
        ) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0


# ─── Relationships ────────────────────────────────────────────────────────────

async def get_relationship(user_id: int) -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "INSERT OR IGNORE INTO relationships (user_id) VALUES (?)", (user_id,)
        )
        await db.commit()
        async with db.execute(
            "SELECT * FROM relationships WHERE user_id=?", (user_id,)
        ) as cur:
            return dict(await cur.fetchone())


async def set_relationship(user_id: int, partner_id: int, status: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO relationships (user_id, partner_id, status) VALUES (?,?,?)",
            (user_id, partner_id, status)
        )
        await db.commit()


# ─── Inventory ────────────────────────────────────────────────────────────────

async def get_inventory(user_id: int) -> list:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT item FROM inventory WHERE user_id=?", (user_id,)
        ) as cur:
            return [row[0] for row in await cur.fetchall()]


async def has_item(user_id: int, item: str) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT 1 FROM inventory WHERE user_id=? AND item=?", (user_id, item)
        ) as cur:
            return await cur.fetchone() is not None


async def add_item(user_id: int, item: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO inventory (user_id, item, bought_at) VALUES (?,?,?)",
            (user_id, item, time.time())
        )
        await db.commit()


# ─── Combat ───────────────────────────────────────────────────────────────────

async def get_combat(user_id: int) -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute("INSERT OR IGNORE INTO combat (user_id) VALUES (?)", (user_id,))
        await db.commit()
        async with db.execute("SELECT * FROM combat WHERE user_id=?", (user_id,)) as cur:
            return dict(await cur.fetchone())


async def update_combat(user_id: int, **kwargs):
    if not kwargs:
        return
    cols = ", ".join(f"{k}=?" for k in kwargs)
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            f"UPDATE combat SET {cols} WHERE user_id=?",
            (*kwargs.values(), user_id)
        )
        await db.commit()


async def is_protected(user_id: int) -> bool:
    c = await get_combat(user_id)
    return c["protection_until"] > time.time()


# ─── Daily / Claim ────────────────────────────────────────────────────────────

async def get_daily(user_id: int) -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute("INSERT OR IGNORE INTO daily (user_id) VALUES (?)", (user_id,))
        await db.commit()
        async with db.execute("SELECT * FROM daily WHERE user_id=?", (user_id,)) as cur:
            return dict(await cur.fetchone())


async def set_daily(user_id: int, streak: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO daily (user_id, last_daily, streak) VALUES (?,?,?)",
            (user_id, time.time(), streak)
        )
        await db.commit()


async def get_group_claim(user_id: int, chat_id: int) -> float:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT last_claim FROM group_claims WHERE user_id=? AND chat_id=?",
            (user_id, chat_id)
        ) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0.0


async def set_group_claim(user_id: int, chat_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO group_claims (user_id, chat_id, last_claim) VALUES (?,?,?)",
            (user_id, chat_id, time.time())
        )
        await db.commit()


# ─── Welcome ─────────────────────────────────────────────────────────────────

async def get_welcome(chat_id: int) -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "INSERT OR IGNORE INTO welcome_settings (chat_id) VALUES (?)", (chat_id,)
        )
        await db.commit()
        async with db.execute(
            "SELECT * FROM welcome_settings WHERE chat_id=?", (chat_id,)
        ) as cur:
            return dict(await cur.fetchone())


async def set_welcome(chat_id: int, enabled: bool):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO welcome_settings (chat_id, enabled) VALUES (?,?)",
            (chat_id, int(enabled))
        )
        await db.commit()


# ─── Chats (for logging / broadcast) ──────────────────────────────────────────

async def add_chat(chat_id: int, title: str = ""):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO chats (chat_id, title, added_at) VALUES (?,?,?) "
            "ON CONFLICT(chat_id) DO UPDATE SET title=excluded.title",
            (chat_id, title, time.time())
        )
        await db.commit()


async def remove_chat(chat_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM chats WHERE chat_id=?", (chat_id,))
        await db.commit()


async def get_all_chats() -> list:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT chat_id FROM chats") as cur:
            return [row[0] for row in await cur.fetchall()]


async def get_all_users() -> list:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT user_id FROM users") as cur:
            return [row[0] for row in await cur.fetchall()]


async def get_chat_count() -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM chats") as cur:
            row = await cur.fetchone()
            return row[0] if row else 0


async def get_user_count() -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cur:
            row = await cur.fetchone()
            return row[0] if row else 0


async def user_exists(user_id: int) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT 1 FROM users WHERE user_id=?", (user_id,)) as cur:
            return (await cur.fetchone()) is not None
