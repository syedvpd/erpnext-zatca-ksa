import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

import frappe.desk.page.setup_wizard.setup_wizard as fsw

args = {
    "language": "English",
    "country": "Saudi Arabia",
    "timezone": "Asia/Riyadh",
    "currency": "SAR",
    "full_name": "Administrator",
    "email": "admin@example.com",
    "company_name": "Demo Saudi Trading Company",
    "company_abbr": "DSTC",
    "chart_of_accounts": "Standard",
    "fy_start_date": "2026-01-01",
    "fy_end_date": "2026-12-31",
    "domain": "Distribution"
}

print("Running setup_complete...")
res = fsw.setup_complete(args)
frappe.db.commit()
print("Result:", res)
print("Setup complete:", frappe.is_setup_complete())
print("Companies:", frappe.get_all("Company", fields=["name", "country", "default_currency"]))
