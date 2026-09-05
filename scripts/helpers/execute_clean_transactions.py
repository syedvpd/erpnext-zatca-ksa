import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
from frappe.utils import today, flt
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

company_name = "Demo Saudi Trading Company"
abbr = "DSTC"
vat_account = f"VAT 15% - {abbr}"
input_vat_account = f"Input VAT 15% - {abbr}"
wh_name = f"Stores - {abbr}"
bank_account = f"Demo Bank Account - {abbr}"

print("1. Creating Purchase Invoice...")
pi = frappe.new_doc("Purchase Invoice")
pi.company = company_name
pi.supplier = "Saudi Local Supplier"
pi.posting_date = today()
pi.update_stock = 1
pi.set_warehouse = wh_name
pi.currency = "SAR"

pi.append("items", {
    "item_code": "Laptop",
    "qty": 2,
    "rate": 1500.0,
    "warehouse": wh_name
})
pi.append("items", {
    "item_code": "Trading Product",
    "qty": 5,
    "rate": 700.0,
    "warehouse": wh_name
})

pi.append("taxes", {
    "charge_type": "On Net Total",
    "account_head": input_vat_account,
    "description": "Input VAT 15%",
    "rate": 15.0
})

pi.save(ignore_permissions=True)
pi.submit()
frappe.db.commit()
print(f"Submitted & Committed PI: {pi.name}")
print(f"  Net Total: {pi.net_total}, Taxes: {pi.total_taxes_and_charges}, Grand Total: {pi.grand_total}")

print("2. Creating B2B Sales Invoice...")
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
    "warehouse": wh_name,
    "cost_center": f"Main - {abbr}"
})

si_b2b.append("taxes", {
    "charge_type": "On Net Total",
    "account_head": vat_account,
    "description": "VAT 15%",
    "rate": 15.0
})

si_b2b.save(ignore_permissions=True)
si_b2b.submit()
frappe.db.commit()
print(f"Submitted & Committed B2B SI: {si_b2b.name}")
print(f"  Net Total: {si_b2b.net_total}, Taxes: {si_b2b.total_taxes_and_charges}, Grand Total: {si_b2b.grand_total}")

print("3. Creating Payment Entry for B2B SI...")
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
pe = get_payment_entry(dt="Sales Invoice", dn=si_b2b.name)
pe.mode_of_payment = "Wire Transfer"
pe.paid_to = bank_account
pe.reference_no = "REF-B2B-001"
pe.reference_date = today()
pe.save(ignore_permissions=True)
pe.submit()
frappe.db.commit()
print(f"Submitted & Committed PE: {pe.name}, Amount: {pe.paid_amount}")

print("4. Creating B2C Sales Invoice (Simplified)...")
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
    "warehouse": wh_name,
    "cost_center": f"Main - {abbr}"
})

si_b2c.append("taxes", {
    "charge_type": "On Net Total",
    "account_head": vat_account,
    "description": "VAT 15%",
    "rate": 15.0
})

si_b2c.save(ignore_permissions=True)
si_b2c.submit()
frappe.db.commit()
print(f"Submitted & Committed B2C SI: {si_b2c.name}")
print(f"  Net Total: {si_b2c.net_total}, Taxes: {si_b2c.total_taxes_and_charges}, Grand Total: {si_b2c.grand_total}")

print("ALL TRANSACTIONS SUCCESSFULLY POSTED AND COMMITTED!")
