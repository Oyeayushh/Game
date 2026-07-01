"""
MadaraDefaultr – Database Layer (SQLite / aiosqlite)
Powered by Madara
"""

import aiosqlite
from config import DATABASE_PATH, STARTING_COINS


# ═══════════════════════════════════════════════════════════════════════════════
#  Schema
# ═══════════════════════════════════════════════════════════════════════════════

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY,
    username    TEXT    DEFAULT '',
    first_name  TEXT    DEFAULT '',
    coins       INTEGER DEFAULT 5000,
    gems        INTEGER DEFAULT 0,
    wins        INTEGER DEFAULT 0,
    losses      INTEGER DEFAULT 0,
    games_played INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS bomb_stats (
    user_id     INTEGER PRIMARY KEY,
    wins        INTEGER DEFAULT 0,
    losses      INTEGER DEFAULT 0,
    coins_won   INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS card_stats (
    user_id     INTEGER PRIMARY KEY,
    wins        INTEGER DEFAULT 0,
    losses      INTEGER DEFAULT 0,
    coins_won   INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS hack_stats (
    user_id     INTEGER PRIMARY KEY,
    wins        INTEGER DEFAULT 0,
    losses      INTEGER DEFAULT 0,
    coins_won   INTEGER DEFAULT 0
);
"""


async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()


# ═══════════════════════════════════════════════════════════════════════════════
#  User helpers
# ═══════════════════════════════════════════════════════════════════════════════

async def get_or_create_user(user_id: int, username: str = "", first_name: str = "") -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            """INSERT OR IGNORE INTO users (user_id, username, first_name, coins)
               VALUES (?, ?, ?, ?)""",
            (user_id, username, first_name, STARTING_COINS)
        )
        await db.execute(
            "UPDATE users SET username=?, first_name=? WHERE user_id=?",
            (username, first_name, user_id)
        )
        await db.commit()
        async with db.execute("SELECT * FROM users WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
            return dict(row)


async def get_balance(user_id: int) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT coins FROM users WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0


async def update_coins(user_id: int, delta: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET coins = MAX(0, coins + ?) WHERE user_id=?",
            (delta, user_id)
        )
        await db.commit()


async def set_coins(user_id: int, amount: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("UPDATE users SET coins=? WHERE user_id=?", (amount, user_id))
        await db.commit()


async def record_win(user_id: int, table: str, coins_won: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            f"""INSERT OR IGNORE INTO {table} (user_id) VALUES (?)""", (user_id,)
        )
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
        await db.execute(
            f"""INSERT OR IGNORE INTO {table} (user_id) VALUES (?)""", (user_id,)
        )
        await db.execute(
            f"UPDATE {table} SET losses=losses+1 WHERE user_id=?", (user_id,)
        )
        await db.execute(
            "UPDATE users SET losses=losses+1, games_played=games_played+1 WHERE user_id=?",
            (user_id,)
        )
        await db.commit()


# ═══════════════════════════════════════════════════════════════════════════════
#  Leaderboard
# ═══════════════════════════════════════════════════════════════════════════════

async def get_top_users(limit: int = 10) -> list:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users ORDER BY coins DESC LIMIT ?", (limit,)
        ) as cur:
            rows = await cur.fetchall()
            return [dict(r) for r in rows]


async def get_bomb_leaderboard(limit: int = 10) -> list:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """SELECT u.first_name, u.username, b.wins, b.losses, b.coins_won
               FROM bomb_stats b JOIN users u ON b.user_id=u.user_id
               ORDER BY b.wins DESC LIMIT ?""", (limit,)
        ) as cur:
            rows = await cur.fetchall()
            return [dict(r) for r in rows]


async def get_user_rank(user_id: int) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT COUNT(*)+1 FROM users WHERE coins > (SELECT coins FROM users WHERE user_id=?)",
            (user_id,)
        ) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0
