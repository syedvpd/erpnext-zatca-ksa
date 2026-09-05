import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
import inspect
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

import frappe.desk.page.setup_wizard.setup_wizard as sw
print("setup_complete args:", inspect.signature(sw.setup_complete))

# Check stages
stages = sw.get_setup_stages({})
for s in stages:
    print(f"Stage: {s.get('stage')}")
