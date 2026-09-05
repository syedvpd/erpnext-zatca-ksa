import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()

siaf = frappe.get_all("Sales Invoice Additional Fields", fields=["name", "sales_invoice", "integration_status", "invoice_counter", "invoice_hash"])
print("Sales Invoice Additional Fields count:", len(siaf))
for s in siaf:
    print(s)
