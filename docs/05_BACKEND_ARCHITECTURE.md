# Backend Architecture & Execution Flow
## Saudi Accounting & ZATCA ERP Suite (v15)

---

### 1. Request Lifecycle & Controller Flow
Every incoming HTTP request traverses a strictly validated, decoupled execution pipeline:

```mermaid
sequenceDiagram
    autonumber
    participant Browser as Web Client / API
    participant Nginx as frontend (Nginx)
    participant WSGI as backend (Gunicorn)
    participant Auth as Auth & RBAC Guard
    participant Controller as DocType Controller
    participant ZATCA as KSA Compliance Hook
    participant DB as MariaDB 11.8

    Browser->>Nginx: POST /api/method/frappe.desk.form.save.savedocs
    Nginx->>WSGI: Proxy Pass (WSGI Request)
    WSGI->>Auth: Validate Session Cookie & CSRF Token
    Auth-->>WSGI: Authenticated (User: Administrator)
    WSGI->>Controller: Parse Document (Sales Invoice)
    Controller->>Controller: Validate Tax Calculation (15% VAT)
    Controller->>DB: Begin DB Transaction
    Controller->>DB: Insert tabSales Invoice (Status: Draft)
    
    Note over Controller,ZATCA: User clicks 'Submit'
    Controller->>ZATCA: on_submit Hook (KSA Compliance)
    ZATCA->>ZATCA: Generate Base64 TLV QR Code (Tags 1-5)
    ZATCA->>ZATCA: Generate UBL 2.1 XML & SHA-256 Hash
    ZATCA->>DB: Update Invoice with QR & Hash
    Controller->>DB: Post Balanced GL Entries (AR, Revenue, VAT)
    Controller->>DB: Commit Transaction
    DB-->>WSGI: Transaction Committed (ACID)
    WSGI-->>Nginx: HTTP 200 OK (JSON Response)
    Nginx-->>Browser: Updated Document with Verified QR Code
```

---

### 2. Modularity & Hook Architecture
The platform preserves core ERPNext upgradeability by leveraging the **Frappe Hooks Pattern**. Custom Saudi regulatory logic attaches asynchronously via `hooks.py`:

```python
# apps/ksa_compliance/ksa_compliance/hooks.py
doc_events = {
    "Sales Invoice": {
        "validate": "ksa_compliance.events.sales_invoice.validate",
        "on_submit": "ksa_compliance.events.sales_invoice.on_submit",
        "on_cancel": "ksa_compliance.events.sales_invoice.on_cancel"
    }
}
```

This guarantees:
- **Zero Core Tampering:** ERPNext core files remain 100% clean and vendor-updateable.
- **Strict Isolation:** All Saudi-specific ZATCA XML, QR, and certificate logic lives entirely inside `apps/ksa_compliance/`.
