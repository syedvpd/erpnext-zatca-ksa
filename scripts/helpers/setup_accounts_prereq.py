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

# 1. Accounts Setup
vat_acc_name = f"VAT 15% - {abbr}"
if not frappe.db.exists("Account", vat_acc_name):
    doc = frappe.new_doc("Account")
    doc.account_name = "VAT 15%"
    doc.company = company_name
    doc.parent_account = f"Duties and Taxes - {abbr}"
    doc.account_type = "Tax"
    doc.insert(ignore_permissions=True)
    print(f"Created: {vat_acc_name}")

input_vat_acc_name = f"Input VAT 15% - {abbr}"
if not frappe.db.exists("Account", input_vat_acc_name):
    doc = frappe.new_doc("Account")
    doc.account_name = "Input VAT 15%"
    doc.company = company_name
    doc.parent_account = f"Tax Assets - {abbr}"
    doc.account_type = "Tax"
    doc.insert(ignore_permissions=True)
    print(f"Created: {input_vat_acc_name}")

bank_acc_name = f"Demo Bank Account - {abbr}"
if not frappe.db.exists("Account", bank_acc_name):
    doc = frappe.new_doc("Account")
    doc.account_name = "Demo Bank Account"
    doc.company = company_name
    doc.parent_account = f"Bank Accounts - {abbr}"
    doc.account_type = "Bank"
    doc.insert(ignore_permissions=True)
    print(f"Created: {bank_acc_name}")

# Link Bank Account in Mode of Payment Wire Transfer
mop = frappe.get_doc("Mode of Payment", "Wire Transfer")
has_link = False
for acc in mop.accounts:
    if acc.company == company_name:
        acc.default_account = bank_acc_name
        has_link = True
if not has_link:
    mop.append("accounts", {"company": company_name, "default_account": bank_acc_name})
mop.save(ignore_permissions=True)

# 2. Warehouse Setup
wh_name = f"Stores - {abbr}"
if not frappe.db.exists("Warehouse", wh_name):
    wh = frappe.new_doc("Warehouse")
    wh.warehouse_name = "Stores"
    wh.company = company_name
    wh.insert(ignore_permissions=True)
    print(f"Created Warehouse: {wh_name}")

# Update Company default inventory account and default warehouse
comp = frappe.get_doc("Company", company_name)
comp.default_warehouse = wh_name
comp.default_bank_account = bank_acc_name
comp.default_cash_account = f"Cash - {abbr}"
comp.default_receivable_account = f"Debtors - {abbr}"
comp.default_payable_account = f"Creditors - {abbr}"
comp.default_inventory_account = f"Stock In Hand - {abbr}"
comp.stock_received_but_not_billed = f"Stock Received But Not Billed - {abbr}"
comp.expenses_included_in_valuation = f"Expenses Included In Valuation - {abbr}"
comp.save(ignore_permissions=True)

frappe.db.commit()
print("Accounting prerequisites committed successfully.")
