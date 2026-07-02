"""
MadaraDefaultr – Small Caps Font Utility
Powered by Madara
"""

# Small caps Unicode mapping (a–z, A–Z)
_SC = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘQʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘQʀsᴛᴜᴠᴡxʏᴢ"
)

def sc(text: str) -> str:
    """Convert text to small-caps Unicode font style."""
    return text.translate(_SC)
