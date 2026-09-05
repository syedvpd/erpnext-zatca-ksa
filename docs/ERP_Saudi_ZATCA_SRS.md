# Software Requirements Specification (SRS)
## Saudi Accounting & ZATCA ERP Suite (v15)

---

## 1. Introduction
This Software Requirements Specification (SRS) details the precise technical behaviors, interfaces, data formats, and regulatory requirements enforced by the **Saudi Accounting & ZATCA ERP Suite (v15)**.

---

## 2. Regulatory ZATCA (Fatoora) Compliance Specification

### 2.1 Phase 1: Electronic Invoice Generation Specification
The system enforces the ZATCA Resolution issued under the VAT Regulation. Every Tax Invoice must embed a dynamic QR code adhering to the **Tag-Length-Value (TLV)** byte structure, serialized in Base64 encoding.

```
+-----------------------------------------------------------------------------+
|                     ZATCA TLV ENCODING BYTE PROTOCOL                        |
+-----------------------------------------------------------------------------+
| Tag (1 byte) | Length (1 byte) | Value (N bytes UTF-8)                      |
+-----------------------------------------------------------------------------+
```

#### Mandatory Tag Definitions:
1. **Tag 1: Seller's Name**
   - Identifier: `0x01`
   - Content: Legal registered corporate name (e.g., `Saudi Trading & Services Co.`).
2. **Tag 2: VAT Registration Number**
   - Identifier: `0x02`
   - Content: 15-digit tax identification number starting and ending with '3' (e.g., `310123456700003`).
3. **Tag 3: Invoice Timestamp**
   - Identifier: `0x03`
   - Content: Standard ISO-8601 formatted datetime string (`YYYY-MM-DDTHH:MM:SS`).
4. **Tag 4: Invoice Grand Total (with VAT)**
   - Identifier: `0x04`
   - Content: Numerical string of invoice grand total in SAR (e.g., `11500.00`).
5. **Tag 5: VAT Total Amount**
   - Identifier: `0x05`
   - Content: Numerical string of 15% VAT amount in SAR (e.g., `1500.00`).

#### Phase 2 Additional Cryptographic Tags:
6. **Tag 6: SHA-256 Hash of XML** (`0x06`)
7. **Tag 7: ECDSA Digital Signature** (`0x07`)
8. **Tag 8: ECDSA Public Key** (`0x08`)
9. **Tag 9: Cryptographic Stamp Identifier** (`0x09`)

### 2.2 Phase 2: Electronic Invoicing Integration Specification
The system builds Universal Business Language (UBL 2.1) XML documents matching ZATCA XML Profiles:
- **Root Element:** `<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">`
- **Profile Execution:** `urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0`
- **Sequential Invoicing Counter (ICV):** Incremental integer assigned monotonically per device/company without gaps.
- **Previous Invoice Hash (PIH):** Base64 encoded SHA-256 hash of the preceding invoice's signed canonical XML, ensuring cryptographic tamper detection across the entire invoice ledger.

---

## 3. Financial Engine & Double-Entry Ledger Specifications

### 3.1 Currency & Precision
- Base Currency: `SAR` (Saudi Riyal).
- Currency Symbol: `ر.س` or `SAR`.
- Fractional Units: Halalas (`1 SAR = 100 Halalas`).
- Internal Currency Precision: 2 decimal places standard; configurable to 4 decimal places for unit prices.

### 3.2 Automated General Ledger Posting Rules
Upon document submission (`docstatus = 1`), the system executes atomic SQL transactions inserting records into `tabGL Entry`:

#### Scenario A: B2B Sales Invoice Submission (Invoice Total: SAR 11,500)
- **Debit:** `1310 - Accounts Receivable - STC` -> `SAR 11,500.00`
- **Credit:** `4110 - Sales Revenue - STC` -> `SAR 10,000.00`
- **Credit:** `2220 - VAT on Sales - STC` -> `SAR 1,500.00`
- *Verification Check:* $\sum Debit (11,500.00) == \sum Credit (11,500.00)$.

#### Scenario B: Supplier Purchase Invoice Submission (Invoice Total: SAR 5,750)
- **Debit:** `5110 - Cost of Goods Sold - STC` -> `SAR 5,000.00`
- **Debit:** `1220 - VAT on Purchases - STC` -> `SAR 750.00`
- **Credit:** `2110 - Accounts Payable - STC` -> `SAR 5,750.00`
- *Verification Check:* $\sum Debit (5,750.00) == \sum Credit (5,750.00)$.

#### Scenario C: Customer Payment Receipt (SAR 11,500)
- **Debit:** `1110 - Cash on Hand / Bank - STC` -> `SAR 11,500.00`
- **Credit:** `1310 - Accounts Receivable - STC` -> `SAR 11,500.00`
- *Verification Check:* Accounts Receivable cleared to `0.00`.
