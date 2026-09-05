# COMPLETE GUIDE: ERPNext v15 + SAUDI ARABIA KSA COMPLIANCE (ZATCA)
**Everything You Need to Know From Scratch: Architecture, Files, Accounting, ZATCA, and Client Demo Preparation**

---

## TABLE OF CONTENTS
1. [What is What? (Plain English Definitions)](#1-what-is-what-plain-english-definitions)
   - [What is Frappe?](#what-is-frappe)
   - [What is ERPNext?](#what-is-erpnext)
   - [What is KSA Compliance & ZATCA?](#what-is-ksa-compliance--zatca)
   - [How Do They Fit Together?](#how-do-they-fit-together)
2. [Folder and File Anatomy (What Lives Where?)](#2-folder-and-file-anatomy-what-lives-where)
   - [Directory Structure Explained](#directory-structure-explained)
   - [Key Configuration and Code Files](#key-configuration-and-code-files)
   - [Docker Volumes (Where Your Data Lives)](#docker-volumes-where-your-data-lives)
3. [How the System Works Behind the Scenes](#3-how-the-system-works-behind-the-scenes)
   - [The 9 Docker Containers Explained](#the-9-docker-containers-explained)
   - [Network and Port Architecture](#network-and-port-architecture)
4. [How to Access and Test the Website Locally](#4-how-to-access-and-test-the-website-locally)
   - [Access Credentials and URL](#access-credentials-and-url)
   - [Understanding the ERPNext Desk Interface](#understanding-the-erpnext-desk-interface)
5. [The Saudi Business & Accounting Setup in Your Demo](#5-the-saudi-business--accounting-setup-in-your-demo)
   - [Company Details](#company-details)
   - [Master Data (Customers, Suppliers, Items)](#master-data-customers-suppliers-items)
   - [The Real Accounting Transactions Posted](#the-real-accounting-transactions-posted)
   - [General Ledger & VAT Balance Proof](#general-ledger--vat-balance-proof)
6. [ZATCA Saudi E-Invoicing Explained in Plain English](#6-zatca-saudi-e-invoicing-explained-in-plain-english)
   - [Phase 1 (Generation Phase - Dynamic QR & TLV)](#phase-1-generation-phase---dynamic-qr--tlv)
   - [Phase 2 (Integration Phase - UBL 2.1 XML & Cryptographic Chaining)](#phase-2-integration-phase---ubl-21-xml--cryptographic-chaining)
   - [What Works Locally vs What Requires Client Credentials](#what-works-locally-vs-what-requires-client-credentials)
7. [Step-by-Step Client Demo Walkthrough (10–15 Minute Script)](#7-step-by-step-client-demo-walkthrough-1015-minute-script)
   - [Preparation Checklist](#preparation-checklist)
   - [Exact Demo Click Sequence & What to Say](#exact-demo-click-sequence--what-to-say)
   - [Honest Positioning (What to Claim vs What Not to Claim)](#honest-positioning-what-to-claim-vs-what-not-to-claim)
   - [Answers to Tough Client Questions](#answers-to-tough-client-questions)
8. [Handy Management Commands (Start, Stop, Status, Backup)](#8-handy-management-commands-start-stop-status-backup)

---

## 1. WHAT IS WHAT? (PLAIN ENGLISH DEFINITIONS)

If you have never worked with Frappe, ERPNext, or ZATCA before, here is the simplest way to understand each piece:

### What is Frappe?
* **Frappe Framework** is a full-stack web application framework written in **Python** (on the backend) and **JavaScript / HTML / CSS** (on the frontend).
* Think of Frappe like Django or Ruby on Rails, but with an entire **Admin Dashboard UI ("The Desk")**, user permissions, database ORM, and workflow engine already built-in.
* In Frappe, everything is a **"DocType"** (Document Type). A DocType defines a database table, user interface form, permissions, and API endpoints all at once. For example, `Customer`, `Sales Invoice`, and `Item` are all DocTypes.

### What is ERPNext?
* **ERPNext** is a massive, open-source enterprise management suite **built on top of the Frappe Framework**.
* It provides complete business modules out of the box:
  * **Accounting:** General Ledger, Chart of Accounts, Invoicing, Payments, Tax rules, Financial Reports (P&L, Balance Sheet, Trial Balance).
  * **Buying & Selling:** Purchase Orders, Supplier Management, Quotations, Sales Orders.
  * **Stock & Inventory:** Warehouses, Serial Numbers, Batches, Stock Ledger, Automated Stock Valuation (FIFO/Moving Average).
  * **HR & Payroll, CRM, Manufacturing, Asset Management.**
* In our setup, ERPNext is configured specifically for the Kingdom of Saudi Arabia (currency: **SAR**, default tax: **15% VAT**).

### What is KSA Compliance & ZATCA?
* **ZATCA** stands for the **Zakat, Tax and Customs Authority** in Saudi Arabia (*الهيئة العامة للزكاة والضريبة والجمارك*). They regulate taxation, customs, and mandatory electronic invoicing (Fatoora).
* **KSA Compliance** is a specialized Frappe application developed by Lavaloon. It plugs into ERPNext to make it fully compliant with Saudi e-invoicing laws:
  * **Phase 1 (Enforced since Dec 2021):** Mandates that every invoice includes a QR code formatted in **Base64 TLV** containing 5 specific fields (Seller Name, VAT ID, Timestamp, Total, Tax Total) so tax inspectors or consumers can scan it.
  * **Phase 2 (Rolling out in waves since Jan 2023):** Mandates standard **UBL 2.1 XML format**, unique sequential counters (**ICV**), cryptographic hash chaining (**PIH**), digital signatures, and direct API clearance/reporting with ZATCA's servers.

### How Do They Fit Together?
Think of it like a car:
* **Frappe** is the engine, chassis, and electrical system (the underlying framework).
* **ERPNext** is the car body, seats, dashboard, and steering (the business application).
* **KSA Compliance** is the Saudi Arabian legal GPS and safety package installed into the dashboard.
* **Docker** is the secure shipping container that holds the entire car and lets it run on any computer (Windows, Mac, Linux) without altering your personal computer's settings.

---

## 2. FOLDER AND FILE ANATOMY (WHAT LIVES WHERE?)

All files for this project are located under: `C:\Users\HP\erpnext-env\`

```
C:\Users\HP\erpnext-env\
├── frappe_docker\              <-- Official Frappe Docker repository templates
├── ksa_compliance\             <-- The source code of the Saudi ZATCA Compliance app
└── erpnext-saudi-demo\         <-- THE ACTIVE RUNNING PROJECT DIRECTORY
    ├── compose.yaml            <-- Docker Compose orchestrator file (tells Docker what to run)
    ├── Dockerfile              <-- Image recipe bundling Frappe + ERPNext + KSA Compliance
    ├── ACC-SINV-2026-00001.xml <-- Generated ZATCA Phase 2 UBL 2.1 XML for B2B Invoice
    ├── ACC-SINV-2026-00002.xml <-- Generated ZATCA Phase 2 UBL 2.1 XML for B2C Invoice
    └── [verification scripts]  <-- Automated test scripts for GL, VAT, and browser checks
```

### Key Configuration and Code Files

1. **`compose.yaml`** (`C:\Users\HP\erpnext-env\erpnext-saudi-demo\compose.yaml`)
   * Defines all **9 services (containers)** needed to run ERPNext.
   * Configures port mapping: maps container port `8080` to Windows host port `8080`.
   * Maps internal network connections between Python, MariaDB, and Redis.
   * Defines **named volumes** so your database and settings are never lost when containers stop.

2. **`Dockerfile`** (`C:\Users\HP\erpnext-env\erpnext-saudi-demo\Dockerfile`)
   * Custom container build file.
   * Starts with the official base image `frappe/erpnext:v15.121.0`.
   * Automatically clones and installs `ksa_compliance` (commit `24968b4`) into the Python environment and builds its frontend JavaScript assets.
   * Results in our unified image: `erpnext-saudi-demo/erpnext-ksa:v15`.

3. **`ACC-SINV-2026-00001.xml` & `ACC-SINV-2026-00002.xml`**
   * Real, generated Saudi ZATCA Phase 2 e-invoices in **UBL 2.1 standard format**.
   * Contains the XML namespace tags, Invoice Counter Value (`<cbc:ID>`), cryptographic SHA-256 hash, and previous invoice hash chaining.

### Docker Volumes (Where Your Data Lives)
Docker volumes are persistent folders managed by Docker on your machine. Even if you turn off your computer or restart Docker, your data remains 100% safe inside:
* **`erpnext-saudi-demo_db-data`**: Contains the MariaDB database files (all ledger entries, invoices, customers, chart of accounts).
* **`erpnext-saudi-demo_sites`**: Contains the Frappe site configuration, passwords, and uploaded attachments/logos.
* **`erpnext-saudi-demo_redis-queue-data`**: Background queue data.
* **`erpnext-saudi-demo_logs`**: System and audit logs.

---

## 3. HOW THE SYSTEM WORKS BEHIND THE SCENES

### The 9 Docker Containers Explained

When you run `docker compose ps`, you see 9 containers running in unison:

| Container Name | Service | What it Does |
| :--- | :--- | :--- |
| `erpnext-saudi-demo-frontend-1` | **Frontend (NGINX)** | The web gateway. Receives your browser requests on port `8080`, serves static files (HTML/CSS/JS), and routes API requests to the backend. |
| `erpnext-saudi-demo-backend-1` | **Backend (Gunicorn)** | Python Gunicorn server running Frappe & ERPNext. Executes all business logic, tax calculations, database queries, and ZATCA XML creation. |
| `erpnext-saudi-demo-db-1` | **Database (MariaDB 11.8)** | The relational SQL database storing all business transactions, invoices, and master records. |
| `erpnext-saudi-demo-redis-cache-1` | **Redis Cache** | In-memory key-value cache used for instant page loads and caching user sessions. |
| `erpnext-saudi-demo-redis-queue-1` | **Redis Queue** | Message broker holding background tasks (e.g., email notifications, report generation, batch syncing). |
| `erpnext-saudi-demo-queue-short-1` | **Queue Worker (Short)** | Background Python process processing fast jobs (e.g., single email, status update). |
| `erpnext-saudi-demo-queue-long-1` | **Queue Worker (Long)** | Background Python process processing heavy jobs (e.g., large data exports, monthly reports). |
| `erpnext-saudi-demo-scheduler-1` | **Scheduler (Cron)** | Automated timer running scheduled jobs (e.g., daily recurring invoices, auto-reminders). |
| `erpnext-saudi-demo-websocket-1` | **Websocket (Socket.io)** | Pushes real-time updates to your browser without needing to refresh the page. |

### Network and Port Architecture
* **External Port:** Only **Port `8080`** is opened to your Windows machine (`http://localhost:8080`).
* **Database Safety:** MariaDB runs on port `3306` inside Docker's private internal virtual network. It does **not** conflict with or touch any existing MySQL/PostgreSQL databases running on your Windows host.

---

## 4. HOW TO ACCESS AND TEST THE WEBSITE LOCALLY

### Access Credentials and URL
* **URL:** Open your web browser (Chrome, Edge, Firefox) and go to:
  **`http://localhost:8080`**
* **Username:** `Administrator`
* **Password:** `admin`

### Understanding the ERPNext Desk Interface
Once logged in, you enter **The Desk**:
1. **The Awesome Bar (Top Center Search Bar):**
   * The most powerful feature in ERPNext. Press `Ctrl + K` or click the search bar.
   * Type anything you want to find: `"Sales Invoice"`, `"Company"`, `"General Ledger"`, `"Saudi B2B Customer"`, or `"ZATCA"`. Press Enter to jump straight to that screen.
2. **Left Sidebar Navigation:**
   * **Accounting:** Access Invoices, Payments, Journal Entries, Chart of Accounts, and Financial Reports.
   * **Stock:** Access Items, Warehouses, Delivery Notes, and Stock Ledger.
   * **Buying:** Suppliers, Purchase Orders, Purchase Invoices.
   * **Selling:** Customers, Quotations, Sales Orders.
3. **Workspace Dashboard:** The main area displays charts, key metrics, and shortcut cards.

---

## 5. THE SAUDI BUSINESS & ACCOUNTING SETUP IN YOUR DEMO

Everything has been configured with real, standard Saudi data so your demo is 100% authentic.

### Company Details
* **Company Name:** `Demo Saudi Trading Company`
* **Abbreviation:** `DSTC`
* **Country:** Saudi Arabia
* **Currency:** `SAR` (Saudi Riyal)
* **VAT Registration Number (TRN):** `310123456700003` (Standard 15-digit Saudi VAT ID ending in 3)
* **Default Bank Account:** `Demo Bank Account - DSTC`
* **Default Warehouse:** `Stores - DSTC`

### Master Data (Customers, Suppliers, Items)
* **Customers:**
  1. `Saudi B2B Customer`: Commercial enterprise, Tax ID `300000000000003`, registered in Riyadh.
  2. `Saudi B2C Customer`: Individual walk-in/retail consumer.
* **Suppliers:**
  * `Saudi Local Supplier`: Local VAT-registered distributor, Tax ID `310000000000003`.
* **Items in Catalog:**
  1. `Laptop`: High-value physical inventory item (Cost: 1,500 SAR | Selling Rate: 2,000 SAR | 15% VAT).
  2. `Trading Product`: Fast-moving consumer retail item (Cost: 700 SAR | Selling Rate: 1,000 SAR | 15% VAT).
  3. `Consulting Service`: Non-stock professional service (Selling Rate: 5,000 SAR | 15% VAT).

### The Real Accounting Transactions Posted

Three complete business transactions and one payment settlement have been posted into the live database:

```
[1. Purchase Invoice] -------------------> [Stores Inventory] (Stock In Hand)
Supplier: Saudi Local Supplier             Laptops + Trading Products stocked
Total: SAR 7,475 (Input VAT: SAR 975)

[2. B2B Sales Invoice] ------------------> [Payment Entry]
Customer: Saudi B2B Customer               Amount: SAR 4,600 received in Bank
Total: SAR 4,600 (Output VAT: SAR 600)     Status: Paid in Full
Status: Paid

[3. B2C Simplified Invoice] -------------> Status: Submitted (Unpaid)
Customer: Saudi B2C Customer
Total: SAR 1,150 (Output VAT: SAR 150)
```

#### Document Details:
1. **Purchase Invoice `ACC-PINV-2026-00001`:**
   * Purchased 2 Laptops @ 1,500 SAR and 5 Trading Products @ 700 SAR.
   * Net Subtotal: **SAR 6,500.00**
   * Input VAT (15%): **SAR 975.00**
   * Grand Total: **SAR 7,475.00** (Booked into Accounts Payable).
2. **B2B Sales Invoice `ACC-SINV-2026-00001`:**
   * Sold 2 Laptops @ 2,000 SAR to `Saudi B2B Customer`.
   * Net Subtotal: **SAR 4,000.00**
   * Output VAT (15%): **SAR 600.00**
   * Grand Total: **SAR 4,600.00**
   * Status: **Paid**.
3. **Payment Entry `ACC-PAY-2026-00001`:**
   * Cleared `ACC-SINV-2026-00001` in full with **SAR 4,600.00** wire transfer into `Demo Bank Account - DSTC`.
4. **B2C Simplified Sales Invoice `ACC-SINV-2026-00002`:**
   * Sold 1 Trading Product @ 1,000 SAR to `Saudi B2C Customer`.
   * Net Subtotal: **SAR 1,000.00**
   * Output VAT (15%): **SAR 150.00**
   * Grand Total: **SAR 1,150.00**
   * Status: **Submitted**.

### General Ledger & VAT Balance Proof

The system strictly follows international double-entry accounting.

* **Mathematical Ledger Balancing Check:**
  $$\text{Total Debits} = \text{SAR } 21,525.00 \quad = \quad \text{Total Credits} = \text{SAR } 21,525.00 \quad \mathbf{[BALANCED]}$$
* **VAT Position from Transactions:**
  * **Output VAT (Collected on Sales):** $600.00\text{ (B2B)} + 150.00\text{ (B2C)} = \mathbf{\text{SAR } 750.00}$ (Liability).
  * **Input VAT (Paid on Purchases):** $\mathbf{\text{SAR } 975.00}$ (Reclaimable Asset).
  * **Net VAT Payable/Refundable:** $\text{SAR } 750.00 - \text{SAR } 975.00 = \mathbf{-\text{SAR } 225.00}$. Because we made an initial inventory investment (purchased 6,500 SAR of stock, sold 5,000 SAR), our company is in a **tax credit / refund claim position** of SAR 225.00.
* **Profitability:**
  * Revenue: SAR 5,000.00
  * Cost of Goods Sold: SAR 3,700.00
  * **Gross Profit:** **SAR 1,300.00**

---

## 6. ZATCA SAUDI E-INVOICING EXPLAINED IN PLAIN ENGLISH

### Phase 1 (Generation Phase - Dynamic QR & TLV)
In Phase 1, every tax invoice must generate a QR code containing 5 specific fields encoded in **TLV (Tag-Length-Value)** format and Base64 encoded:

| Tag | Name | Description | Example from our Demo |
| :---: | :--- | :--- | :--- |
| **1** | Seller Name | Legal entity name | `Demo Saudi Trading Company` |
| **2** | VAT Registration | 15-digit Tax Identification Number | `310123456700003` |
| **3** | Timestamp | Exact date and time invoice was posted | `2026-09-05T07:14:48Z` |
| **4** | Invoice Total | Total invoice amount including VAT | `4600.00` |
| **5** | VAT Total | Total VAT amount | `600.00` |

* **How to Verify:** In ERPNext, open any Sales Invoice and click **Print**. Choose the **ZATCA Phase 1 Print Format**. Scan the QR code with any ZATCA-compliant QR scanner mobile app (or online TLV decoder). It immediately decodes these 5 tags.

### Phase 2 (Integration Phase - UBL 2.1 XML & Cryptographic Chaining)
Phase 2 connects company ERPs directly to ZATCA's Fatoora cloud platform. It requires advanced cryptographic integrity:
1. **UBL 2.1 XML File:** An international standard XML document describing every line item, VAT category code, buyer/seller address, and currency.
2. **Invoice Counter Value (ICV):** An tamper-proof sequential counter (`ICV = 1`, `ICV = 2`, etc.). No invoice can be skipped or deleted.
3. **Previous Invoice Hash (PIH):** A blockchain-like security chain. The cryptographic SHA-256 hash of Invoice #1 is embedded inside Invoice #2. If someone alters an old invoice, the whole chain breaks.
4. **SHA-256 Invoice Digest:** The cryptographic fingerprint of the invoice content.
5. **Clearance vs Reporting:**
   * **B2B Standard Invoices:** Must be sent to ZATCA for **Clearance** (API returns an approved, stamped XML) *before* the invoice is given to the customer.
   * **B2C Simplified Invoices:** The QR code is generated instantly at the point of sale, and the invoice is reported to ZATCA within 24 hours.

### What Works Locally vs What Requires Client Credentials

| E-Invoicing Feature | Status in This Demo | Explanation |
| :--- | :---: | :--- |
| **B2B Standard Invoice Generation** | **VERIFIED LOCALLY** | Working seamlessly with 15% VAT and customer TRN. |
| **B2C Simplified Invoice Generation** | **VERIFIED LOCALLY** | Working seamlessly for retail and walk-in sales. |
| **Dynamic Phase 1 QR Code (5 TLV Tags)** | **VERIFIED LOCALLY** | Generated dynamically and verified matching document values. |
| **Phase 2 UBL 2.1 XML File Generation** | **VERIFIED LOCALLY** | Full XML files generated on disk (`ACC-SINV-2026-00001.xml`). |
| **ICV Counter & PIH Hash Chaining** | **VERIFIED LOCALLY** | Sequential counting and SHA-256 hash chaining verified. |
| **CSR Configuration Generation** | **VERIFIED LOCALLY** | Ready to generate the cryptographic certificate request. |
| **ZATCA Onboarding (CSID Token)** | **REQUIRES CLIENT CREDENTIALS** | Requires an official **OTP** generated by the client from their real ZATCA Fatoora Portal for their commercial registration. |
| **Live API Transmission to ZATCA** | **REQUIRES CLIENT CREDENTIALS** | Legally and technically requires the client's official production/sandbox certificate. |

> **IMPORTANT:** Never claim to a client that you have "submitted invoices to ZATCA live on their behalf." Transmitting to ZATCA's live government servers requires their legal commercial tax authorization. Being honest about this proves you are professional, knowledgeable, and security-conscious.

---

## 7. STEP-BY-STEP CLIENT DEMO WALKTHROUGH (10–15 MINUTE SCRIPT)

Here is your exact, stress-free roadmap for presenting to the client.

### Preparation Checklist (5 Minutes Before the Call)
1. Open PowerShell and check that the containers are running:
   ```powershell
   cd C:\Users\HP\erpnext-env\erpnext-saudi-demo
   docker compose ps
   ```
   *(All 9 containers should show status `Up`).*
2. Open your web browser to: **`http://localhost:8080`**
3. Log in with `Administrator` / `admin`.
4. Keep these two browser tabs open:
   * Tab 1: The ERPNext Desk (`http://localhost:8080/app`)
   * Tab 2: General Ledger Report (`http://localhost:8080/app/query-report/General%20Ledger`)

---

### Exact Demo Click Sequence & What to Say

#### Part 1: Introduction & Saudi Localization (2 Minutes)
* **What to Click:**
  1. From the top search bar (Awesome Bar), type **`Company`** and click **Demo Saudi Trading Company**.
* **What to Say to the Client:**
  > *"Good morning/afternoon. Today I'm demonstrating our localized ERPNext v15 system configured specifically for Saudi Arabian regulatory and accounting standards. Here you can see our company setup: currency is in Saudi Riyals (SAR), localized chart of accounts, and official 15-digit VAT registration number (TRN) 310123456700003."*

#### Part 2: Master Data & Saudi 15% VAT (2 Minutes)
* **What to Click:**
  1. In the search bar, type **`Customer List`**. Show `Saudi B2B Customer` (Commercial with Tax ID) and `Saudi B2C Customer` (Individual).
  2. In the search bar, type **`Item List`**. Click on **`Laptop`** or **`Trading Product`**. Scroll to the Item Tax section showing 15% standard rate.
* **What to Say to the Client:**
  > *"The system supports full catalog management with automatic VAT categorization. We have separate workflows for B2B commercial entities with tax validation and B2C retail consumers."*

#### Part 3: Real B2B Sales Invoice & Payment Entry (3 Minutes)
* **What to Click:**
  1. In the search bar, type **`Sales Invoice`**.
  2. Open invoice **`ACC-SINV-2026-00001`**.
  3. Point out: Subtotal = SAR 4,000.00 | VAT 15% = SAR 600.00 | Grand Total = SAR 4,600.00 | Status = **Paid**.
  4. Scroll to the bottom and click on the **Connections** tab to show the linked **Payment Entry `ACC-PAY-2026-00001`**.
  5. Click **Menu (top right dots)** $\rightarrow$ **View Ledger**.
* **What to Say to the Client:**
  > *"Here is a completed B2B sales transaction. Notice how the system automatically calculates the 15% VAT breakdown and tracks payment reconciliation. When we inspect the General Ledger, we see a complete double-entry posting: Debtors, Revenue, Output VAT, and automatic Cost of Goods Sold inventory adjustments."*

#### Part 4: B2C Simplified Tax Invoice (2 Minutes)
* **What to Click:**
  1. Go back to **`Sales Invoice`** list.
  2. Open invoice **`ACC-SINV-2026-00002`** (Saudi B2C Customer, Total SAR 1,150.00).
* **What to Say to the Client:**
  > *"For point-of-sale or retail consumer transactions, the system issues Simplified Tax Invoices compliant with retail regulations, maintaining immediate QR code generation at the point of sale."*

#### Part 5: ZATCA Phase 1 QR Code Demonstration (3 Minutes)
* **What to Click:**
  1. On either sales invoice, click the **Print** icon (printer button top right).
  2. In the print format dropdown, select **ZATCA Phase 1 Print Format**.
  3. The print format displays the formatted invoice with the official ZATCA QR Code.
  4. *(Optional Pro Move)*: Open your phone camera or any QR scanner app and point it at the screen. Show that it reads:
     * Seller: *Demo Saudi Trading Company*
     * VAT Number: *310123456700003*
     * Total: *SAR 4,600.00*
     * VAT: *SAR 600.00*
* **What to Say to the Client:**
  > *"Here is our Phase 1 ZATCA implementation. The QR code is dynamically rendered from a Base64 TLV payload containing the 5 mandatory tax authority tags: Seller Name, VAT Number, exact timestamp, invoice total, and VAT amount."*

#### Part 6: ZATCA Phase 2 Technical Readiness (2 Minutes)
* **What to Say to the Client:**
  > *"For Phase 2, our backend is equipped with the full UBL 2.1 XML compilation engine. It handles sequential Invoice Counter Values (ICV), cryptographic SHA-256 invoice hashing, and Previous Invoice Hash (PIH) chaining. Once you provide your company's ZATCA Fatoora Portal OTP, the system performs the one-time CSID certificate enrollment and enables live automated clearance and reporting."*

#### Part 7: Financial & VAT Reports (2 Minutes)
* **What to Click:**
  1. In the search bar, type **`General Ledger`**.
  2. Select Company: **Demo Saudi Trading Company**. Click **Refresh**.
  3. Point out: **Total Debits = SAR 21,525.00** and **Total Credits = SAR 21,525.00** (Perfect balance).
  4. In the search bar, type **`Trial Balance`**. Show the organized Chart of Accounts.
* **What to Say to the Client:**
  > *"Finally, from an accounting and audit standpoint, our general ledger is in balance. The system automatically tracks Input VAT paid on purchases against Output VAT collected on sales, giving your financial team real-time visibility into your tax liability or refund claim."*

---

### Honest Positioning (What to Claim vs What Not to Claim)

| What You CAN Confidently Claim | What You MUST NOT Claim |
| :--- | :--- |
| **"The ERPNext system is 100% operational locally."** | *"We have already sent these invoices to your real tax account at ZATCA."* |
| **"Saudi Chart of Accounts and 15% VAT are fully automated."** | *"You don't need to do any ZATCA onboarding."* *(Every business must do an onboarding ceremony with their own CR and OTP).* |
| **"Phase 1 QR code complies with all 5 mandatory TLV tags."** | *"We generated a production certificate for your business without your involvement."* |
| **"Phase 2 UBL 2.1 XML and hash chaining are built and tested."** | |
| **"All financial reports and ledgers balance out of the box."** | |

### Answers to Tough Client Questions

* **Client Question:** *"Can this connect directly to our ZATCA Fatoora portal?"*
  * **Your Answer:** *"Yes, absolutely. The KSA Compliance application includes built-in endpoints for ZATCA's Fatoora API. As soon as you log into your ZATCA portal and generate an OTP for your branch, we input that OTP into the system to generate your official CSID security token. From that moment on, invoices are reported directly."*
* **Client Question:** *"Does this support Arabic as well as English?"*
  * **Your Answer:** *"Yes. Frappe and ERPNext support native bilingual English and Arabic out of the box. Users can switch their interface language to Arabic anytime, and invoice print formats can print both English and Arabic labels side by side."*
* **Client Question:** *"Where is our data stored? Is it in the cloud or on our servers?"*
  * **Your Answer:** *"This is completely self-hosted using Docker containers. You have 100% ownership and sovereignty over your data. It can run on your own local office server, a private data center in Riyadh, or your private cloud (e.g., Oracle Cloud Riyadh, AWS ME-Central, or Azure Saudi)."*

---

## 8. HANDY MANAGEMENT COMMANDS (START, STOP, STATUS, BACKUP)

Run all commands from PowerShell on your Windows machine in directory:
`C:\Users\HP\erpnext-env\erpnext-saudi-demo`

### Check If Everything is Running:
```powershell
cd C:\Users\HP\erpnext-env\erpnext-saudi-demo
docker compose ps
```
*(All 9 containers should show `Up` or `Up (healthy)`).*

### Stop the System Gracefully:
```powershell
cd C:\Users\HP\erpnext-env\erpnext-saudi-demo
docker compose stop
```
*(Stops the containers without losing any data).*

### Start the System Up Again:
```powershell
cd C:\Users\HP\erpnext-env\erpnext-saudi-demo
docker compose up -d
```
*(Starts all 9 services in the background. Wait ~30 seconds for the website to be available at `http://localhost:8080`).*

### Restart Just the Web Backend and Frontend:
```powershell
cd C:\Users\HP\erpnext-env\erpnext-saudi-demo
docker compose restart backend frontend
```

### View Live Backend Logs (To see transactions in real time):
```powershell
cd C:\Users\HP\erpnext-env\erpnext-saudi-demo
docker compose logs -f backend
```
*(Press `Ctrl + C` to stop watching logs).*

---

*This concludes the complete guide. You are now fully prepared to demonstrate ERPNext + ZATCA Compliance with absolute confidence.*
