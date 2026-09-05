import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

accs = frappe.get_all("Account", filters={"company": "Demo Saudi Trading Company"}, fields=["name", "parent_account", "account_type", "is_group"])
for a in accs:
    print(f"Account: {a.name} (type: {a.account_type}, group: {a.is_group}, parent: {a.parent_account})")
