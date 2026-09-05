import requests

session = requests.Session()
login_res = session.post("http://localhost:8080/api/method/login", data={
    "usr": "Administrator",
    "pwd": "admin"
})
print("Login Status:", login_res.status_code, login_res.json())

pages_to_test = [
    "/app/home",
    "/app/company/Demo%20Saudi%20Trading%20Company",
    "/app/customer/Saudi%20B2B%20Customer",
    "/app/customer/Saudi%20B2C%20Customer",
    "/app/supplier/Saudi%20Local%20Supplier",
    "/app/item/Laptop",
    "/app/item/Trading%20Product",
    "/app/sales-invoice/ACC-SINV-2026-00001",
    "/app/sales-invoice/ACC-SINV-2026-00002",
    "/app/purchase-invoice/ACC-PINV-2026-00001",
    "/app/payment-entry/ACC-PAY-2026-00001",
    "/app/query-report/General%20Ledger",
    "/app/query-report/Trial%20Balance",
    "/app/query-report/Profit%20and%20Loss%20Statement",
    "/app/query-report/Balance%20Sheet",
    "/app/zatca-phase-1-business-settings",
    "/app/zatca-business-settings"
]

all_passed = True
for page in pages_to_test:
    res = session.get(f"http://localhost:8080{page}")
    status = "OK" if res.status_code == 200 else f"ERR {res.status_code}"
    if res.status_code != 200:
        all_passed = False
    print(f"GET {page} -> {res.status_code} ({status})")

print("\nBrowser Workflow Rehearsal Result:", "ALL PASSED" if all_passed else "FAILURES DETECTED")
