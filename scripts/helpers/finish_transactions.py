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
wh_name = f"Stores - {abbr}"

# Check if Stock Entry for Trading Product needed
if frappe.db.get_value("Bin", {"item_code": "Trading Product", "warehouse": wh_name}, "actual_qty") or 0 < 1:
    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type = "Material Receipt"
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
else:
    print("Trading Product stock already exists.")

# Check if B2B Sales Invoice already exists
existing_b2b = frappe.db.get_value("Sales Invoice", {"customer": "Saudi B2B Customer", "docstatus": 1}, "name")
if not existing_b2b:
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
    existing_b2b = si_b2b.name
else:
    print(f"B2B Sales Invoice already exists: {existing_b2b}")

# Payment Entry for B2B Sales Invoice
existing_pe = frappe.db.get_value("Payment Entry Reference", {"reference_name": existing_b2b, "docstatus": 1}, "parent")
if not existing_pe:
    from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
    pe = get_payment_entry(dt="Sales Invoice", dn=existing_b2b)
    pe.mode_of_payment = "Wire Transfer"
    pe.paid_to = f"Demo Bank Account - {abbr}"
    pe.reference_no = "REF-B2B-001"
    pe.reference_date = today()
    pe.save(ignore_permissions=True)
    pe.submit()
    print(f"Submitted Payment Entry: {pe.name}, Paid Amount: {pe.paid_amount}")
else:
    print(f"Payment Entry already exists: {existing_pe}")

# B2C Sales Invoice (Simplified)
existing_b2c = frappe.db.get_value("Sales Invoice", {"customer": "Saudi B2C Customer", "docstatus": 1}, "name")
if not existing_b2c:
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
else:
    print(f"B2C Sales Invoice already exists: {existing_b2c}")

frappe.db.commit()
print("Transactions committed successfully.")
