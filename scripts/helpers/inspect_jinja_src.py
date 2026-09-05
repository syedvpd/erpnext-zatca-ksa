import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
import inspect
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()

import ksa_compliance.jinja as kj
print("Source of get_zatca_phase_1_qr_for_invoice:")
print(inspect.getsource(kj.get_zatca_phase_1_qr_for_invoice))

import ksa_compliance.generate_xml as gx
print("\nSource of generate_xml_file:")
print(inspect.getsource(gx.generate_xml_file))
