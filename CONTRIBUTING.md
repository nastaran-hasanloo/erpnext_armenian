# Helping out

Thanks for taking a look! Any fix helps, even a single word.

## The quickest way: fix it right on GitHub

No tools needed.

1. Open the file for the app the text belongs to, for example `translations/erpnext/hy.po`.
2. Click the pencil icon, then press Ctrl+F and search for the English text.
3. Change the Armenian line right under it (`msgstr "..."`).
4. Click "Commit changes" and GitHub will make a pull request for you.

We'll rebuild the final file when we merge it.

## Fixing a translation on your computer

Open the right file in [Poedit](https://poedit.net/) or any text editor:

- `translations/frappe/hy.po`, `translations/erpnext/hy.po` or `translations/hrms/hy.po` for normal strings
- `translations/overrides/hy.po` for strings that aren't in the upstream POT files, or when you want to override an upstream translation

A few things that are easy to break:

- Leave placeholders alone: `{0}`, `%s`, `%(name)s`, `{{ ... }}`
- Same for HTML tags and brand names
- For accounting and ERP terms, try to stick to `translations/glossary-hy.json` so the same thing isn't called three different names. If you think a glossary term is wrong, just say so in your PR.

Then rebuild and run the checks:

```bash
pip install polib babel
python scripts/build_locale.py
python scripts/check_po.py
```

Commit the file you changed together with `erpnext_armenian/locale/hy.po` and open a PR against `version-16`.

Not comfortable with git? Open an issue with the screen, the current text and what it should say. That's totally fine too.

## When upstream ships a new release

```bash
python scripts/sync_with_pot.py frappe  ../frappe-bench/apps/frappe/frappe/locale/main.pot
python scripts/sync_with_pot.py erpnext ../frappe-bench/apps/erpnext/erpnext/locale/main.pot
python scripts/sync_with_pot.py hrms    ../frappe-bench/apps/hrms/hrms/locale/main.pot
```

New strings come in empty. Translate them and rebuild.

## Style we're going for

- Eastern Armenian, reformed spelling
- Buttons in the infinitive: Պահպանել, Ջնջել, Ստեղծել
- Polite requests start with «Խնդրում ենք ...»
- Short labels. Screens get crowded fast.

The per-app files also go to the [Frappe project on Crowdin](https://crowdin.com/project/frappe), so the good stuff ends up in the official releases too.
