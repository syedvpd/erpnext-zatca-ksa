# Backend Architecture & Execution Manual
## Saudi Accounting & ZATCA ERP Suite (v15)

---

## 1. Architectural Philosophy
The backend architecture is built on the **Frappe Model-View-Controller (MVC) Metadata Architecture** running on Python 3.11 with Gunicorn. It operates with a clear separation of concerns:
- **Presentation Layer (Nginx):** Reverse proxies traffic, serves compiled desk assets, and load-balances requests.
- **Application Engine (Frappe/ERPNext):** Executes business rules, manages state machines, and enforces role-based permissions.
- **Regulatory Hooks (KSA Compliance):** Intercepts document lifecycles to calculate ZATCA Phase 1 QR codes and Phase 2 XML documents.
- **Persistence Layer (MariaDB 11.8):** Executes ACID transactions with row-level locking.

---

## 2. DocType ORM & Controller Lifecycle
Every entity in the system is defined as a **DocType**. The controller lifecycle enforces strict transaction boundaries:

```
+-----------------------------------------------------------------------------+
|                     DOCTYPE CONTROLLER EXECUTION LIFECYCLE                   |
+-----------------------------------------------------------------------------+
|                                                                             |
|  [ 1. BEFORE INSERT ]      -> Validate schema, check mandatory fields       |
|            |                                                                |
|  [ 2. VALIDATE ]           -> Validate business logic, verify 15% VAT       |
|            |                                                                |
|  [ 3. BEFORE SAVE ]        -> Apply system defaults, calculate grand totals |
|            |                                                                |
|  [ 4. ON UPDATE ]          -> Write Draft record to MariaDB (docstatus = 0) |
|            |                                                                |
|  ======================= USER CLICKS 'SUBMIT' ============================= |
|            |                                                                |
|  [ 5. BEFORE SUBMIT ]      -> Lock document for mutation                    |
|            |                                                                |
|  [ 6. ON SUBMIT (HOOKS) ]  -> 1. Generate ZATCA Base64 TLV QR Code          |
|            |                  2. Generate UBL 2.1 XML & SHA-256 Hash        |
|            |                  3. Assign sequential ICV counter              |
|            |                  4. Post double-entry General Ledger entries   |
|            |                  5. Update Stock Ledger entries (FIFO)         |
|            |                  6. Commit MariaDB transaction (docstatus = 1) |
|            |                                                                |
|  [ 7. ON CANCEL ]          -> Generate reversal GL & Stock entries          |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 3. ZATCA Compliance Integration Hook Implementation
The Saudi ZATCA compliance logic is cleanly bound to the Sales Invoice lifecycle via `apps/ksa_compliance/ksa_compliance/hooks.py`:

```python
# Event binding in hooks.py
doc_events = {
    "Sales Invoice": {
        "validate": "ksa_compliance.events.sales_invoice.validate",
        "on_submit": "ksa_compliance.events.sales_invoice.on_submit",
        "on_cancel": "ksa_compliance.events.sales_invoice.on_cancel"
    }
}
```

### Execution Flow on Invoice Submission:
1. **`validate`:** Inspects the company's Saudi tax settings. Ensures customer VAT number format conforms to the 15-digit standard (`3XXXXXXXXXXXXX3`) for B2B invoices.
2. **`on_submit`:**
   - Extracts Company Name, VAT ID, Timestamp, Grand Total, and VAT Amount.
   - Encodes data into binary Tag-Length-Value (TLV) structure.
   - Computes Base64 representation and stores it in the `zatca_qr_code` field on `tabSales Invoice`.
   - Serializes the document into UBL 2.1 compliant XML.
   - Canonicalizes the XML and computes the SHA-256 invoice hash.
   - Updates the sequential Invoice Counter Value (`zatca_icv`).
3. **Database Commit:** The entire payload (invoice, QR code, XML hash, and balanced GL entries) commits atomically to MariaDB.
