import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

cg = frappe.get_all("Customer Group", fields=["name", "is_group"])
sg = frappe.get_all("Supplier Group", fields=["name", "is_group"])
ig = frappe.get_all("Item Group", fields=["name", "is_group"])

print("Customer Groups:", cg)
print("Supplier Groups:", sg)
print("Item Groups:", ig)
