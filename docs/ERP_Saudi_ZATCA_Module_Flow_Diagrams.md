# Detailed Module Flow Diagrams
## Saudi Accounting & ZATCA ERP Suite (v15)

---

## 1. ZATCA Phase 1 TLV QR Code Generation Flowchart

```mermaid
flowchart TD
    Start([User Clicks 'Submit' on Invoice]) --> Extract[Extract 5 Mandatory ZATCA Fields]
    Extract --> F1[Tag 1: Company Legal Name]
    Extract --> F2[Tag 2: 15-Digit VAT Registration Number]
    Extract --> F3[Tag 3: ISO-8601 Timestamp]
    Extract --> F4[Tag 4: Invoice Grand Total in SAR]
    Extract --> F5[Tag 5: 15% VAT Total in SAR]

    F1 & F2 & F3 & F4 & F5 --> Pack[Binary TLV Packing: Tag + Length + Value Bytes]
    Pack --> Concat[Concatenate TLV Byte String]
    Concat --> B64[Base64 Encoding]
    B64 --> SaveDB[(Store Base64 String in tabSales Invoice)]
    SaveDB --> RenderSVG[Render Scannable 2D Barcode on Print Format]
    RenderSVG --> Finish([Invoice Ready for Tax Inspection])
```

---

## 2. ZATCA Phase 2 Cryptographic Hash Chaining Flowchart

```mermaid
flowchart TD
    A[Sales Invoice Submitted] --> B[Generate UBL 2.1 XML Structure]
    B --> C[Fetch Previous Invoice Hash PIH from Database]
    C --> D{Is this the first invoice?}
    D -->|Yes| E[Set PIH = Base64 of SHA-256 of '0']
    D -->|No| F[Set PIH = SHA-256 Hash of Previous Invoice XML]
    E & F --> G[Assign Incremental ICV Counter e.g. 1, 2, 3...]
    G --> H[Embed PIH and ICV into XML Nodes]
    H --> I[C14N XML Canonicalization]
    I --> J[Compute Cryptographic SHA-256 Digest]
    J --> K[Sign XML with X.509 ECDSA Private Key]
    K --> L[Generate XML Signature Block & QR Tags 6-9]
    L --> M[(Commit Signed XML & Hash to Database)]
    M --> N[Transmit via REST API to ZATCA Fatoora Portal]
```

---

## 3. Financial Ledger Posting & Double-Entry Balancing Flowchart

```mermaid
flowchart TD
    T[Transaction Submitted: Sales / Purchase / Payment] --> Begin[Begin MariaDB Atomic Transaction]
    Begin --> Rule{Transaction Type?}

    Rule -->|Sales Invoice| SI[Debit Accounts Receivable 1310
Credit Sales Revenue 4110
Credit Output VAT 2220]
    Rule -->|Purchase Invoice| PI[Debit Cost of Goods / Asset
Debit Input VAT 1220
Credit Accounts Payable 2110]
    Rule -->|Payment Receipt| PY[Debit Bank / Cash 1110
Credit Accounts Receivable 1310]

    SI & PI & PY --> BalCheck{Check Balance:
Total Debit == Total Credit?}
    BalCheck -->|Variance != 0| Rollback[Abort & Rollback Transaction
Throw Invariant Error]
    BalCheck -->|Variance == 0| Commit[Commit to tabGL Entry
Update Account Running Balances]
    Commit --> Finish([Real-Time Ledger Updated])
```
