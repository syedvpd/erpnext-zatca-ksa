import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()

import inspect
import erpnext.setup.setup_wizard.setup_wizard as esw
print("stage_fixtures:")
print(inspect.getsource(esw.stage_fixtures))
print("setup_defaults:")
print(inspect.getsource(esw.setup_defaults))
