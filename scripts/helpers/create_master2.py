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

# 1. Master Data: Customers
b2b_name = "Saudi B2B Customer"
if not frappe.db.exists("Customer", b2b_name):
    cust = frappe.new_doc("Customer")
    cust.customer_name = b2b_name
    cust.customer_type = "Company"
    cust.customer_group = "Commercial"
    cust.territory = "Saudi Arabia"
    cust.tax_id = "300000000000003"
    cust.insert(ignore_permissions=True)
    print(f"Created B2B Customer: {b2b_name}, VAT ID: {cust.tax_id}")
else:
    cust = frappe.get_doc("Customer", b2b_name)
    cust.customer_group = "Commercial"
    cust.tax_id = "300000000000003"
    cust.save(ignore_permissions=True)
    print(f"Customer exists/updated: {b2b_name}")

b2c_name = "Saudi B2C Customer"
if not frappe.db.exists("Customer", b2c_name):
    cust = frappe.new_doc("Customer")
    cust.customer_name = b2c_name
    cust.customer_type = "Individual"
    cust.customer_group = "Individual"
    cust.territory = "Saudi Arabia"
    cust.insert(ignore_permissions=True)
    print(f"Created B2C Customer: {b2c_name}")
else:
    print(f"Customer exists: {b2c_name}")

# 2. Master Data: Supplier
supp_name = "Saudi Local Supplier"
if not frappe.db.exists("Supplier", supp_name):
    supp = frappe.new_doc("Supplier")
    supp.supplier_name = supp_name
    supp.supplier_group = "Local"
    supp.country = "Saudi Arabia"
    supp.tax_id = "310000000000003"
    supp.insert(ignore_permissions=True)
    print(f"Created Supplier: {supp_name}, VAT ID: {supp.tax_id}")
else:
    print(f"Supplier exists: {supp_name}")

# 3. Master Data: Items
items_data = [
    {"item_code": "Laptop", "item_name": "Laptop", "item_group": "Products", "is_stock_item": 1, "standard_rate": 2000.0, "valuation_rate": 1500.0},
    {"item_code": "Trading Product", "item_name": "Trading Product", "item_group": "Products", "is_stock_item": 1, "standard_rate": 1000.0, "valuation_rate": 700.0},
    {"item_code": "Consulting Service", "item_name": "Consulting Service", "item_group": "Services", "is_stock_item": 0, "standard_rate": 5000.0, "valuation_rate": 0.0}
]
uom = frappe.db.get_value("UOM", {"uom_name": "Nos"}, "name") or "Unit"
for itm in items_data:
    if not frappe.db.exists("Item", itm["item_code"]):
        doc = frappe.new_doc("Item")
        doc.item_code = itm["item_code"]
        doc.item_name = itm["item_name"]
        doc.item_group = itm["item_group"]
        doc.stock_uom = uom
        doc.is_stock_item = itm["is_stock_item"]
        doc.standard_rate = itm["standard_rate"]
        doc.valuation_rate = itm["valuation_rate"]
        doc.insert(ignore_permissions=True)
        print(f"Created Item: {itm['item_code']}")
    else:
        print(f"Item exists: {itm['item_code']}")

frappe.db.commit()
print("Master data created successfully.")
