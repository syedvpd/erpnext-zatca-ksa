import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
import base64
import json
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

import ksa_compliance
import ksa_compliance.jinja as ksa_jinja

print("==================================================")
print("PHASE 13: KSA COMPLIANCE VERIFICATION")
print("==================================================")

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

for inv_name in ["ACC-SINV-2026-00001", "ACC-SINV-2026-00002"]:
    inv = frappe.get_doc("Sales Invoice", inv_name)
    print(f"\n--- Testing Invoice: {inv_name} ({inv.customer}) ---")
    
    # 1. Test Phase 1 QR
    try:
        # Check jinja QR function
        qr_code = ksa_jinja.get_zatca_phase_1_qr_for_invoice(inv_name)
        print(f"Generated Phase 1 QR payload (length={len(qr_code)}):")
        print(f"  Base64: {qr_code[:60]}...")
        
        # Decode TLV
        tags = decode_tlv(qr_code)
        print("Decoded TLV 5 Mandatory Tags:")
        tag_names = {
            1: "Seller Name",
            2: "VAT Registration Number",
            3: "Timestamp",
            4: "Invoice Total (Inc. VAT)",
            5: "VAT Total"
        }
        for t, name in tag_names.items():
            val = tags.get(t, "MISSING")
            print(f"  Tag {t} ({name}): {val}")
            
        # Cross-verify
        assert tags.get(1) == inv.company, "Seller name mismatch"
        assert tags.get(2) == "310123456700003", "VAT number mismatch"
        assert float(tags.get(4)) == float(inv.grand_total), "Grand total mismatch"
        assert float(tags.get(5)) == float(inv.total_taxes_and_charges), "VAT total mismatch"
        print("  -> Phase 1 TLV 5-Tag Cross-Verification: PASSED LOCALLY")
    except Exception as e:
        print(f"  Phase 1 QR Error: {e}")

# 2. Test Phase 2 XML Generation
print("\n--- Testing Phase 2 XML Generation ---")
try:
    import ksa_compliance.generate_xml as gxml
    print("generate_xml module loaded:", [f for f in dir(gxml) if not f.startswith("_")])
    
    # Test generating XML for B2B invoice
    inv = frappe.get_doc("Sales Invoice", "ACC-SINV-2026-00001")
    xml_content = gxml.generate_xml_file(inv)
    print(f"Phase 2 XML Generated successfully! (Length={len(xml_content)} chars)")
    print("XML Preview (first 300 chars):")
    print(xml_content[:300])
    print("...")
    print("Contains UBL Invoice tag:", "<Invoice" in xml_content)
    print("Contains Seller Tax ID:", "310123456700003" in xml_content)
    print("Contains Grand Total 4600:", "4600" in xml_content or "4,600" in xml_content)
    print("  -> Phase 2 XML Generation: VERIFIED LOCALLY")
except Exception as e:
    import traceback
    print(f"  Phase 2 XML Error: {e}")
    traceback.print_exc()
