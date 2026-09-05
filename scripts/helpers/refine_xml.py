import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
import uuid
import hashlib
import base64
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

import ksa_compliance.ksa_compliance.doctype.sales_invoice_additional_fields.sales_invoice_additional_fields as siaf_mod
from ksa_compliance.output_models.e_invoice_output_model import Einvoice
from ksa_compliance.generate_xml import generate_xml_file

company_name = "Demo Saudi Trading Company"

# Update ZATCA Business Settings with full address details
zbs_name = frappe.db.get_value("ZATCA Business Settings", {"company": company_name}, "name")
zbs = frappe.get_doc("ZATCA Business Settings", zbs_name)
zbs.building_number = "1234"
zbs.street = "King Fahd Road"
zbs.district = "Al Olaya"
zbs.city = "Riyadh"
zbs.postal_code = "12211"
zbs.save(ignore_permissions=True)

# Also update Address
addr_name = frappe.db.get_value("Address", {"address_title": "Demo Saudi Trading Company - HQ"}, "name")
if addr_name:
    addr = frappe.get_doc("Address", addr_name)
    addr.custom_building_number = "1234" if hasattr(addr, "custom_building_number") else None
    addr.save(ignore_permissions=True)

# Update B2B SIAF
siaf_b2b_name = frappe.db.get_value("Sales Invoice Additional Fields", {"sales_invoice": "ACC-SINV-2026-00001"}, "name")
siaf_b2b = frappe.get_doc("Sales Invoice Additional Fields", siaf_b2b_name)
if not siaf_b2b.uuid:
    siaf_b2b.uuid = str(uuid.uuid4())
siaf_b2b.save(ignore_permissions=True)

einvoice_b2b = Einvoice(sales_invoice_additional_fields_doc=siaf_b2b, invoice_type="Standard")
xml_b2b = generate_xml_file(einvoice_b2b.result)

with open("/home/frappe/frappe-bench/sites/frontend/zatca-files/ACC-SINV-2026-00001.xml", "w", encoding="utf-8") as f:
    f.write(xml_b2b)

print("Updated B2B XML with UUID & building details:")
with open("/home/frappe/frappe-bench/sites/frontend/zatca-files/ACC-SINV-2026-00001.xml") as f:
    for i in range(25):
        print(f.readline(), end="")
