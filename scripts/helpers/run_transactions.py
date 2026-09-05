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

# 1. Purchase Invoice exactly per user requirement:
# Supplier: Saudi Local Supplier
# Laptop, Qty: 2, Rate: 1,500, Subtotal: 3,000, Input VAT 15%: 450, Total: 3,450
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

pi.append("taxes", {
    "charge_type": "On Net Total",
    "account_head": input_vat_account,
    "description": "Input VAT 15%",
    "rate": 15.0
})

pi.save(ignore_permissions=True)
pi.submit()
print(f"Submitted Purchase Invoice: {pi.name}")
print(f"  Net Total: {pi.net_total}, Taxes: {pi.total_taxes_and_charges}, Grand Total: {pi.grand_total}")

# Also receive 1 Trading Product into Stock via Stock Entry for B2C sale
se = frappe.new_doc("Stock Entry")
se.purpose = "Material Receipt"
se.company = company_name
se.posting_date = today()
se.append("items", {
    "item_code": "Trading Product",
    "qty": 5,
    "t_warehouse": wh_name,
    "basic_rate": 700.0,
    "cost_center": f"Main - {abbr}"
})
se.save(ignore_permissions=True)
se.submit()
print(f"Submitted Stock Entry for Trading Product: {se.name}")

# 2. B2B Sales Invoice
# Customer: Saudi B2B Customer
# Laptop, Qty: 2, Rate: 2,000, Subtotal: 4,000, VAT 15%: 600, Grand Total: 4,600
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
print(f"Submitted B2B Sales Invoice: {si_b2b.name}")
print(f"  Net Total: {si_b2b.net_total}, Taxes: {si_b2b.total_taxes_and_charges}, Grand Total: {si_b2b.grand_total}")

# 3. Payment Entry for B2B Sales Invoice
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
pe = get_payment_entry(dt="Sales Invoice", dn=si_b2b.name)
pe.mode_of_payment = "Wire Transfer"
pe.paid_to = f"Demo Bank Account - {abbr}"
pe.reference_no = "REF-B2B-001"
pe.reference_date = today()
pe.save(ignore_permissions=True)
pe.submit()
print(f"Submitted Payment Entry: {pe.name}, Paid Amount: {pe.paid_amount}")

# 4. B2C Sales Invoice (Simplified)
# Customer: Saudi B2C Customer
# Trading Product, Qty: 1, Rate: 1,000, Subtotal: 1,000, VAT 15%: 150, Grand Total: 1,150
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
print(f"Submitted B2C Sales Invoice: {si_b2c.name}")
print(f"  Net Total: {si_b2c.net_total}, Taxes: {si_b2c.total_taxes_and_charges}, Grand Total: {si_b2c.grand_total}")

frappe.db.commit()
print("All transactions created, posted, and committed successfully!")
