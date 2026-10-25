import frappe

LANGUAGE = {
	"language_code": "hy",
	"language_name": "Հայերեն",
	"enabled": 1,
	"date_format": "dd.mm.yyyy",
	"time_format": "HH:mm",
	"number_format": "# ###,##",
	"first_day_of_the_week": "Monday",
}


def ensure_language():
	"""Create or enable the `hy` Language record. Existing format choices are kept."""
	if frappe.db.exists("Language", "hy"):
		doc = frappe.get_doc("Language", "hy")
		doc.enabled = 1
		doc.language_name = doc.language_name or LANGUAGE["language_name"]
		for key in ("date_format", "time_format", "number_format", "first_day_of_the_week"):
			if not doc.get(key):
				doc.set(key, LANGUAGE[key])
		doc.save(ignore_permissions=True)
	else:
		frappe.get_doc({"doctype": "Language", **LANGUAGE}).insert(ignore_permissions=True)


def before_install():
	"""Stop early with a clear message if this branch doesn't match the Frappe version."""
	major = int(frappe.__version__.split(".")[0])
	if major != 16:
		frappe.throw(
			f"This is the version-16 branch, but your Frappe is v{major}. "
			"Remove the app with `bench remove-app erpnext_armenian` and get the branch "
			"that matches your version (see the README)."
		)


def after_install():
	ensure_language()
	frappe.clear_cache()
	print(
		"Armenian is ready. Switch to it in My Settings > Language > Հայերեն, "
		"or for everyone in System Settings."
	)


def after_migrate():
	ensure_language()
