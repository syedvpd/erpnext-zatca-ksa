import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

path = "/home/frappe/frappe-bench/apps/ksa_compliance/ksa_compliance/ksa_compliance/doctype/sales_invoice_additional_fields/sales_invoice_additional_fields.py"
with open(path) as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "generate_xml_file(" in l:
        for j in range(max(0, i - 15), min(len(lines), i + 25)):
            print(f"{j+1}: {lines[j]}", end="")
