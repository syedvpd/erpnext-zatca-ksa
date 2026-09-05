import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
from frappe.utils import today, nowdate, flt
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

company_name = "Demo Saudi Trading Company"
abbr = "DSTC"
vat_account = f"VAT 15% - {abbr}"
input_vat_account = f"Input VAT 15% - {abbr}"

# Ensure default warehouse exists
warehouse = frappe.db.get_value("Warehouse", {"company": company_name, "is_group": 0}, "name")
if not warehouse:
    warehouse = frappe.db.get_value("Warehouse", {"is_group": 0}, "name")
print(f"Using warehouse: {warehouse}")

# ==========================================
# 1. Purchase Invoice
# ==========================================
# Purchase 2 Laptops @ 1,500 SAR and 2 Trading Products @ 700 SAR
pi = frappe.new_doc("Purchase Invoice")
pi.company = company_name
pi.supplier = "Saudi Local Supplier"
pi.posting_date = today()
pi.update_stock = 1
pi.set_warehouse = warehouse
pi.currency = "SAR"

pi.append("items", {
    "item_code": "Laptop",
    "qty": 2,
    "rate": 1500.0,
    "warehouse": warehouse
})
pi.append("items", {
    "item_code": "Trading Product",
    "qty": 2,
    "rate": 700.0,
    "warehouse": warehouse
})

pi.append("taxes", {
    "charge_type": "On Net Total",
    "account_head": input_vat_account,
    "description": "Input VAT 15%",
    "rate": 15.0
})

pi.save(ignore_permissions=True)
pi.submit()
print(f"Submitted Purchase Invoice: {pi.name}, Net Total: {pi.net_total}, VAT: {pi.total_taxes_and_charges}, Grand Total: {pi.grand_total}")

# Verify GL for Purchase Invoice
gl_pi = frappe.get_all("GL Entry", filters={"voucher_no": pi.name}, fields=["account", "debit", "credit"])
print(f"Purchase Invoice GL Entries ({len(gl_pi)}):")
for g in gl_pi:
    print(f"  {g.account}: Debit={g.debit}, Credit={g.credit}")

# ==========================================
# 2. B2B Sales Invoice
# ==========================================
si_b2b = frappe.new_doc("Sales Invoice")
si_b2b.company = company_name
si_b2b.customer = "Saudi B2B Customer"
si_b2b.posting_date = today()
si_b2b.update_stock = 1
si_b2b.currency = "SAR"

si_b2b.append("items", {
    "item_code": "Laptop",
    "qty": 2,
    "rate": 2000.0,
    "warehouse": warehouse
})

si_b2b.append("taxes", {
    "charge_type": "On Net Total",
    "account_head": vat_account,
    "description": "VAT 15%",
    "rate": 15.0
})

si_b2b.save(ignore_permissions=True)
si_b2b.submit()
print(f"Submitted B2B Sales Invoice: {si_b2b.name}, Net Total: {si_b2b.net_total}, VAT: {si_b2b.total_taxes_and_charges}, Grand Total: {si_b2b.grand_total}")

# Verify GL for B2B Sales Invoice
gl_b2b = frappe.get_all("GL Entry", filters={"voucher_no": si_b2b.name}, fields=["account", "debit", "credit"])
print(f"B2B Sales Invoice GL Entries ({len(gl_b2b)}):")
for g in gl_b2b:
    print(f"  {g.account}: Debit={g.debit}, Credit={g.credit}")

# ==========================================
# 3. Payment Entry for B2B Sales Invoice
# ==========================================
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
pe = get_payment_entry(dt="Sales Invoice", dn=si_b2b.name)
pe.mode_of_payment = "Wire Transfer"
pe.reference_no = "REF-B2B-001"
pe.reference_date = today()
pe.save(ignore_permissions=True)
pe.submit()
print(f"Submitted Payment Entry: {pe.name}, Paid Amount: {pe.paid_amount}")

# Verify GL for Payment Entry
gl_pe = frappe.get_all("GL Entry", filters={"voucher_no": pe.name}, fields=["account", "debit", "credit"])
print(f"Payment Entry GL Entries ({len(gl_pe)}):")
for g in gl_pe:
    print(f"  {g.account}: Debit={g.debit}, Credit={g.credit}")

# ==========================================
# 4. B2C Sales Invoice (Simplified)
# ==========================================
si_b2c = frappe.new_doc("Sales Invoice")
si_b2c.company = company_name
si_b2c.customer = "Saudi B2C Customer"
si_b2c.posting_date = today()
si_b2c.update_stock = 1
si_b2c.currency = "SAR"

si_b2c.append("items", {
    "item_code": "Trading Product",
    "qty": 1,
    "rate": 1000.0,
    "warehouse": warehouse
})

si_b2c.append("taxes", {
    "charge_type": "On Net Total",
    "account_head": vat_account,
    "description": "VAT 15%",
    "rate": 15.0
})

si_b2c.save(ignore_permissions=True)
si_b2c.submit()
print(f"Submitted B2C Sales Invoice: {si_b2c.name}, Net Total: {si_b2c.net_total}, VAT: {si_b2c.total_taxes_and_charges}, Grand Total: {si_b2c.grand_total}")

# Verify GL for B2C Sales Invoice
gl_b2c = frappe.get_all("GL Entry", filters={"voucher_no": si_b2c.name}, fields=["account", "debit", "credit"])
print(f"B2C Sales Invoice GL Entries ({len(gl_b2c)}):")
for g in gl_b2c:
    print(f"  {g.account}: Debit={g.debit}, Credit={g.credit}")

frappe.db.commit()
print("All transactions created and submitted successfully!")
