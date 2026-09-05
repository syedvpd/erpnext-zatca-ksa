import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()

meta = frappe.get_meta("ZATCA Phase 1 Business Settings")
for f in meta.fields:
    print(f"Field: {f.fieldname} ({f.fieldtype}, reqd={f.reqd})")
