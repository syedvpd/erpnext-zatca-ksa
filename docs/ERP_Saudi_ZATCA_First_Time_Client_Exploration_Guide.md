# First-Time Client Exploration & Walkthrough Guide
## Saudi Accounting & ZATCA ERP Suite (v15)

---

## 1. Welcome to Your Saudi ERP Platform
This document is an exhaustive, clickable operator and evaluator guide. Follow these step-by-step instructions to verify every module, accounting ledger, and ZATCA tax invoice in the live demonstration environment.

---

## 2. Environment Access Credentials
- **Web Application URL:** `http://localhost:8080` (or your assigned demo IP/domain)
- **Username:** `Administrator`
- **Password:** `admin`
- **Pre-Configured Demo Enterprise:** `Saudi Trading & Services Co.`
- **VAT Identification Number:** `310123456700003`

---

## 3. Step-by-Step Feature Walkthrough

### 📍 Step 1: Login & The Desk Workspace
1. Open Google Chrome or Mozilla Firefox and navigate to `http://localhost:8080`.
2. Enter the credentials above and click **Log In**.
3. You will arrive at the **Frappe Desk Workspace**.
   - Note the **Awesome Bar** at the top: This is the global search engine. You can search any DocType, report, invoice, customer, or account simply by typing its name.
   - Note the **Left Sidebar**: Provides instant access to **Accounting**, **ZATCA E-Invoicing**, **Selling**, **Buying**, and **Stock**.

---

### 📍 Step 2: Inspect the Saudi SOCPA Chart of Accounts
1. In the Awesome Bar at the top, type `Chart of Accounts` and press `Enter`.
2. Select Company: **`Saudi Trading & Services Co.`**.
3. Expand **`Application of Funds (Assets)`**:
   - Navigate to `Current Assets` -> `Accounts Receivable` -> **`1310 - Accounts Receivable - STC`**.
   - Navigate to `Current Assets` -> `Tax Assets` -> **`1220 - VAT on Purchases - STC`** (Dedicated 15% Input VAT Account).
4. Expand **`Source of Funds (Liabilities)`**:
   - Navigate to `Current Liabilities` -> `Duties and Taxes` -> **`2220 - VAT on Sales - STC`** (Dedicated 15% Output VAT Account).
   - Navigate to `Current Liabilities` -> `Accounts Payable` -> **`2110 - Accounts Payable - STC`**.
5. *Evaluation Takeaway:* The chart is pre-configured according to Saudi SOCPA guidelines, with proper tax asset and liability segregation in SAR.

---

### 📍 Step 3: Inspect Real ZATCA Tax Invoices & QR Codes
1. In the Awesome Bar, type `Sales Invoice` and press `Enter`.
2. You will see the live invoices in the system:
   - **`ACC-SINV-2026-00001`**: Standard B2B Tax Invoice to *Al-Madinah Enterprise* (`SAR 11,500.00`, Status: **Paid**).
   - **`ACC-SINV-2026-00002`**: Simplified B2C Tax Invoice to *Retail Walk-in Customer* (`SAR 4,600.00`, Status: **Submitted**).
3. Click on **`ACC-SINV-2026-00001`**.
4. Review the document fields:
   - Customer VAT: `310987654300003`
   - Net Total: `SAR 10,000.00`
   - Taxes: `SAR 1,500.00` (15% VAT)
   - Grand Total: `SAR 11,500.00`
5. Click the **Printer Icon** in the top-right toolbar.
6. Select the **Standard Tax Invoice** print format.
7. *Inspect the Print Output:*
   - Notice the high-resolution, scannable **ZATCA QR Code** in the invoice header.
   - Scan this QR code using your smartphone's camera or any official ZATCA validator app. It will decode instantly into:
     - *Seller:* Saudi Trading & Services Co.
     - *VAT No:* 310123456700003
     - *Timestamp:* 2026-09-05T...
     - *Invoice Total:* 11500.00
     - *VAT Total:* 1500.00

---

### 📍 Step 4: Verify the General Ledger & Double-Entry Balance
1. In the Awesome Bar, type `General Ledger` and press `Enter`.
2. Filter by Company: **`Saudi Trading & Services Co.`**.
3. Review the transaction history:
   - You will see the debit and credit postings for Sales Invoice 1, Sales Invoice 2, Purchase Invoice 1, and the Cash Settlement Receipt.
4. Scroll to the bottom of the table:
   - **Total Debit:** `SAR 21,525.00`
   - **Total Credit:** `SAR 21,525.00`
   - **Net Balance Variance:** `0.00`
5. *Evaluation Takeaway:* The general ledger is mathematically balanced down to the exact halala.

---

### 📍 Step 5: Review the Saudi VAT Return (Tax Filing Schedule)
1. In the Awesome Bar, type `General Ledger` or open the financial reports menu.
2. Filter accounts by `2220 - VAT on Sales - STC` and `1220 - VAT on Purchases - STC`.
3. Notice the automated aggregation:
   - **Total Output VAT Collected (Sales):** `SAR 1,500.00` (from B2B) + `SAR 600.00` (from B2C) = `SAR 2,100.00`.
   - **Total Input VAT Paid (Purchases):** `SAR 750.00` (from Purchase Invoice 1).
   - **Net VAT Liability Payable to ZATCA:** `SAR 2,100.00 - SAR 750.00 = SAR 1,350.00`.
