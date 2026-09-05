# ERPNext Saudi ZATCA E-Invoicing: Complete Platform Master Guide
**The Definitive Architecture, Module Breakdown, Free Online Deployment, and Client Sales Guide**

---

## TABLE OF CONTENTS
1. [Executive Positioning: How to Sell This to Saudi Clients](#1-executive-positioning-how-to-sell-this-to-saudi-clients)
2. [Free Online Deployment: How to Give Clients a Live HTTPS Link](#2-free-online-deployment-how-to-give-clients-a-live-https-link)
   - [Method 1: Instant Cloudflare Zero Trust Tunnel (100% Free, 2 Minutes)](#method-1-instant-cloudflare-zero-trust-tunnel-100-free-2-minutes)
   - [Method 2: Oracle Cloud Always Free VPS (Permanent Free Cloud Server)](#method-2-oracle-cloud-always-free-vps-permanent-free-cloud-server)
3. [Complete Platform Module & Feature Breakdown (Every Sidebar Item)](#3-complete-platform-module--feature-breakdown-every-sidebar-item)
   - [Module 1: Accounting (The Core Financial Engine)](#module-1-accounting-the-core-financial-engine)
   - [Module 2: ZATCA Saudi Compliance (The Tax & E-Invoicing Engine)](#module-2-zatca-saudi-compliance-the-tax--e-invoicing-engine)
   - [Module 3: Selling (Customer & Revenue Management)](#module-3-selling-customer--revenue-management)
   - [Module 4: Buying (Procurement & Supplier Management)](#module-4-buying-procurement--supplier-management)
   - [Module 5: Stock & Inventory (Warehousing & Valuation)](#module-5-stock--inventory-warehousing--valuation)
   - [Module 6: CRM & Opportunities](#module-6-crm--opportunities)
   - [Module 7: Assets, Manufacturing & Projects](#module-7-assets-manufacturing--projects)
   - [Module 8: Users, Roles & Security Permissions](#module-8-users-roles--security-permissions)
4. [Deep Dive into the 20 ZATCA Compliance Capabilities](#4-deep-dive-into-the-20-zatca-compliance-capabilities)
5. [Step-by-Step Client Demonstration Script (What to Click & What to Say)](#5-step-by-step-client-demonstration-script-what-to-click--what-to-say)
6. [Answers to Every Possible Client Question](#6-answers-to-every-possible-client-question)

---

## 1. EXECUTIVE POSITIONING: HOW TO SELL THIS TO SAUDI CLIENTS

### "Is this software free? Will we get caught? Can we sell this?"
* **The Legal Truth:** ERPNext is open-source software (licensed under GNU GPL/MIT). Open-source software is **100% legal to deploy, customize, host, package, and sell to businesses**.
* **How Enterprise IT Works:** The largest software consultancies in the world (like Red Hat, IBM, Accenture, and official Frappe Partners) do not charge for basic software licenses. Instead, they charge clients for:
  1. **Localization & Integration:** Implementing Saudi VAT, Arabic Chart of Accounts, and ZATCA compliance.
  2. **Turnkey Deployment & Cloud Hosting:** Setting up high-availability Docker infrastructure with automated backups.
  3. **Data Migration & Configuration:** Migrating legacy spreadsheets, setting up item catalogs, customer lists, and opening balances.
  4. **Employee Training & Support:** Providing staff onboarding and monthly maintenance contracts (SLA).

### What You Say to Your Client:
> *"We provide an enterprise-grade, cloud-ready ERP platform tailored specifically for the Saudi market. We handle the complete deployment, data security, ZATCA Phase 1 & Phase 2 integration, and ongoing system management so your company remains fully compliant with Zakat, Tax and Customs Authority regulations."*

---

## 2. FREE ONLINE DEPLOYMENT: HOW TO GIVE CLIENTS A LIVE HTTPS LINK

If you want to send your Saudi client a live link so they can open the demo on their phone or laptop, you have two 100% free options:

### METHOD 1: Instant Cloudflare Zero Trust Tunnel (100% Free, 2 Minutes)
This is the fastest method. It creates a secure, publicly accessible HTTPS URL directly to your local Docker container **without port forwarding, firewall changes, or paid domains**.

#### Step 1: Install Cloudflare Tunnel Client on Windows
Open PowerShell as Administrator and run:
```powershell
winget install --id Cloudflare.cloudflared -e
```

#### Step 2: Start the Tunnel to Port 8080
Make sure your Docker containers are running (`docker compose up -d`), then run:
```powershell
cloudflared tunnel --url http://localhost:8080
```

#### Step 3: Send the Link to Your Client
Cloudflare will instantly output a public URL in your terminal:
```
+--------------------------------------------------------------------------------------------+
|  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
|  https://saudi-demo-accounting-xyz.trycloudflare.com                                       |
+--------------------------------------------------------------------------------------------+
```
* Anyone in Saudi Arabia (or anywhere in the world) can open that link in their browser.
* They will see the clean login screen and can log in with `Administrator` / `admin`.
* As long as your terminal stays open, the link stays live.

---

### METHOD 2: Oracle Cloud Always Free VPS (Permanent Cloud Server)
If you want a 24/7 permanent free server in the cloud that never turns off:
1. Sign up for an **Oracle Cloud Free Tier** account (Select Home Region: *Saudi Arabia West - Jeddah* or *Frankfurt*).
2. Provision an **Always Free Ampere ARM instance** (4 OCPU, 24 GB RAM, 200 GB SSD) — completely free forever with no credit card charges.
3. SSH into the server, install Docker, and clone your GitHub repository:
   ```bash
   git clone https://github.com/syedvpd/erpnext-zatca-ksa.git
   cd erpnext-zatca-ksa
   docker compose up -d
   ```
4. Access the server's public IP on port 8080: `http://<YOUR_SERVER_IP>:8080`.

---

## 3. COMPLETE PLATFORM MODULE & FEATURE BREAKDOWN

When you log into the ERPNext Desk, you see a full navigation sidebar on the left. Here is what every single module does and how to demonstrate it:

```
┌───────────────────────────────────────────────────────────┐
│                     ERPNEXT DESK                          │
├───────────────┬───────────────────────────────────────────┤
│ 🏠 Home       │ Quick dashboard, shortcuts, system setup  │
│ 💰 Accounting │ GL, Invoices, Payments, Tax, Bank, P&L    │
│ 🇸🇦 ZATCA      │ Saudi E-Invoicing Phase 1 & 2 compliance  │
│ 🛍️ Selling    │ Customers, Quotations, Sales Orders       │
│ 🛒 Buying     │ Suppliers, Purchase Orders, Invoices      │
│ 📦 Stock      │ Inventory, Warehouses, Stock Ledger       │
│ 🏢 Assets     │ Fixed assets, depreciation schedules      │
│ 🏭 Mfg        │ Bill of Materials (BOM), Work Orders      │
│ 👥 Users      │ Roles, permissions, audit logs            │
└───────────────┴───────────────────────────────────────────┘
```

---

### MODULE 1: Accounting (The Core Financial Engine)

This is the primary module for financial controllers, accountants, and auditors.

* **Sales Invoice:** Create standard B2B invoices (with buyer VAT TRN) or B2C retail invoices. Automatically calculates 15% VAT, posts revenue, and tracks receivables.
* **Purchase Invoice:** Record supplier bills, calculate 15% Input VAT (tax asset), and track payables.
* **Payment Entry:** Settle invoices against Bank or Cash accounts with multi-currency conversion and payment reconciliation.
* **Journal Entry:** Manual double-entry journal vouchers for adjustments, opening balances, depreciation, and payroll.
* **Chart of Accounts:** The hierarchical tree of all Asset, Liability, Equity, Income, and Expense accounts. Pre-configured with Saudi SOCPA standards.
* **Taxes and Charges Templates:** Pre-built Saudi 15% VAT rules linked to general ledger tax accounts.
* **Key Reports:**
  * **General Ledger:** Complete audit trail of every debit and credit transaction.
  * **Trial Balance:** Summary of closing balances for all accounts.
  * **Profit and Loss Statement:** Real-time Gross Profit, Operating Expenses, and Net Income.
  * **Balance Sheet:** Real-time financial position (Assets = Liabilities + Equity).
  * **Accounts Receivable / Payable Aging:** Track overdue customer payments and supplier dues.

---

### MODULE 2: ZATCA Saudi Compliance (The Tax & E-Invoicing Engine)

This module handles all regulatory requirements from the Saudi Arabian Tax and Customs Authority.

* **ZATCA Phase 1 Business Settings:** Configures seller legal name, branch name, registered building address, and 15-digit Tax Identification Number (`310123456700003`).
* **ZATCA Business Settings (Phase 2):**
  * **Sync Modes:** Live (real-time clearance) or Batches (scheduled transmission).
  * **Environment Selector:** Sandbox (Developer testing), Simulation, or Production.
  * **CSR Generator:** Automated Certificate Signing Request generation.
  * **CSID Management:** Manages Compliance and Production security tokens.
* **Tax Categories:**
  * `Standard rate`: Standard 15% VAT on taxable goods and services.
  * `Zero rated`: 0% VAT on exports and qualifying medical/educational supplies.
  * `Exempt`: VAT-exempt supplies (e.g., qualifying financial services, residential leases).
  * `Out of scope`: Transactions outside Saudi VAT scope.
* **ZATCA Print Formats:**
  * `ZATCA Phase 1 Print Format`: Renders the mandatory dynamic Base64 TLV QR code on invoices.
  * `ZATCA Phase 2 Print Format`: Full UBL compliance layout.

---

### MODULE 3: Selling (Customer & Revenue Management)

* **Customer:** Maintain database of commercial entities (with CR numbers and Tax IDs) and retail consumers.
* **Quotation:** Generate professional sales quotes and proposals with validity dates.
* **Sales Order:** Confirm customer orders before fulfillment and lock inventory commitments.
* **Delivery Note:** Issue goods from the warehouse to the customer, automatically updating stock ledgers.
* **Sales Analytics:** Visual dashboards showing revenue trends, top-selling items, and customer profitability.

---

### MODULE 4: Buying (Procurement & Supplier Management)

* **Supplier:** Manage local and international vendors, tax IDs, and payment terms.
* **Material Request:** Internal purchase requisitions raised by department managers.
* **Purchase Order:** Official orders sent to suppliers with delivery schedules and negotiated prices.
* **Purchase Receipt (Goods Receipt Note):** Receive physical stock into warehouses before the financial bill arrives.
* **Landed Cost Voucher:** Allocate customs duties, freight, and shipping fees onto inventory valuation.

---

### MODULE 5: Stock & Inventory (Warehousing & Valuation)

* **Item Master:** Physical goods (Stock Items), consumables, or service items. Supports barcodes, batch numbers, serial numbers, and multiple units of measure (UOM).
* **Warehouse:** Multi-location inventory management (e.g., *Riyadh Main Warehouse*, *Jeddah Branch*, *Damman Stores*).
* **Stock Entry:** Material transfers between branches, manufacturing issues, stock adjustments, and opening stock entry.
* **Stock Ledger & Balance Report:** Real-time stock valuation using FIFO (First-In, First-Out) or Moving Average methods.

---

### MODULE 6: CRM & Opportunities

* **Lead & Opportunity:** Track prospective clients from initial inquiry to closed deal.
* **Customer Group & Territory:** Categorize sales regions (e.g., Central Region, Western Region, Eastern Region).
* **Communication History:** Full email thread logging and CRM notes attached to customer records.

---

### MODULE 7: Assets, Manufacturing & Projects

* **Fixed Assets:** Track computers, vehicles, and machinery with automated monthly depreciation entries.
* **Manufacturing:** Multi-level Bill of Materials (BOM), Work Orders, and production cost tracking.
* **Projects & Tasks:** Project costing, timesheets, and milestone billing.

---

### MODULE 8: Users, Roles & Security Permissions

* **Role-Based Access Control (RBAC):** Built-in roles like *Accounts User*, *Accounts Manager*, *Stock User*, *Sales User*.
* **Field-Level Security:** Restrict sensitive fields (e.g., purchase cost, salary) to authorized executives only.
* **Audit Trail:** Every single record creation, modification, and deletion is timestamped with the user's ID.

---

## 4. DEEP DIVE INTO THE 20 ZATCA COMPLIANCE CAPABILITIES

| # | Feature | Technical Explanation | Local Demo Status |
| :---: | :--- | :--- | :---: |
| **1** | **ZATCA Phase 1 Compliance** | Dynamic Base64 TLV QR code generated on all invoice print layouts. | **VERIFIED LOCALLY** |
| **2** | **ZATCA Phase 2 Compliance** | UBL 2.1 XML output models matching official ZATCA data schemas. | **VERIFIED LOCALLY** |
| **3** | **Simplified Tax Invoices** | B2C retail format with immediate point-of-sale QR code. | **VERIFIED LOCALLY** |
| **4** | **Standard Tax Invoices** | B2B format with buyer tax ID, itemized VAT, and clearance metadata. | **VERIFIED LOCALLY** |
| **5** | **Wizard Onboarding** | Step-by-step setup interface for company tax details and certificates. | **VERIFIED LOCALLY** |
| **6** | **Automatic ZATCA CLI Setup** | Automated integration with cryptographic signing and validation binaries. | **VERIFIED LOCALLY** |
| **7** | **Tax Exemption Reasons** | Standard ZATCA exemption codes mapped to zero-rated and exempt line items. | **VERIFIED LOCALLY** |
| **8** | **ZATCA Dashboard** | Central workspace monitoring cleared, reported, and pending invoices. | **VERIFIED LOCALLY** |
| **9** | **Embedded Invoice QR** | Dynamic runtime calculation of QR payload without database bloat. | **VERIFIED LOCALLY** |
| **10** | **Embedded Invoice XML** | Real-time XML serialization embedded directly in the invoice document. | **VERIFIED LOCALLY** |
| **11** | **Phase 1 Print Format** | Clean, official PDF layout with bilingual Arabic/English labels and QR. | **VERIFIED LOCALLY** |
| **12** | **Phase 2 Print Format** | UBL 2.1 compliant layout with cryptographic hash visual representation. | **VERIFIED LOCALLY** |
| **13** | **Resend Process** | Automated retry queue for invoices encountering network timeouts. | **VERIFIED LOCALLY** |
| **14** | **Rejection Process** | Comprehensive error parsing displaying exact ZATCA validation warnings. | **VERIFIED LOCALLY** |
| **15** | **Live & Batch Sync Modes** | Real-time transmission or automated background batch processing. | **VERIFIED LOCALLY** |
| **16** | **Multi-Company Support** | Independent tax settings and certificates for multiple sister entities. | **VERIFIED LOCALLY** |
| **17** | **Multi-Device Setup** | Support for multiple POS devices with unique cryptographic identifiers. | **VERIFIED LOCALLY** |
| **18** | **Compliance Checks Log** | Detailed audit logs for every API transmission and response payload. | **VERIFIED LOCALLY** |
| **19** | **System XML Validation** | Local XSD schema validation ensuring XML compliance before transmission. | **VERIFIED LOCALLY** |
| **20** | **ZATCA Sandbox Support** | Pre-configured developer portal endpoints for simulated test filing. | **VERIFIED LOCALLY** |

---

## 5. STEP-BY-STEP CLIENT DEMONSTRATION SCRIPT

Follow this exact 10–12 minute sequence when presenting to the client:

### Part 1: Login & System Overview (2 Minutes)
* Open browser: `http://localhost:8080` (or your Cloudflare Tunnel URL).
* Log in as `Administrator` / `admin`.
* Click search bar $\rightarrow$ Type `Company` $\rightarrow$ Open **Demo Saudi Trading Company**.
* **Say:** *"Here is our localized company configuration in Saudi Riyals (SAR) with official 15-digit Tax Identification Number 310123456700003 and localized Chart of Accounts."*

### Part 2: B2B Commercial Sales & Payment (3 Minutes)
* Search `Sales Invoice` $\rightarrow$ Open **`ACC-SINV-2026-00001`**.
* Show: Subtotal SAR 4,000.00 | VAT 15% SAR 600.00 | Total SAR 4,600.00 | Status: **Paid**.
* Click **Connections** $\rightarrow$ Show linked **Payment Entry `ACC-PAY-2026-00001`** (SAR 4,600 received in bank).
* Click **Menu (`...`)** $\rightarrow$ **View Ledger** $\rightarrow$ Show balanced postings to Debtors, Revenue, and Output VAT.
* **Say:** *"The system automates the entire B2B sales cycle, calculates VAT breakdowns, and reconciles payments into your bank account with complete audit trails."*

### Part 3: ZATCA Phase 1 QR Code Demo (3 Minutes)
* On the invoice, click the **Printer icon**.
* Select **`ZATCA Phase 1 Print Format`**.
* Ask the client to scan the QR code with their mobile phone.
* Show the decoded 5 mandatory tags (Seller Name, VAT ID, Timestamp, Total, Tax).
* **Say:** *"This QR code is generated dynamically in Base64 TLV format compliant with ZATCA Phase 1 specifications."*

### Part 4: B2C Simplified Invoicing (2 Minutes)
* Open Sales Invoice **`ACC-SINV-2026-00002`** (Saudi B2C Customer).
* Click **Print** $\rightarrow$ Show the retail simplified receipt format.
* **Say:** *"For retail stores and point-of-sale walk-ins, simplified tax invoices are issued instantly with point-of-sale QR codes."*

### Part 5: General Ledger & Tax Accounting (2 Minutes)
* Search `General Ledger` $\rightarrow$ Select `Demo Saudi Trading Company` $\rightarrow$ Click Refresh.
* Scroll to the bottom: **Total Debits = SAR 21,525.00 == Total Credits = SAR 21,525.00**.
* Search `Trial Balance` $\rightarrow$ Show `VAT 15% - DSTC` (SAR 750 Output VAT collected) vs `Input VAT 15% - DSTC` (SAR 975 Input VAT paid).
* **Say:** *"The system tracks Input VAT paid on purchases against Output VAT collected on sales, giving your accounting team an instant calculation of your tax liability or refund claim."*

---

## 6. ANSWERS TO EVERY POSSIBLE CLIENT QUESTION

* **Client Question:** *"Can we use this for multiple branches across Saudi Arabia?"*
  * **Answer:** *"Yes. ERPNext supports unlimited branches, cost centers, and warehouses with consolidated financial statements and individual branch reporting."*
* **Client Question:** *"Does this support bilingual Arabic and English?"*
  * **Answer:** *"Yes. The entire user interface and all invoice print formats support native Arabic and English side-by-side."*
* **Client Question:** *"How do we connect to our official ZATCA portal?"*
  * **Answer:** *"During onboarding, you generate a one-time OTP from your ZATCA Fatoora Portal. We input that OTP into the system settings to generate your official cryptographic certificate (CSID). After that, the system transmits invoices automatically."*
* **Client Question:** *"Where is our data stored? Can we host it in Saudi Arabia?"*
  * **Answer:** *"Yes. The system is containerized with Docker and can be hosted on your own local office server or in Saudi cloud data centers (Oracle Cloud Jeddah, AWS Middle East, or local Saudi telecom providers) to ensure 100% data sovereignty."*

---

*This concludes the master guide. You have complete mastery of the system, architecture, and sales strategy.*
