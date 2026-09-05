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

# 1. Ensure Tax Category
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

# 2. Create Sales Taxes and Charges Template
stc = frappe.new_doc("Sales Taxes and Charges Template")
stc.title = f"Saudi 15% VAT - {abbr}"
stc.company = company_name
stc.tax_category = tc_name
stc.is_default = 1
stc.append("taxes", {
    "charge_type": "On Net Total",
    "account_head": f"VAT 15% - {abbr}",
    "description": "VAT 15%",
    "rate": 15.0
})
stc.insert(ignore_permissions=True)
print(f"Created Sales Taxes and Charges Template: {stc.name}")

# 3. Update Sales Invoices
for inv_name in ["ACC-SINV-2026-00001", "ACC-SINV-2026-00002"]:
    frappe.db.set_value("Sales Invoice", inv_name, "taxes_and_charges", stc.name)
    frappe.db.set_value("Sales Invoice", inv_name, "tax_category", tc_name)
    print(f"Linked {stc.name} and {tc_name} to {inv_name}")

frappe.db.commit()
print("Committed successfully!")
