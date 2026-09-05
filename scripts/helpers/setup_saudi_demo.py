import frappe

def run():
    print("Checking Setup Wizard status...")
    setup_complete = frappe.db.get_single_value("System Settings", "setup_complete")
    print("setup_complete:", setup_complete)
    if not setup_complete:
        print("Running erpnext_setup_complete...")
        from erpnext.setup.setup_wizard.setup_wizard import setup_complete as erpnext_setup_complete
        args = {
            "language": "en",
            "country": "Saudi Arabia",
            "timezone": "Asia/Riyadh",
            "currency": "SAR",
            "full_name": "Administrator",
            "email": "admin@example.com",
            "company_name": "Demo Saudi Trading Company",
            "company_abbr": "DSTC",
            "chart_of_accounts": "Standard",
            "fy_start_date": "2026-01-01",
            "fy_end_date": "2026-12-31",
        }
        erpnext_setup_complete(args)
        frappe.db.commit()
        print("Setup wizard finished!")
    else:
        print("Setup wizard was already completed.")

run()
