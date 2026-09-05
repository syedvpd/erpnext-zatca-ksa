import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

company_name = "Demo Saudi Trading Company"
abbr = "DSTC"
template_name = f"Saudi 15% VAT - {abbr}"

# Update taxes_and_charges on both Sales Invoices
for inv_name in ["ACC-SINV-2026-00001", "ACC-SINV-2026-00002"]:
    frappe.db.set_value("Sales Invoice", inv_name, "taxes_and_charges", template_name)
    print(f"Set taxes_and_charges={template_name} on {inv_name}")

frappe.db.commit()
print("Updated invoice tax templates successfully.")
