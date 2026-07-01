"""
MadaraDefaultr – Bot client proxy module
Plugins import this as: `import MadaraDefaultr as app`
Then use:  @app.on_message(...)  /  await app.send_message(...)
The actual client is injected by main.py before plugins are imported.
Powered by Madara
"""

import sys

# Injected by main.py after the event loop is running
_client = None


def __getattr__(name: str):
    """Proxy every attribute lookup to the underlying Pyrogram Client."""
    if _client is None:
        raise RuntimeError(
            "MadaraDefaultr client is not initialised yet. "
            "Ensure main.py sets MadaraDefaultr._client before importing plugins."
        )
    return getattr(_client, name)
