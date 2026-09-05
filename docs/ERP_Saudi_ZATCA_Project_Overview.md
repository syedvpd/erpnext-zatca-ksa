# Saudi Accounting & ZATCA ERP Suite (v15)
## Comprehensive Project Overview & Executive Brief

---

## 1. Executive Summary

The **Saudi Accounting & ZATCA ERP Suite (v15)** is an enterprise-grade, fully localized Enterprise Resource Planning system specifically engineered for commercial and industrial enterprises operating within the **Kingdom of Saudi Arabia (KSA)**.

The software addresses two critical operational requirements for Saudi enterprises:
1. **Uncompromised Regulatory Compliance:** Out-of-the-box compliance with the electronic invoicing mandates issued by the **Zakat, Tax and Customs Authority (ZATCA - هيئة الزكاة والضريبة والجمارك)** under the Fatoora project, covering both **Phase 1 (Generation of TLV Base64 QR Invoices)** and **Phase 2 (Integration with UBL 2.1 XML, Cryptographic Stamping, sequential ICV, and SHA-256 hash chaining)**.
2. **Comprehensive Corporate Resource Planning:** A unified double-entry financial accounting, procurement, sales, multi-warehouse inventory, and human resources platform localized with the **Saudi SOCPA Chart of Accounts**, automatic **15% Value Added Tax (VAT)**, and bilingual Arabic/English operational parity.

---

## 2. Market Problem & Solution Analysis

### 2.1 The Regulatory Challenge in Saudi Arabia
Starting December 4, 2021, ZATCA mandated Phase 1 electronic invoicing across all VAT-registered resident taxpayers. Taxpayers must issue electronic invoices containing tamper-proof QR codes with strict TLV structure. Starting January 1, 2023, ZATCA rolled out Phase 2 in waves, requiring enterprise ERP systems to integrate directly via REST APIs with the ZATCA Fatoora clearance platform using Universal Business Language (UBL 2.1) XML standard, ECDSA digital signatures, cryptographic hashes, and strict clearance/reporting workflows.

Legacy systems (such as generic QuickBooks, SAP, or Tally) require expensive third-party middleware, recurring per-invoice SaaS API fees, and complex middleware configurations that introduce latency and single points of failure.

### 2.2 The Solution: Unified In-Kingdom ERP Architecture
This platform integrates the ZATCA compliance engine natively into the database transaction boundary:
- **Zero Middleware:** Invoices generate compliant QR codes and UBL 2.1 XML directly inside the ERP backend at the moment of document submission (`on_submit`).
- **Data Sovereignty:** The system is 100% containerized with Docker, deployable inside Saudi Arabian cloud regions (Oracle Cloud Riyadh, AWS Riyadh, STC Cloud) or on-premise private data centers, ensuring full compliance with the National Cybersecurity Authority (NCA) and Cloud Computing Regulatory Framework.
- **Zero Recurring Per-Invoice Fees:** Perpetual ownership of the source code and deployment topology with no vendor lock-in.

---

## 3. Core Architectural Pillars

