"""
One-shot: move every file currently in Messages_Between_Departments/{Inbox,Outbox}
into Messages_Between_Departments/_archive_20260722/ so nothing is deleted, but
the directories the daily cycle scans go to zero. Also archives the top-level
Messages/ folder if it exists.

Companion change: MessageHandler.write_message is patched (in
trading_department.py and operations_manager.py via ArchivedMessageHandler
sentinel) to become a no-op so no new files accumulate. Nothing reads these
messages — they were pure side effects.

Run once. Safe to re-run — it just moves whatever's currently in the live dirs.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
MSG_ROOT = ROOT / "Messages_Between_Departments"
ARCHIVE = MSG_ROOT / "_archive_20260722"


def move_tree(src: Path, dst_root: Path) -> int:
    if not src.exists():
        return 0
    moved = 0
    for path in src.rglob("*"):
        if path.is_file():
            rel = path.relative_to(src)
            dest = dst_root / src.name / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(dest))
            moved += 1
    return moved


def main() -> int:
    if not MSG_ROOT.exists():
        print(f"No {MSG_ROOT} — nothing to do")
        return 0

    ARCHIVE.mkdir(parents=True, exist_ok=True)
    print(f"Archiving to {ARCHIVE}")

    total = 0
    for sub in ("Inbox", "Outbox", "Executive"):
        p = MSG_ROOT / sub
        if p.exists():
            n = move_tree(p, ARCHIVE)
            print(f"  {sub}: moved {n} files")
            total += n

    # Also handle top-level Messages/ if present
    alt = ROOT / "Messages"
    if alt.exists():
        n = move_tree(alt, ARCHIVE)
        print(f"  Messages/: moved {n} files")
        total += n

    print(f"Total moved: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
