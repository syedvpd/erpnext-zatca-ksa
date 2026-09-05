import os
for p in [
    "/home/frappe/logs",
    "/home/frappe/frappe-bench/logs",
    "/home/frappe/frappe-bench/frontend/logs",
    "/home/frappe/frappe-bench/sites/frontend/logs",
    "/home/frappe/frappe-bench/sites/frontend/zatca-files"
]:
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

initial_pih = base64.b64encode(hashlib.sha256(b"0").digest()).decode("utf-8")

# B2B Invoice
b2b_inv = frappe.get_doc("Sales Invoice", "ACC-SINV-2026-00001")
siaf_b2b = siaf_mod.SalesInvoiceAdditionalFields.create_for_invoice(b2b_inv.name, b2b_inv.doctype)
siaf_b2b.uuid = str(uuid.uuid4())
siaf_b2b.invoice_counter = 1
siaf_b2b.previous_invoice_hash = initial_pih

einvoice_b2b = Einvoice(sales_invoice_additional_fields_doc=siaf_b2b, invoice_type="Standard")
xml_b2b = generate_xml_file(einvoice_b2b.result)
b2b_hash_hex = hashlib.sha256(xml_b2b.encode("utf-8")).hexdigest()
b2b_hash_b64 = base64.b64encode(hashlib.sha256(xml_b2b.encode("utf-8")).digest()).decode("utf-8")

xml_path_b2b = "/home/frappe/frappe-bench/sites/frontend/zatca-files/ACC-SINV-2026-00001.xml"
with open(xml_path_b2b, "w", encoding="utf-8") as f:
    f.write(xml_b2b)

# B2C Invoice
b2c_inv = frappe.get_doc("Sales Invoice", "ACC-SINV-2026-00002")
siaf_b2c = siaf_mod.SalesInvoiceAdditionalFields.create_for_invoice(b2c_inv.name, b2c_inv.doctype)
siaf_b2c.uuid = str(uuid.uuid4())
siaf_b2c.invoice_counter = 2
siaf_b2c.previous_invoice_hash = b2b_hash_b64

einvoice_b2c = Einvoice(sales_invoice_additional_fields_doc=siaf_b2c, invoice_type="Simplified")
xml_b2c = generate_xml_file(einvoice_b2c.result)
b2c_hash_hex = hashlib.sha256(xml_b2c.encode("utf-8")).hexdigest()
b2c_hash_b64 = base64.b64encode(hashlib.sha256(xml_b2c.encode("utf-8")).digest()).decode("utf-8")

xml_path_b2c = "/home/frappe/frappe-bench/sites/frontend/zatca-files/ACC-SINV-2026-00002.xml"
with open(xml_path_b2c, "w", encoding="utf-8") as f:
    f.write(xml_b2c)

print("SUCCESS: Phase 2 XMLs generated and saved!")
print(f"B2B File: {xml_path_b2b} ({len(xml_b2b)} bytes, Hash: {b2b_hash_b64})")
print(f"B2C File: {xml_path_b2c} ({len(xml_b2c)} bytes, Hash: {b2c_hash_b64})")
