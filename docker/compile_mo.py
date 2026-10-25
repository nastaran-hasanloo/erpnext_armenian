"""Compile apps/erpnext_armenian/erpnext_armenian/locale/hy.po to
sites/assets/locale/hy/LC_MESSAGES/erpnext_armenian.mo (same result as
`bench compile-po-to-mo --app erpnext_armenian`)."""
from pathlib import Path

from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po

bench = Path("/home/frappe/frappe-bench")
po = bench / "apps/erpnext_armenian/erpnext_armenian/locale/hy.po"
mo = bench / "sites/assets/locale/hy/LC_MESSAGES/erpnext_armenian.mo"
mo.parent.mkdir(parents=True, exist_ok=True)
with open(po, "rb") as f:
	catalog = read_po(f, locale="hy")
with open(mo, "wb") as f:
	write_mo(f, catalog)
print(f"compiled {po} -> {mo} ({len(catalog)} messages)")
