import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()

bins = frappe.get_all("Bin", fields=["item_code", "warehouse", "actual_qty"])
for b in bins:
    print(f"Item: {b.item_code} in {b.warehouse} -> Qty: {b.actual_qty}")
