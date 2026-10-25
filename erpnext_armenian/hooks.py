app_name = "erpnext_armenian"
app_title = "ERPNext Armenian"
app_publisher = "ERPNext Armenian contributors"
app_description = "Armenian (hy) translation for Frappe, ERPNext and Frappe HR"
app_email = "283343093+nastaran-hasanloo@users.noreply.github.com"
app_license = "gpl-3.0"

# Works with Frappe alone; ERPNext and HRMS strings are translated when those apps are installed.
required_apps = ["frappe"]

# Register the Armenian language (Հայերեն) with Armenian formats.
before_install = "erpnext_armenian.install.before_install"
after_install = "erpnext_armenian.install.after_install"
after_migrate = "erpnext_armenian.install.after_migrate"
