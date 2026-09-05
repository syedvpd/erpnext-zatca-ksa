import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
import inspect
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()

from ksa_compliance.output_models.e_invoice_output_model import Einvoice
print(inspect.getsource(Einvoice.__init__))
