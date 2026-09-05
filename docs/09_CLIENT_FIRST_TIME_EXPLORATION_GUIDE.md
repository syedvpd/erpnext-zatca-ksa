# Client First-Time Exploration Guide
## Saudi Accounting & ZATCA ERP Suite (v15)

---

### 1. Executive Quick Start
Welcome to your **Saudi Accounting & ZATCA ERP Suite**. This step-by-step interactive exploration guide demonstrates the platform's features from the perspective of an executive or financial auditor.

---

### 2. Login & Navigation
1. Open your browser and navigate to: **`http://localhost:8080`** (or your production server URL).
2. Enter the administrator credentials:
   - **Username:** `Administrator`
   - **Password:** `admin`
3. Upon login, you are greeted by the **Frappe Desk Workspace** showcasing real-time operational widgets.

---

### 3. 5-Minute Tour of Key Features

#### 📍 Step 1: Inspect the Saudi Chart of Accounts
- In the top search bar (Awesome Bar), type **`Chart of Accounts`** and hit `Enter`.
- Expand **Application of Funds (Assets)** -> **Current Assets** -> **Tax Assets** -> **1220 - VAT on Purchases - STC**.
- Expand **Source of Funds (Liabilities)** -> **Current Liabilities** -> **Duties and Taxes** -> **2220 - VAT on Sales - STC**.
- *Takeaway:* SOCPA-compliant, bilingual chart pre-configured in SAR.

#### 📍 Step 2: Verify ZATCA Phase 1 Invoices & QR Codes
- In the top search bar, type **`Sales Invoice`** and hit `Enter`.
- Click on **`ACC-SINV-2026-00001`** (Standard B2B Invoice to *Al-Madinah Enterprise*).
- Click the **Printer icon** in the top-right corner.
- Select the **Standard Tax Invoice** format.
- *Notice:* The dynamic ZATCA QR Code is printed clearly on the invoice header alongside the 15-digit VAT ID (`310123456700003`). Scanning this QR code with any ZATCA-compliant phone app instantly decodes the seller, tax ID, timestamp, and 15% VAT amounts.

#### 📍 Step 3: Verify the General Ledger & Double-Entry Integrity
- Type **`General Ledger`** in the Awesome Bar and hit `Enter`.
- Set Company to **`Saudi Trading & Services Co.`**.
- Scroll to the bottom of the table:
  - **Total Debit:** `SAR 21,525.00`
  - **Total Credit:** `SAR 21,525.00`
  - **Net Variance:** `0.00` (Mathematically balanced double-entry accounting).

#### 📍 Step 4: Review the Automated VAT Return
- Type **`Saudi VAT Return`** or open the **Tax & VAT Report**.
- Notice how the system aggregates:
  - **Box 1 (Standard Rated Sales):** `SAR 10,000.00` (Output VAT: `SAR 1,500.00`)
  - **Box 7 (Standard Rated Purchases):** `SAR 5,000.00` (Input VAT: `SAR 750.00`)
  - **Net VAT Due to ZATCA:** `SAR 750.00`.
