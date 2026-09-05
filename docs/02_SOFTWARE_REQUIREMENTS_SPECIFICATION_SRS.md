# Software Requirements Specification (SRS)
## Saudi Accounting & ZATCA ERP Suite (v15)

---

### 1. Introduction
This Software Requirements Specification (SRS) defines the functional, interface, and performance specifications for the **Saudi Accounting & ZATCA ERP Suite (v15)**.

---

### 2. Regulatory Compliance Specifications (ZATCA / Fatoora)

#### 2.1 Phase 1: E-Invoice Generation (Enforced Since December 4, 2021)
The system MUST generate a QR code encoded in **Base64 Tag-Length-Value (TLV)** format on all Tax Invoices and Simplified Tax Invoices upon document submission.

| Tag | Field Name | Data Format | Requirement | Validation Rule |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Seller's Name | UTF-8 String | Mandatory | Matches Company Legal Name |
| **2** | VAT Registration Number | 15-digit numeric string | Mandatory | Must begin and end with '3' (Saudi 15-digit VAT standard) |
| **3** | Time Stamp | ISO 8601 String | Mandatory | Format: `YYYY-MM-DDTHH:MM:SS` |
| **4** | Invoice Total (with VAT) | Decimal String | Mandatory | Matches `grand_total` in SAR |
| **5** | VAT Total | Decimal String | Mandatory | Matches `total_taxes_and_charges` |

#### 2.2 Phase 2: Integration & Clearance (Wave-Based Implementation)
The system MUST generate an XML document compliant with the **Universal Business Language (UBL 2.1)** standard matching the Saudi Tax Profile.

```
+-----------------------------------------------------------------------------+
|                     ZATCA Phase 2 Cryptographic Structure                   |
+-----------------------------------------------------------------------------+
| 1. Invoice Counter Value (ICV) : Sequential integer (1, 2, 3, ...)          |
| 2. Previous Invoice Hash (PIH) : SHA-256 Base64 hash of previous XML        |
|    - Initial invoice PIH = SHA-256("0")                                     |
| 3. Invoice Hash                : SHA-256 digest of canonicalized XML        |
| 4. Digital Signature           : ECDSA secp256k1 signature via X.509 cert   |
| 5. QR Code Tag 6 & 7           : ECDSA Public Key & Signature bytes         |
+-----------------------------------------------------------------------------+
```

---

### 3. Core Functional Use Cases

```mermaid
usecaseDiagram
    actor "Accountant" as Acc
    actor "Sales Rep" as Sales
    actor "ZATCA Gateway" as ZATCA

    package "Saudi Accounting & ZATCA Suite" {
        usecase "Create Sales Invoice" as UC1
        usecase "Calculate 15% VAT" as UC2
        usecase "Generate Phase 1 TLV QR" as UC3
        usecase "Generate Phase 2 UBL XML" as UC4
        usecase "Post Double-Entry Ledger" as UC5
        usecase "Submit to ZATCA API" as UC6
    }

    Sales --> UC1
    UC1 --> UC2
    UC1 --> UC3
    Acc --> UC5
    UC1 ..> UC4 : triggers
    UC4 --> UC6
    UC6 --> ZATCA
```

---

### 4. Financial & Double-Entry Accounting Requirements
1. **Currency Support:** Primary accounting currency MUST be Saudi Riyal (`SAR`).
2. **Double-Entry Consistency:** Every submitted transaction MUST generate balanced `tabGL Entry` records where:
   $$\sum \text{Debit} = \sum \text{Credit}$$
3. **Chart of Accounts:** Standard Saudi SOCPA-compliant 5-root hierarchy:
   - `1000 - Application of Funds (Assets)`
   - `2000 - Source of Funds (Liabilities)`
   - `3000 - Equity`
   - `4000 - Income`
   - `5000 - Expenses`
4. **15% VAT Tracking:** Automatic segregation into:
   - `2220 - VAT on Sales (Output VAT)` [Liability]
   - `1220 - VAT on Purchases (Input VAT)` [Asset]
