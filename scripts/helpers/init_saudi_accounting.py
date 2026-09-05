import os
import sys

os.makedirs("/home/frappe/logs", exist_ok=True)
os.makedirs("/home/frappe/frappe-bench/logs", exist_ok=True)

import frappe
from frappe.utils import today, nowdate, flt

frappe.init(site="frontend", sites_path="/home/frappe/frappe-bench/sites")
frappe.connect()
frappe.set_user("Administrator")

print("Connected to frontend as Administrator")

# 1. Complete Setup Wizard if not completed
setup_complete = frappe.db.get_single_value("System Settings", "setup_complete")
if not setup_complete:
    print("Running setup_wizard.setup_complete...")
    from erpnext.setup.setup_wizard.setup_wizard import setup_complete as erpnext_setup_complete
    erpnext_setup_complete({
        "language": "en",
        "country": "Saudi Arabia",
        "timezone": "Asia/Riyadh",
        "currency": "SAR",
        "full_name": "Administrator",
        "email": "admin@example.com",
        "company_name": "Demo Saudi Trading Company",
        "company_abbr": "DSTC",
        "chart_of_accounts": "Standard",
        "fy_start_date": "2026-01-01",
        "fy_end_date": "2026-12-31"
    })
    frappe.db.commit()
    print("Setup wizard completed!")

company_name = "Demo Saudi Trading Company"
abbr = "DSTC"

if not frappe.db.exists("Company", company_name):
    print("Creating Company:", company_name)
    company = frappe.get_doc({
        "doctype": "Company",
        "company_name": company_name,
        "abbr": abbr,
        "default_currency": "SAR",
        "country": "Saudi Arabia",
        "chart_of_accounts": "Standard"
    }).insert(ignore_permissions=True)
    frappe.db.commit()
else:
    company = frappe.get_doc("Company", company_name)

print("Company ready:", company.name, "| Country:", company.country, "| Currency:", company.default_currency)
