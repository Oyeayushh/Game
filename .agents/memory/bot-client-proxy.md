---
name: Bot client proxy pattern
description: How the MadaraDefaultr module proxy works and why the client must be created inside asyncio.run()
---

Creating a Pyrogram `Client` at module-import time (outside any async context) causes
"Task got Future attached to a different loop" when `asyncio.run()` starts a new loop later.

**Pattern used in this project:**

1. `MadaraDefaultr.py` — proxy module with `_client = None` and `__getattr__` that delegates to `_client`
2. `main.py` — inside `async def main()`, create the `Client`, set `MadaraDefaultr._client = client`,
   THEN import plugin modules (which register handlers via `@app.on_message`)

**Why:** Plugins do `import MadaraDefaultr as app` and call `@app.on_message(...)` at module load.
The `__getattr__` proxy makes `app.on_message` resolve to `_client.on_message` at decoration time,
but only if `_client` is already set before plugins are imported.

**How to apply:** Always import plugins AFTER setting `MadaraDefaultr._client` in `main.py`.
Never move `Client(...)` construction back to module level in `MadaraDefaultr.py`.
