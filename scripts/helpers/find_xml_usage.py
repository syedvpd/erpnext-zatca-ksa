import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()

import glob
ksa_dir = "/home/frappe/frappe-bench/apps/ksa_compliance/ksa_compliance"
py_files = glob.glob(f"{ksa_dir}/**/*.py", recursive=True)
for pf in py_files:
    with open(pf, "r", errors="ignore") as f:
        content = f.read()
        if "generate_xml_file" in content:
            print("Found generate_xml_file in:", pf)
        if "generate_xml" in content:
            print("Found generate_xml in:", pf)
