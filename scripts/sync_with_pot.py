#!/usr/bin/env python3
"""Sync translations/<app>/hy.po with a newer upstream main.pot.

Keeps every existing translation, adds new strings (empty), drops strings that
were removed upstream. Same idea as `bench update-po-files`.

Usage:
  python scripts/sync_with_pot.py erpnext /path/to/apps/erpnext/erpnext/locale/main.pot
"""
from __future__ import annotations

import sys
from pathlib import Path

import polib

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    app, pot_path = sys.argv[1], sys.argv[2]
    po_path = ROOT / "translations" / app / "hy.po"
    old = {(e.msgctxt, e.msgid): e.msgstr for e in polib.pofile(str(po_path))} if po_path.exists() else {}
    pot = polib.pofile(pot_path)
    po = polib.POFile(wrapwidth=0)
    po.metadata = polib.pofile(str(po_path)).metadata if po_path.exists() else {"Language": "hy"}
    new = 0
    for e in pot:
        t = old.get((e.msgctxt, e.msgid), "")
        new += not t
        po.append(polib.POEntry(msgid=e.msgid, msgctxt=e.msgctxt, msgstr=t, occurrences=e.occurrences, comment=e.comment, flags=e.flags))
    po_path.parent.mkdir(parents=True, exist_ok=True)
    po.save(str(po_path))
    print(f"{app}: {len(po)} strings, {new} untranslated")


if __name__ == "__main__":
    main()
