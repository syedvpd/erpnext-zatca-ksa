import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()

import inspect
from erpnext.setup.setup_wizard.operations import install_fixtures as fixtures
print("setup_defaults:")
print(inspect.getsource(fixtures.setup_defaults))
