import os
import sys

# Ensure all possible log directories exist
for p in [
    "/home/frappe/logs",
    "/home/frappe/frappe-bench/logs",
    "/home/frappe/frappe-bench/frontend/logs",
    "/home/frappe/frappe-bench/sites/frontend/logs",
    "/home/frappe/frappe-bench/sites/logs"
]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

print("SUCCESS: Connected to frontend as Administrator!")
print("Installed apps:", frappe.get_installed_apps())
print("Setup complete flag:", frappe.db.get_single_value("System Settings", "setup_complete"))
