import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.set_user("Administrator")

company_name = "Demo Saudi Trading Company"
abbr = "DSTC"

# 1. Check & Create Tax Accounts
# Find parent account for Duties and Taxes
duties = frappe.db.get_value("Account", {"company": company_name, "account_name": ["like", "%Duties and Taxes%"], "is_group": 1}, "name")
if not duties:
    duties = frappe.db.get_value("Account", {"company": company_name, "root_type": "Liability", "is_group": 1}, "name")

vat_account = f"VAT 15% - {abbr}"
if not frappe.db.exists("Account", vat_account):
    acc = frappe.new_doc("Account")
    acc.account_name = "VAT 15%"
    acc.company = company_name
    acc.parent_account = duties
    acc.account_type = "Tax"
    acc.insert(ignore_permissions=True)
    print(f"Created Tax Account: {vat_account}")
else:
    print(f"Tax Account exists: {vat_account}")

current_assets = frappe.db.get_value("Account", {"company": company_name, "account_name": ["like", "%Current Assets%"], "is_group": 1}, "name")
input_vat_account = f"Input VAT 15% - {abbr}"
if not frappe.db.exists("Account", input_vat_account):
    acc = frappe.new_doc("Account")
    acc.account_name = "Input VAT 15%"
    acc.company = company_name
    acc.parent_account = current_assets
    acc.account_type = "Tax"
    acc.insert(ignore_permissions=True)
    print(f"Created Input Tax Account: {input_vat_account}")
else:
    print(f"Input Tax Account exists: {input_vat_account}")

# 2. Sales Taxes and Charges Template
stc_name = f"Saudi 15% VAT - {abbr}"
if not frappe.db.exists("Sales Taxes and Charges Template", stc_name):
    stc = frappe.new_doc("Sales Taxes and Charges Template")
    stc.title = stc_name
    stc.company = company_name
    stc.is_default = 1
    stc.append("taxes", {
        "charge_type": "On Net Total",
        "account_head": vat_account,
        "description": "VAT 15%",
        "rate": 15.0
    })
    stc.insert(ignore_permissions=True)
    print(f"Created Sales Tax Template: {stc_name}")
else:
    print(f"Sales Tax Template exists: {stc_name}")

# 3. Purchase Taxes and Charges Template
ptc_name = f"Saudi 15% Input VAT - {abbr}"
if not frappe.db.exists("Purchase Taxes and Charges Template", ptc_name):
    ptc = frappe.new_doc("Purchase Taxes and Charges Template")
    ptc.title = ptc_name
    ptc.company = company_name
    ptc.is_default = 1
    ptc.append("taxes", {
        "charge_type": "On Net Total",
        "account_head": input_vat_account,
        "description": "Input VAT 15%",
        "rate": 15.0
    })
    ptc.insert(ignore_permissions=True)
    print(f"Created Purchase Tax Template: {ptc_name}")
else:
    print(f"Purchase Tax Template exists: {ptc_name}")

# 4. Master Data: Customers
b2b_name = "Saudi B2B Customer"
if not frappe.db.exists("Customer", b2b_name):
    cust = frappe.new_doc("Customer")
    cust.customer_name = b2b_name
    cust.customer_type = "Company"
    cust.customer_group = "All Customer Groups"
    cust.territory = "Saudi Arabia"
    cust.tax_id = "300000000000003"
    cust.insert(ignore_permissions=True)
    print(f"Created B2B Customer: {b2b_name}, VAT ID: {cust.tax_id}")
else:
    cust = frappe.get_doc("Customer", b2b_name)
    cust.tax_id = "300000000000003"
    cust.save(ignore_permissions=True)
    print(f"Customer exists: {b2b_name}")

b2c_name = "Saudi B2C Customer"
if not frappe.db.exists("Customer", b2c_name):
    cust = frappe.new_doc("Customer")
    cust.customer_name = b2c_name
    cust.customer_type = "Individual"
    cust.customer_group = "All Customer Groups"
    cust.territory = "Saudi Arabia"
    cust.insert(ignore_permissions=True)
    print(f"Created B2C Customer: {b2c_name}")
else:
    print(f"Customer exists: {b2c_name}")

# 5. Master Data: Supplier
supp_name = "Saudi Local Supplier"
if not frappe.db.exists("Supplier", supp_name):
    supp = frappe.new_doc("Supplier")
    supp.supplier_name = supp_name
    supp.supplier_group = "All Supplier Groups"
    supp.country = "Saudi Arabia"
    supp.tax_id = "310000000000003"
    supp.insert(ignore_permissions=True)
    print(f"Created Supplier: {supp_name}, VAT ID: {supp.tax_id}")
else:
    print(f"Supplier exists: {supp_name}")

# 6. Master Data: Items
items_data = [
    {"item_code": "Laptop", "item_name": "Laptop", "is_stock_item": 1, "standard_rate": 2000.0, "valuation_rate": 1500.0},
    {"item_code": "Trading Product", "item_name": "Trading Product", "is_stock_item": 1, "standard_rate": 1000.0, "valuation_rate": 700.0},
    {"item_code": "Consulting Service", "item_name": "Consulting Service", "is_stock_item": 0, "standard_rate": 5000.0, "valuation_rate": 0.0}
]
uom = frappe.db.get_value("UOM", {"uom_name": "Nos"}, "name") or "Unit"
for itm in items_data:
    if not frappe.db.exists("Item", itm["item_code"]):
        doc = frappe.new_doc("Item")
        doc.item_code = itm["item_code"]
        doc.item_name = itm["item_name"]
        doc.item_group = "All Item Groups"
        doc.stock_uom = uom
        doc.is_stock_item = itm["is_stock_item"]
        doc.standard_rate = itm["standard_rate"]
        doc.valuation_rate = itm["valuation_rate"]
        doc.insert(ignore_permissions=True)
        print(f"Created Item: {itm['item_code']}")
    else:
        print(f"Item exists: {itm['item_code']}")

frappe.db.commit()
print("Master data and tax setup completed successfully.")
