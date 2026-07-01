---
name: Kurigram module name
description: Kurigram is a Pyrogram fork — it installs its module as `pyrogram`, not `kurigram`
---

Kurigram 2.2.23 installs to site-packages as the `pyrogram` directory.
All imports must use `from pyrogram import ...`, NOT `from kurigram import ...`.

Kurigram-specific additions (vs vanilla Pyrogram):
- `InlineKeyboardButton(..., style=ButtonStyle.PRIMARY/SUCCESS/DANGER)` — coloured buttons
- `ButtonStyle` enum lives at `from pyrogram.enums import ButtonStyle`
- `idle()` is a standalone function: `from pyrogram import idle`

**Why:** The package name on PyPI is `kurigram` but the installed Python module is `pyrogram`
because Kurigram is a drop-in fork that keeps the same module namespace.

**How to apply:** Any file that did `from kurigram import X` will get ModuleNotFoundError at runtime.
Always write `from pyrogram import X` in this project.
