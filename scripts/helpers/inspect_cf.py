import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

cf_list = frappe.get_all("Custom Field", filters={"module": "KSA Compliance"}, fields=["dt", "fieldname", "fieldtype", "reqd"])
print(f"Total KSA Compliance custom fields: {len(cf_list)}")
for cf in cf_list:
    print(f"  {cf.dt}.{cf.fieldname} ({cf.fieldtype}, reqd={cf.reqd})")
