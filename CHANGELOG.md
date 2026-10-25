# Changelog

## 16.0.0 (2026-10-25)

First release, for version-16.

- Translated basically all of the v16 UI in Frappe, ERPNext and Frappe HR. A few codes and brand names are left as they are on purpose.
- Installing the app adds the `hy` language with Armenian date and number formats, and Monday as the first day of the week.
- Added translations for the setup wizard survey options, the home dashboard text, the Frappe HR getting-started steps and a couple of sidebar labels. None of these are in the upstream POT files.
- Fixed `ALL` (Albanian lek), `JAN` (barcode type) and `HERE` (map provider). They were getting translated as normal words.
- One-click test setup in `docker/` for Windows, plus a script for Linux and macOS. If you already have a test site, it gets the app installed the next time you start it.
- CI checks placeholders, HTML tags and that the MO file compiles.
