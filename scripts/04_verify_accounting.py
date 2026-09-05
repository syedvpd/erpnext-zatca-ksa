import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
from frappe.utils import flt
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

company_name = "Demo Saudi Trading Company"
abbr = "DSTC"

print("==================================================")
print("PHASE 12: GENERAL LEDGER & ACCOUNTING VERIFICATION")
print("==================================================")

# 1. Total GL Debit and Credit
gl_totals = frappe.db.sql("""
    SELECT SUM(debit) as total_debit, SUM(credit) as total_credit
    FROM `tabGL Entry`
    WHERE company = %s AND is_cancelled = 0
""", (company_name,), as_dict=True)[0]

total_debit = flt(gl_totals.total_debit, 2)
total_credit = flt(gl_totals.total_credit, 2)
is_balanced = (total_debit == total_credit)
print(f"1. GL Balance Check:")
print(f"   Total Debit:  SAR {total_debit:,.2f}")
print(f"   Total Credit: SAR {total_credit:,.2f}")
print(f"   Debit == Credit: {'PASS' if is_balanced else 'FAIL'}")

# 2. Account Balances
print("\n2. Account Balances Breakdown:")
balances = frappe.db.sql("""
    SELECT account, SUM(debit) - SUM(credit) as net_balance
    FROM `tabGL Entry`
    WHERE company = %s AND is_cancelled = 0
    GROUP BY account
    ORDER BY account
""", (company_name,), as_dict=True)

for b in balances:
    print(f"   {b.account}: SAR {flt(b.net_balance, 2):,.2f}")

# 3. VAT Accounts Verification
vat_output = frappe.db.sql("""
    SELECT SUM(credit) - SUM(debit) as output_vat
    FROM `tabGL Entry`
    WHERE account = %s AND is_cancelled = 0
""", (f"VAT 15% - {abbr}",), as_dict=True)[0].output_vat or 0.0

vat_input = frappe.db.sql("""
    SELECT SUM(debit) - SUM(credit) as input_vat
    FROM `tabGL Entry`
    WHERE account = %s AND is_cancelled = 0
""", (f"Input VAT 15% - {abbr}",), as_dict=True)[0].input_vat or 0.0

print(f"\n3. VAT Position:")
print(f"   Output VAT (15% on Sales): SAR {flt(vat_output, 2):,.2f}")
print(f"   Input VAT (15% on Purchases): SAR {flt(vat_input, 2):,.2f}")
print(f"   Net VAT Position: SAR {flt(vat_output - vat_input, 2):,.2f} ({'Payable' if vat_output > vat_input else 'Refundable/Credit'})")

# 4. Invoices Status Verification
b2b_inv = frappe.get_doc("Sales Invoice", "ACC-SINV-2026-00001")
print(f"\n4. Invoice Status:")
print(f"   B2B Invoice (ACC-SINV-2026-00001): Status={b2b_inv.status}, Grand Total={b2b_inv.grand_total}, Outstanding={b2b_inv.outstanding_amount}")

b2c_inv = frappe.get_doc("Sales Invoice", "ACC-SINV-2026-00002")
print(f"   B2C Invoice (ACC-SINV-2026-00002): Status={b2c_inv.status}, Grand Total={b2c_inv.grand_total}, Outstanding={b2c_inv.outstanding_amount}")

pinv = frappe.get_doc("Purchase Invoice", "ACC-PINV-2026-00001")
print(f"   Purchase Invoice (ACC-PINV-2026-00001): Status={pinv.status}, Grand Total={pinv.grand_total}, Outstanding={pinv.outstanding_amount}")
