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

# 1. Update Company
company = frappe.get_doc("Company", company_name)
company.tax_id = "310123456700003"
company.save(ignore_permissions=True)
print(f"Updated Company: {company.name}, Tax ID: {company.tax_id}, Currency: {company.default_currency}")

# 2. Mode of Payments
modes = [
    {"name": "Cash", "type": "Cash", "code": "10"},
    {"name": "Wire Transfer", "type": "Bank", "code": "42"},
    {"name": "Credit Card", "type": "Bank", "code": "48"},
    {"name": "Cheque", "type": "Bank", "code": "20"}
]
for m in modes:
    if not frappe.db.exists("Mode of Payment", m["name"]):
        doc = frappe.new_doc("Mode of Payment")
        doc.mode_of_payment = m["name"]
        doc.type = m["type"]
        doc.custom_zatca_payment_means_code = m["code"]
        doc.insert(ignore_permissions=True)
        print(f"Created Mode of Payment: {m['name']} (ZATCA Code: {m['code']})")
    else:
        doc = frappe.get_doc("Mode of Payment", m["name"])
        doc.custom_zatca_payment_means_code = m["code"]
        doc.save(ignore_permissions=True)
        print(f"Updated Mode of Payment: {m['name']} (ZATCA Code: {m['code']})")

frappe.db.commit()
print("Payment modes configured successfully.")
