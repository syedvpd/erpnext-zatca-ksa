import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
import base64
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

import ksa_compliance.jinja as kj

print("==========================================")
print("TESTING PHASE 1 QR GENERATION & TLV")
print("==========================================")

def decode_tlv(qr_base64):
    raw = base64.b64decode(qr_base64)
    tlv_data = {}
    i = 0
    while i < len(raw):
        tag = raw[i]
        i += 1
        if i >= len(raw):
            break
        length = raw[i]
        i += 1
        value = raw[i:i+length]
        i += length
        try:
            tlv_data[tag] = value.decode("utf-8")
        except:
            tlv_data[tag] = value.hex()
    return tlv_data

tag_names = {
    1: "Seller Name",
    2: "VAT Registration Number",
    3: "Timestamp",
    4: "Invoice Total (Inc. VAT)",
    5: "VAT Total"
}

for inv_name in ["ACC-SINV-2026-00001", "ACC-SINV-2026-00002"]:
    inv = frappe.get_doc("Sales Invoice", inv_name)
    print(f"\n--- Testing Invoice: {inv_name} ({inv.customer}) ---")
    qr_svg_or_base64 = kj.get_zatca_phase_1_qr_for_invoice(inv_name)
    inputs = kj._get_qr_inputs(inv_name)
    print(f"Inputs extracted: {inputs}")
    decoded_string = kj._generate_decoded_string(inputs)
    print(f"Base64 TLV Payload: {decoded_string}")
    
    tags = decode_tlv(decoded_string)
    print("Decoded 5 Mandatory TLV Tags:")
    for t in range(1, 6):
        val = tags.get(t)
        print(f"  Tag {t} ({tag_names[t]}): {val}")
    
    # Assertions
    assert tags[1] == "Demo Saudi Trading Company", "Tag 1 mismatch"
    assert tags[2] == "310123456700003", "Tag 2 mismatch"
    assert float(tags[4]) == float(inv.grand_total), "Tag 4 mismatch"
    assert float(tags[5]) == float(inv.total_taxes_and_charges), "Tag 5 mismatch"
    print("  => Phase 1 TLV 5 Mandatory Tags: VERIFIED LOCALLY (PASS)")

# Inspect Phase 2 XML preparation
print("\n==========================================")
print("INVESTIGATING PHASE 2 XML PREPARATION")
print("==========================================")
import grep
import inspect
from ksa_compliance.zatca import sales_invoice
print("sales_invoice module attributes:", [a for a in dir(sales_invoice) if not a.startswith("_")])
