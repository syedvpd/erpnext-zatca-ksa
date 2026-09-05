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

# 1. Create Tax Category
tc_name = "Standard Tax"
if not frappe.db.exists("Tax Category", tc_name):
    tc = frappe.new_doc("Tax Category")
    tc.title = tc_name
    tc.custom_zatca_category = "Standard rate"
    tc.insert(ignore_permissions=True)
    print(f"Created Tax Category: {tc.name}")
else:
    tc = frappe.get_doc("Tax Category", tc_name)
    tc.custom_zatca_category = "Standard rate"
    tc.save(ignore_permissions=True)
    print(f"Updated Tax Category: {tc.name}")

# 2. Link Tax Category to Sales Taxes and Charges Template
stc_name = f"Saudi 15% VAT - {abbr}"
stc = frappe.get_doc("Sales Taxes and Charges Template", stc_name)
stc.tax_category = tc_name
stc.save(ignore_permissions=True)
print(f"Linked Tax Category {tc_name} to {stc_name}")

# 3. Update both Sales Invoices
for inv_name in ["ACC-SINV-2026-00001", "ACC-SINV-2026-00002"]:
    frappe.db.set_value("Sales Invoice", inv_name, "tax_category", tc_name)
    print(f"Set tax_category={tc_name} on {inv_name}")

frappe.db.commit()
print("Tax Category configuration committed.")
