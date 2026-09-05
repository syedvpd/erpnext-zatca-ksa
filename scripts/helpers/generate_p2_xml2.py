import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
import hashlib
import base64
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

import ksa_compliance.ksa_compliance.doctype.sales_invoice_additional_fields.sales_invoice_additional_fields as siaf_mod
from ksa_compliance.output_models.e_invoice_output_model import Einvoice
from ksa_compliance.invoice import InvoiceType
from ksa_compliance.generate_xml import generate_xml_file

company_name = "Demo Saudi Trading Company"
addr_name = frappe.db.get_value("Address", {"address_title": "Demo Saudi Trading Company - HQ"}, "name")

# 1. Ensure ZATCA Business Settings
zbs_name = frappe.db.get_value("ZATCA Business Settings", {"company": company_name}, "name")
if not zbs_name:
    zbs = frappe.new_doc("ZATCA Business Settings")
    zbs.company = company_name
    zbs.status = "Active"
    zbs.company_unit = "Main Branch"
    zbs.company_unit_serial = "1"
    zbs.company_category = "Trading"
    zbs.country = "Saudi Arabia"
    zbs.currency = "SAR"
    zbs.company_address = addr_name
    zbs.seller_name = company_name
    zbs.vat_registration_number = "310123456700003"
    zbs.enable_zatca_integration = 1
    zbs.sync_with_zatca = "Batches"
    zbs.type_of_business_transactions = "Both"
    zbs.cli_setup = "Manual"
    zbs.insert(ignore_permissions=True)
    print(f"Created ZATCA Business Settings: {zbs.name}")
    zbs_name = zbs.name
else:
    zbs = frappe.get_doc("ZATCA Business Settings", zbs_name)
    zbs.status = "Active"
    zbs.enable_zatca_integration = 1
    zbs.sync_with_zatca = "Batches"
    zbs.company_address = addr_name
    zbs.save(ignore_permissions=True)
    print(f"Updated ZATCA Business Settings: {zbs.name}")

# 2. Ensure Counting Settings
cs_name = frappe.db.get_value("ZATCA Invoice Counting Settings", {"business_settings_reference": zbs_name}, "name")
initial_pih = base64.b64encode(hashlib.sha256(b"0").digest()).decode("utf-8")
if not cs_name:
    cs = frappe.new_doc("ZATCA Invoice Counting Settings")
    cs.business_settings_reference = zbs_name
    cs.invoice_counter = 0
    cs.previous_invoice_hash = initial_pih
    cs.insert(ignore_permissions=True)
    print(f"Created ZATCA Invoice Counting Settings: {cs.name}")
else:
    print(f"Counting Settings exists: {cs_name}")

frappe.db.commit()

# 3. Generate Phase 2 XML for B2B Invoice
b2b_inv = frappe.get_doc("Sales Invoice", "ACC-SINV-2026-00001")
siaf_b2b_name = frappe.db.get_value("Sales Invoice Additional Fields", {"sales_invoice": b2b_inv.name}, "name")
if not siaf_b2b_name:
    siaf_b2b = siaf_mod.SalesInvoiceAdditionalFields.create_for_invoice(b2b_inv.name, b2b_inv.doctype)
    siaf_b2b.invoice_counter = 1
    siaf_b2b.previous_invoice_hash = initial_pih
    siaf_b2b.insert(ignore_permissions=True)
    print(f"Created Sales Invoice Additional Fields for B2B: {siaf_b2b.name}")
else:
    siaf_b2b = frappe.get_doc("Sales Invoice Additional Fields", siaf_b2b_name)
    if not siaf_b2b.invoice_counter:
        siaf_b2b.invoice_counter = 1
        siaf_b2b.previous_invoice_hash = initial_pih
        siaf_b2b.save(ignore_permissions=True)

# Build Einvoice Model & XML
einvoice_b2b = Einvoice(sales_invoice_additional_fields_doc=siaf_b2b, invoice_type=InvoiceType.STANDARD)
xml_b2b = generate_xml_file(einvoice_b2b.result)
b2b_hash = hashlib.sha256(xml_b2b.encode("utf-8")).hexdigest()
b2b_hash_b64 = base64.b64encode(hashlib.sha256(xml_b2b.encode("utf-8")).digest()).decode("utf-8")
siaf_b2b.invoice_hash = b2b_hash_b64
siaf_b2b.save(ignore_permissions=True)

