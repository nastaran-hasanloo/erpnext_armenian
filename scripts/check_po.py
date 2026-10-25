#!/usr/bin/env python3
"""Sanity checks for Armenian PO files (used by CI).

Fails when a translation changes placeholders ({0}, %s, %(name)s, {{ jinja }}),
HTML tags, or when the file cannot be compiled to MO.

Usage: python scripts/check_po.py [files...]   (default: all translations/*/hy.po)
"""
from __future__ import annotations

import io
import re
import sys
from collections import Counter
from pathlib import Path

import polib
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po

ROOT = Path(__file__).resolve().parent.parent
PH = re.compile(r"\{\d*\}|\{\{.*?\}\}|\{%.*?%\}|%\(\w+\)s|%[sd]|\{[a-z_]+\}")
TAG = re.compile(r"</?([a-zA-Z][a-zA-Z0-9]*)\b")


def check(path: Path) -> int:
    errors = 0
    po = polib.pofile(str(path))
    for e in po:
        if not e.msgstr:
            continue
        if Counter(PH.findall(e.msgid)) != Counter(PH.findall(e.msgstr)):
            print(f"{path}:{e.linenum}: placeholders differ: {e.msgid[:60]!r} -> {e.msgstr[:60]!r}")
            errors += 1
        elif Counter(TAG.findall(e.msgid)) != Counter(TAG.findall(e.msgstr)):
            print(f"{path}:{e.linenum}: HTML tags differ: {e.msgid[:60]!r}")
            errors += 1
    with open(path, "rb") as f:
        write_mo(io.BytesIO(), read_po(f, locale="hy"))
    done = len(po.translated_entries())
    total = len([e for e in po if not e.obsolete])
    print(f"{path.relative_to(ROOT)}: {done}/{total} translated, {errors} problem(s)")
    return errors


def main() -> None:
    files = [Path(p).resolve() for p in sys.argv[1:]] or sorted((ROOT / "translations").glob("*/hy.po"))
    files.append(ROOT / "erpnext_armenian" / "locale" / "hy.po") if not sys.argv[1:] else None
    total = sum(check(p) for p in files if p.exists())
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
