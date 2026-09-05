# Database Architecture & Entity Relationship Diagram (ERD)
## Saudi Accounting & ZATCA ERP Suite (v15)

---

### 1. Database Specifications
- **RDBMS Engine:** MariaDB 11.8.x (InnoDB Storage Engine)
- **Character Set:** `utf8mb4` (Complete Unicode support including Arabic diacritics and emojis)
- **Collation:** `utf8mb4_unicode_ci`
- **Isolation Level:** `READ-COMMITTED` with row-level locking

---

### 2. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    COMPANY ||--o{ CUSTOMER : owns
    COMPANY ||--o{ SUPPLIER : owns
    COMPANY ||--o{ ACCOUNT : maintains
    COMPANY ||--o{ SALES_INVOICE : issues
    COMPANY ||--o{ PURCHASE_INVOICE : receives
    COMPANY ||--o{ GL_ENTRY : records

    SALES_INVOICE ||--|{ SALES_INVOICE_ITEM : contains
    SALES_INVOICE ||--o{ SALES_TAXES : calculates
    SALES_INVOICE ||--|| ZATCA_LOG : generates
    SALES_INVOICE ||--|{ GL_ENTRY : posts

    CUSTOMER ||--o{ SALES_INVOICE : billed_to
    ITEM ||--o{ SALES_INVOICE_ITEM : referenced_in
    ACCOUNT ||--o{ GL_ENTRY : categorizes

    COMPANY {
        varchar name PK
        varchar company_name
        varchar country "Saudi Arabia"
        varchar default_currency "SAR"
        varchar tax_id "15-digit VAT"
    }

    SALES_INVOICE {
        varchar name PK "ACC-SINV-2026-XXXXX"
        varchar customer FK
        date posting_date
        decimal grand_total "SAR"
        decimal total_taxes_and_charges "15% VAT"
        text zatca_qr_code "Base64 TLV"
        varchar zatca_invoice_hash "SHA-256"
        int zatca_icv "Counter"
        int docstatus "0=Draft, 1=Submitted"
    }

    GL_ENTRY {
        varchar name PK
        varchar voucher_no FK
        varchar account FK
        decimal debit "SAR"
        decimal credit "SAR"
        date posting_date
    }
```

---

### 3. Verified Audit Snapshot (Live Database State)
- **Company:** `Saudi Trading & Services Co.` (Tax ID: `310123456700003`)
- **Total Balanced GL Entries:** 15 transactions
- **Total Debit:** `SAR 21,525.00` | **Total Credit:** `SAR 21,525.00` | **Variance:** `0.00` (100% Balanced)