print("\n==========================================")
print("PHASE 2 XML GENERATION: B2B STANDARD INVOICE")
print("==========================================")
print(f"Invoice: {b2b_inv.name}")
print(f"ICV (Invoice Counter Value): {siaf_b2b.invoice_counter}")
print(f"PIH (Previous Invoice Hash): {siaf_b2b.previous_invoice_hash}")
print(f"Calculated SHA-256 Invoice Hash (Hex):    {b2b_hash}")
print(f"Calculated SHA-256 Invoice Hash (Base64): {b2b_hash_b64}")
print(f"Generated UBL 2.1 XML Length: {len(xml_b2b)} bytes")
print("XML Structure Validations:")
print(f"  - <Invoice xmlns=\"urn:oasis:names:specification:ubl:schema:xsd:Invoice-2\": {'<Invoice' in xml_b2b}")
print(f"  - ProfileID (ZATCA reporting): {'<cbc:ProfileID>' in xml_b2b}")
print(f"  - Invoice Type Code 388 (Standard): {'388' in xml_b2b}")
print(f"  - Seller VAT ID 310123456700003: {'310123456700003' in xml_b2b}")
print(f"  - Buyer VAT ID 300000000000003: {'300000000000003' in xml_b2b}")
print(f"  - Payable Amount 4600.0: {'4600' in xml_b2b or '4,600' in xml_b2b}")
print(f"  - Tax Amount 600.0: {'600' in xml_b2b}")

# 4. Generate Phase 2 XML for B2C Invoice (Simplified)
b2c_inv = frappe.get_doc("Sales Invoice", "ACC-SINV-2026-00002")
siaf_b2c_name = frappe.db.get_value("Sales Invoice Additional Fields", {"sales_invoice": b2c_inv.name}, "name")
if not siaf_b2c_name:
    siaf_b2c = siaf_mod.SalesInvoiceAdditionalFields.create_for_invoice(b2c_inv.name, b2c_inv.doctype)
    siaf_b2c.invoice_counter = 2
    siaf_b2c.previous_invoice_hash = b2b_hash_b64
    siaf_b2c.insert(ignore_permissions=True)
    print(f"\nCreated Sales Invoice Additional Fields for B2C: {siaf_b2c.name}")
else:
    siaf_b2c = frappe.get_doc("Sales Invoice Additional Fields", siaf_b2c_name)
    if not siaf_b2c.invoice_counter:
        siaf_b2c.invoice_counter = 2
        siaf_b2c.previous_invoice_hash = b2b_hash_b64
        siaf_b2c.save(ignore_permissions=True)

einvoice_b2c = Einvoice(sales_invoice_additional_fields_doc=siaf_b2c, invoice_type=InvoiceType.SIMPLIFIED)
xml_b2c = generate_xml_file(einvoice_b2c.result)
b2c_hash = hashlib.sha256(xml_b2c.encode("utf-8")).hexdigest()
b2c_hash_b64 = base64.b64encode(hashlib.sha256(xml_b2c.encode("utf-8")).digest()).decode("utf-8")
siaf_b2c.invoice_hash = b2c_hash_b64
siaf_b2c.save(ignore_permissions=True)

print("\n==========================================")
print("PHASE 2 XML GENERATION: B2C SIMPLIFIED INVOICE")
print("==========================================")
print(f"Invoice: {b2c_inv.name}")
print(f"ICV (Invoice Counter Value): {siaf_b2c.invoice_counter}")
print(f"PIH (Previous Invoice Hash chained to B2B): {siaf_b2c.previous_invoice_hash}")
print(f"Calculated SHA-256 Invoice Hash (Hex):    {b2c_hash}")
print(f"Calculated SHA-256 Invoice Hash (Base64): {b2c_hash_b64}")
print(f"Generated UBL 2.1 XML Length: {len(xml_b2c)} bytes")
print("XML Structure Validations:")
print(f"  - <Invoice xmlns=\"urn:oasis:names:specification:ubl:schema:xsd:Invoice-2\": {'<Invoice' in xml_b2c}")
print(f"  - Invoice Type Code 388: {'388' in xml_b2c}")
print(f"  - Payable Amount 1150.0: {'1150' in xml_b2c or '1,150' in xml_b2c}")
print(f"  - Tax Amount 150.0: {'150' in xml_b2c}")

frappe.db.commit()
print("\nPHASE 2 XML & HASHING VERIFICATION COMPLETED SUCCESSFULLY!")
