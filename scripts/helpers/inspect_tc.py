import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()

tc_list = frappe.get_all("Tax Category", fields=["name", "title"])
print("Existing Tax Categories:", tc_list)

meta = frappe.get_meta("Tax Category")
for f in meta.fields:
    if "zatca" in f.fieldname or "category" in f.fieldname:
        print(f"Field: {f.fieldname} ({f.fieldtype}, options: {f.options})")
