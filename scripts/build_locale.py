#!/usr/bin/env python3
"""Merge translations/*/hy.po into the app catalog erpnext_armenian/locale/hy.po.

Frappe loads `<app>/locale/<lang>.po` of every installed app (compiled to .mo by
`bench build` / `bench compile-po-to-mo`) and merges them into one dictionary, so a
single catalog shipped by this app translates Frappe, ERPNext and HRMS.

Order of precedence (first non-empty translation wins):
  translations/overrides/hy.po  -> fixes and strings that are not in upstream POT files
  translations/frappe/hy.po
  translations/erpnext/hy.po
  translations/hrms/hy.po

Usage: python scripts/build_locale.py
"""
from __future__ import annotations

import datetime
from pathlib import Path

import polib

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ["overrides", "frappe", "erpnext", "hrms"]
OUT = ROOT / "erpnext_armenian" / "locale" / "hy.po"


def main() -> None:
    merged: dict[tuple[str | None, str], polib.POEntry] = {}
    for src in SOURCES:
        path = ROOT / "translations" / src / "hy.po"
        if not path.exists():
            continue
        for e in polib.pofile(str(path)):
            if e.obsolete or not e.msgstr.strip():
                continue
            key = (e.msgctxt, e.msgid)
            if key not in merged:
                merged[key] = polib.POEntry(msgid=e.msgid, msgctxt=e.msgctxt, msgstr=e.msgstr)

    po = polib.POFile(wrapwidth=0)
    po.metadata = {
        "Project-Id-Version": "erpnext_armenian version-16",
        "Language": "hy",
        "Language-Team": "Armenian",
        "MIME-Version": "1.0",
        "Content-Type": "text/plain; charset=UTF-8",
        "Content-Transfer-Encoding": "8bit",
        "Plural-Forms": "nplurals=2; plural=(n != 1);",
        "PO-Revision-Date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M+0000"),
        "X-Generator": "erpnext_armenian scripts/build_locale.py",
    }
    for key in sorted(merged, key=lambda k: (k[1], k[0] or "")):
        po.append(merged[key])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    po.save(str(OUT))
    print(f"wrote {OUT.relative_to(ROOT)}: {len(po)} messages")


if __name__ == "__main__":
    main()
