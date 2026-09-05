import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

print("Checking installed apps:")
for app in frappe.get_installed_apps():
    print(f"  - {app}")

# Check if setup wizard is done
is_setup_complete = frappe.db.get_single_value("System Settings", "setup_complete")
print(f"Setup complete status: {is_setup_complete}")
