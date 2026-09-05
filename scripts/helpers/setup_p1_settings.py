import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

company_name = "Demo Saudi Trading Company"

# 1. Create Address
addr_title = "Demo Saudi Trading Company - HQ"
if not frappe.db.exists("Address", {"address_title": addr_title}):
    addr = frappe.new_doc("Address")
    addr.address_title = addr_title
    addr.address_type = "Billing"
    addr.address_line1 = "King Fahd Road, Al Olaya"
    addr.city = "Riyadh"
    addr.country = "Saudi Arabia"
    addr.postal_code = "12211"
    addr.append("links", {
        "link_doctype": "Company",
        "link_name": company_name
    })
    addr.insert(ignore_permissions=True)
    print(f"Created Address: {addr.name}")
    addr_name = addr.name
else:
    addr_name = frappe.db.get_value("Address", {"address_title": addr_title}, "name")
    print(f"Address exists: {addr_name}")

# 2. Create ZATCA Phase 1 Business Settings
p1_name = frappe.db.get_value("ZATCA Phase 1 Business Settings", {"company": company_name}, "name")
if not p1_name:
    p1 = frappe.new_doc("ZATCA Phase 1 Business Settings")
    p1.company = company_name
    p1.vat_registration_number = "310123456700003"
    p1.address = addr_name
    p1.type_of_transaction = "Both"
    p1.status = "Active"
    p1.insert(ignore_permissions=True)
    print(f"Created ZATCA Phase 1 Business Settings: {p1.name}")
else:
    p1 = frappe.get_doc("ZATCA Phase 1 Business Settings", p1_name)
    p1.vat_registration_number = "310123456700003"
    p1.address = addr_name
    p1.type_of_transaction = "Both"
    p1.status = "Active"
    p1.save(ignore_permissions=True)
    print(f"Updated ZATCA Phase 1 Business Settings: {p1.name}")

frappe.db.commit()
print("ZATCA Phase 1 Settings configured and active!")