```
+-----------------------------------------------------------------------------+
|               SAUDI ACCOUNTING & ZATCA ERP SUITE (v15)                     |
+-----------------------------------------------------------------------------+
|                                                                             |
|  [ LAYER 1: CLIENT PRESENTATION ]                                           |
|  - Frappe Desk Vue.js / HTML5 SPA                                           |
|  - Native Bilingual Arabic (RTL) / English (LTR) Parity                     |
|  - Dual-Language Print Engine (Jinja2 + SVG / Base64 QR Code)               |
|                                                                             |
|  [ LAYER 2: REVERSE PROXY & GATEWAY ]                                       |
|  - Nginx 1.26 HTTP/HTTPS Proxy (Port 8080 / 443)                           |
|  - Static Asset Offloading & Gzip Compression                               |
|                                                                             |
|  [ LAYER 3: CORE ERP APPLICATION ENGINE ]                                   |
|  - Frappe Framework v15 (Python 3.11 WSGI / Gunicorn)                       |
|  - ERPNext v15 Financials, Sales, Buying, Inventory, Payroll                |
|  - KSA Compliance App (ZATCA Phase 1 & 2 Engine)                            |
|                                                                             |
|  [ LAYER 4: ASYNCHRONOUS WORKER & QUEUE ENGINE ]                            |
|  - Redis 7.x In-Memory Broker & Cache                                       |
|  - Python-RQ Dual Workers (queue-short & queue-long)                        |
|  - Frappe Cron Scheduler & Socket.io WebSocket Push                         |
|                                                                             |
|  [ LAYER 5: DATA PERSISTENCE & SOVEREIGNTY ]                                |
|  - MariaDB 11.8 Relational Database (InnoDB ACID Engine)                    |
|  - Docker Named Persistent Volumes (Zero Data Loss)                         |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 4. Key Out-of-the-Box Capabilities

### 🇸🇦 ZATCA E-Invoicing Compliance
1. **Phase 1 (Generation):** Automatic generation of cryptographic Base64 TLV QR Codes containing Seller Name, 15-digit VAT Number, Timestamp, Grand Total, and VAT Total on all Tax Invoices.
2. **Phase 2 (Integration):** Native UBL 2.1 XML schema generation, sequential Invoice Counter Value (ICV) management, Previous Invoice Hash (PIH) chaining using SHA-256 digests, and preparation for cryptographic compliance.
3. **Dual Invoicing Workflows:**
   - **Standard Tax Invoice (B2B):** Clearance workflow for business-to-business transactions.
   - **Simplified Tax Invoice (B2C):** Immediate point-of-sale issuance with 24-hour reporting workflow.

### 💰 Complete Saudi Financial Accounting Engine
1. **SOCPA Chart of Accounts:** 5-root hierarchical accounts tree natively denominated in Saudi Riyals (SAR).
2. **Automated 15% VAT:** Pre-configured Tax Templates automatically routing 15% VAT into dedicated **Output VAT (Account 2220)** on sales and **Input VAT (Account 1220)** on purchases.
3. **Audit-Proof Double-Entry General Ledger:** Strictly enforces total debits equal total credits on every submitted transaction. Verified live state: `Debit == Credit == SAR 21,525.00` across 15 balanced GL ledger entries.
4. **Automated Financial Statements:** Real-time generation of Balance Sheet, Profit & Loss, Trial Balance, Cash Flow, and official Saudi VAT Return reports.

### 📦 Operational Supply Chain Modules
1. **Order-to-Cash (O2C):** Quotations, Sales Orders, Delivery Notes, Sales Invoices, and Payment Receipts with customer credit limits and multi-currency pricing.
2. **Procure-to-Pay (P2P):** Material Requests, Supplier Quotation Comparisons, Purchase Orders, Purchase Receipts, and Supplier Invoices.
3. **Multi-Warehouse Inventory:** Automated FIFO valuation, real-time Stock Ledger entries, multi-location stock transfers, and batch/serial tracking.
4. **Role-Based Security & Permissions:** Strict Role-Based Access Control (RBAC) governing system administrators, accountants, sales officers, purchase managers, and warehouse staff.

---

## 5. Source Code Ownership & Licensing Model
The software is distributed under a clean, multi-license open-source and integration structure:
- **Custom Integration, Docker Compose Topology, Automation Scripts & Master Documentation:** Licensed under [MIT License](LICENSE) (c) 2026 SYED ZUBAIR.
- **Core ERP Engine:** ERPNext (GNU General Public License v3.0 by Frappe Technologies Pvt. Ltd.).
- **Underlying Web Framework:** Frappe Framework (MIT License by Frappe Technologies Pvt. Ltd.).
- **Saudi ZATCA Regulatory Module:** KSA Compliance (GNU Affero General Public License v3.0 by LavaLoon and contributors).
- **Client Entitlement:** Full transfer of deployment topology, Docker configurations, and custom verification code with complete self-hosting autonomy.
