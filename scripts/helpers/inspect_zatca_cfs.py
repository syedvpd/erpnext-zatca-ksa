import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

cfs = frappe.db.sql("""
    SELECT dt, fieldname, label, fieldtype, reqd, `options` 
    FROM `tabCustom Field` 
    WHERE fieldname LIKE '%zatca%' OR fieldname LIKE '%ksa%'
""", as_dict=True)

print(f"Found {len(cfs)} zatca/ksa custom fields:")
for c in cfs:
    print(f"  {c.dt} -> {c.fieldname} ({c.label}, {c.fieldtype}, reqd={c.reqd})")
