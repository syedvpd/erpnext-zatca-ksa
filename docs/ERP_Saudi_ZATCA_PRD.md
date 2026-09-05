# Product Requirements Document (PRD)
## Saudi Accounting & ZATCA ERP Suite (v15)

---

## 1. Document Overview
- **Document Title:** Product Requirements Document (PRD)
- **Product Name:** Saudi Accounting & ZATCA ERP Suite (v15)
- **Product Architect & Integrator:** SYED ZUBAIR (syedvpd)
- **Target Market:** Kingdom of Saudi Arabia (KSA) - Commercial, Industrial, Trading & Service Enterprises
- **Document Version:** 1.0 (Enterprise Release)

---

## 2. Product Vision & Goals

### 2.1 Vision
To deliver the most reliable, fully self-hosted, and legally compliant Enterprise Resource Planning system for businesses in the Kingdom of Saudi Arabia, eliminating compliance risks, software subscription bloat, and foreign data hosting concerns.

### 2.2 Core Product Goals
1. **100% Autonomous ZATCA Invoicing:** Enable small-to-large businesses to issue compliant Phase 1 TLV QR code invoices and integrate seamlessly with ZATCA Phase 2 clearance APIs without recurring third-party middleware fees.
2. **SOCPA Accounting Compliance:** Provide an out-of-the-box Saudi Chart of Accounts, standard 15% VAT calculation, and automated VAT return generation matching GAZT/ZATCA tax filing formats.
3. **Data Residency Compliance:** Guarantee that 100% of financial, customer, employee, and transaction records reside on servers located within the Kingdom of Saudi Arabia.
4. **Complete Source Code Transparency:** Provide client enterprises with full control of their software stack, container definitions, database backups, and custom business logic.

---

## 3. User Personas & Journey Maps

### Persona 1: Tariq Al-Ghamdi (Chief Financial Officer - CFO)
- **Background:** 20 years in Saudi corporate finance.
- **Needs:** Real-time visibility into company balance sheets, profit & loss, operating cash flows, and tax liabilities.
- **Pain Points:** Disjointed spreadsheets, delayed month-end closings, anxiety regarding ZATCA tax penalties.
- **Core Workflows:**
  1. Accesses executive dashboard daily to monitor cash and bank balances in SAR.
  2. Reviews General Ledger and Trial Balance before monthly sign-off.
  3. Audits the automated Saudi 15% VAT return report before official ZATCA portal submission.

### Persona 2: Faisal Al-Otaibi (Chief Accountant / Tax Lead)
- **Background:** Certified Saudi accountant specializing in VAT and corporate tax.
- **Needs:** Accurate segregation of Output VAT (sales) and Input VAT (purchases), strict double-entry ledger balancing, and bank reconciliation.
- **Pain Points:** Human error in calculating 15% tax on diverse invoice items, managing debit/credit notes, manual tax returns.
- **Core Workflows:**
  1. Sets up and audits Tax and Charges Templates (`Saudi VAT 15% - STC`).
  2. Creates and verifies Journal Entries for operational adjustments.
  3. Audits invoice ledger postings (`tabGL Entry`) to ensure debit equals credit.

### Persona 3: Sarah Al-Harbi (Sales & Invoicing Officer)
- **Background:** High-volume commercial sales coordinator.
- **Needs:** Rapid generation of quotations, sales orders, and invoices that immediately generate scannable ZATCA QR codes.
- **Pain Points:** Slow system responses during checkout, manual calculation of VAT, invoice rejections by corporate clients.
- **Core Workflows:**
  1. Selects customer master and line items from catalog.
  2. Selects invoice type (`Standard B2B` vs. `Simplified B2C`).
  3. Clicks 'Submit' to immediately generate a verified bilingual Tax Invoice with printed ZATCA QR code.

### Persona 4: Khalid Mansoor (IT Systems & Security Administrator)
- **Background:** Enterprise DevOps & Infrastructure Engineer.
- **Needs:** Automated deployment, zero downtime, isolated container architecture, automated daily backups.
- **Pain Points:** Complex installations, database corruption risks, security vulnerabilities, cloud data sovereignty breaches.
- **Core Workflows:**
  1. Deploys the complete 9-container topology via `docker compose up -d`.
  2. Configures automated nightly MariaDB backups to local encrypted storage.
  3. Manages user roles, password policies, and two-factor authentication.

---

## 4. Feature Requirements Matrix

| ID | Feature Name | Priority | Description | Acceptance Criteria |
| :--- | :--- | :---: | :--- | :--- |
| **FR-01** | **ZATCA Phase 1 QR Generation** | P0 (Critical) | Generate Base64 TLV encoded QR code on all invoices. | QR contains Tags 1 through 5, decodable via ZATCA mobile validator. |
| **FR-02** | **ZATCA Phase 2 UBL 2.1 XML** | P0 (Critical) | Generate standard UBL 2.1 XML structure with invoice hashing. | Generates valid XML with sequential ICV and SHA-256 hash chaining. |
| **FR-03** | **Saudi 15% VAT Automation** | P0 (Critical) | Automatically calculate 15% VAT on standard items. | Split into Output VAT (Account 2220) and Input VAT (Account 1220). |
| **FR-04** | **Saudi Chart of Accounts** | P0 (Critical) | Pre-configured 5-root SOCPA compliant chart in SAR. | Standard asset, liability, equity, income, and expense accounts pre-seeded. |
| **FR-05** | **Double-Entry General Ledger** | P0 (Critical) | Immutable double-entry bookkeeping engine. | Enforce `Total Debit == Total Credit` on every document submission. |
| **FR-06** | **Bilingual Print Engine** | P1 (High) | Dual-language (Arabic/English) invoice print formats. | Conforms to Saudi VAT Article 53 requirement for bilingual tax invoices. |
| **FR-07** | **Order-to-Cash Pipeline** | P1 (High) | Quotation -> Sales Order -> Delivery Note -> Sales Invoice. | One-click document conversion with automatic stock and GL posting. |
| **FR-08** | **Procure-to-Pay Pipeline** | P1 (High) | Material Request -> PO -> Purchase Receipt -> Purchase Invoice. | Automated accounts payable posting and input VAT deduction. |
| **FR-09** | **Multi-Warehouse Stock** | P1 (High) | Inventory ledger with automated FIFO valuation. | Real-time valuation and bin tracking across multiple locations. |
| **FR-10** | **Executive Dashboard & BI** | P2 (Medium) | Real-time charts for revenue, expenses, and receivables. | Visual graphs and KPI indicator cards on Frappe Desk. |

---

## 5. Non-Functional Requirements & Benchmarks
1. **Performance:** Invoice submission and QR generation must complete in under 200 milliseconds.
2. **Availability:** Multi-container topology engineered for 99.9% availability with Docker healthchecks.
3. **Auditability:** Once an invoice is submitted, it cannot be modified or deleted. Adjustments require formal Debit/Credit notes or cancellation workflow.
4. **Data Sovereignty:** Zero outbound network traffic to external unauthorized services or analytics trackers.
