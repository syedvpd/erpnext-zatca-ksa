import os
for p in ["/home/frappe/logs", "/home/frappe/frappe-bench/logs", "/home/frappe/frappe-bench/frontend/logs", "/home/frappe/frappe-bench/sites/frontend/logs"]:
    os.makedirs(p, exist_ok=True)

import frappe
import inspect
os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()

from ksa_compliance.ksa_compliance.doctype.zatca_business_settings.zatca_business_settings import ZATCABusinessSettings
print(inspect.getsource(ZATCABusinessSettings.for_invoice))
