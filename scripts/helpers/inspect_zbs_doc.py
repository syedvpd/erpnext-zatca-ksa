import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()

path = "/home/frappe/frappe-bench/apps/ksa_compliance/ksa_compliance/ksa_compliance/doctype/zatca_business_settings/zatca_business_settings.py"
with open(path) as f:
    lines = f.readlines()
for l in lines[:60]:
    print(l, end="")
