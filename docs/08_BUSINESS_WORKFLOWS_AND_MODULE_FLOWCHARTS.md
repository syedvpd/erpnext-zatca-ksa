# Business Workflows & Module Flowcharts
## Saudi Accounting & ZATCA ERP Suite (v15)

---

### 1. Order-to-Cash (O2C) Workflow with ZATCA Phase 1 QR

```mermaid
graph TD
    A[Customer Request] --> B[Quotation / Sales Pitch]
    B --> C[Sales Order Confirmed]
    C --> D[Delivery Note: Goods Dispatched from Warehouse]
    D --> E[Stock Ledger Automatically Decremented]
    C --> F[Create Sales Invoice]
    F --> G[System Calculates 15% VAT Output]
    G --> H[Submit Sales Invoice]
    H --> I[Generate Base64 TLV QR Code]
    H --> J[Post GL: Debit AR / Credit Revenue & VAT]
    H --> K[Generate Standard / Simplified Print Format]
    K --> L[Payment Entry: Settle Cash / Bank in SAR]
```

---

### 2. ZATCA Phase 2 E-Invoicing Clearance & Reporting Engine

```mermaid
graph TD
    INV[Sales Invoice Submitted] --> CHK{Invoice Type?}
    
    CHK -->|B2B: Standard Tax Invoice| B2B[Clearance Workflow]
    CHK -->|B2C: Simplified Tax Invoice| B2C[Reporting Workflow]

    B2B --> B2B1[Generate UBL 2.1 XML]
    B2B1 --> B2B2[Assign Sequential ICV e.g. 1, 2, 3]
    B2B2 --> B2B3[Calculate Previous Invoice Hash PIH]
    B2B3 --> B2B4[Canonicalize XML & Compute SHA-256 Hash]
    B2B4 --> B2B5[Sign XML with Cryptographic Stamp X.509]
    B2B5 --> B2B6[Send API Request to ZATCA Fatoora Portal]
    B2B6 --> B2B7{ZATCA Response}
    B2B7 -->|Cleared 200 OK| B2B8[Attach ZATCA Clearance Stamp & Deliver to Buyer]

    B2C --> B2C1[Generate UBL 2.1 XML + TLV QR Code]
    B2C1 --> B2C2[Issue Immediately to Consumer at POS]
    B2C2 --> B2C3[Batch Report to ZATCA within 24 Hours]
```

---

### 3. Procure-to-Pay (P2P) Workflow & Input VAT Reclamation

```mermaid
graph TD
    PR[Material Request] --> PO[Purchase Order to Supplier]
    PO --> PRCV[Purchase Receipt: Goods Received in Warehouse]
    PRCV --> SLE[Stock Ledger Automatically Incremented]
    PO --> PINV[Purchase Invoice: Vendor Bill]
    PINV --> PVAT[Calculate 15% Input VAT Asset Account 1220]
    PINV --> PGL[Post GL: Debit Expense/Asset & Input VAT / Credit AP]
    PINV --> PPAY[Payment Entry: Bank Wire Transfer in SAR]
```
