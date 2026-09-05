# End-to-End Application Workflow Manual
## Saudi Accounting & ZATCA ERP Suite (v15)

---

## 1. Enterprise Business Cycles Overview
The system models complete commercial operations across 4 interconnected cycles:
1. **Order-to-Cash (O2C):** Revenue cycle from quotation to cash settlement.
2. **Procure-to-Pay (P2P):** Expenditure cycle from material requisition to vendor payment.
3. **Record-to-Report (R2R):** Accounting cycle from ledger postings to financial statements and VAT return.
4. **ZATCA E-Invoicing Cycle:** Regulatory cycle covering QR generation, UBL 2.1 XML serialization, and hash chaining.

---

## 2. Order-to-Cash (O2C) Detailed Workflow

```
+-----------------------------------------------------------------------------+
|                      ORDER-TO-CASH (O2C) DETAILED FLOW                      |
+-----------------------------------------------------------------------------+
|                                                                             |
|  [ 1. QUOTATION ]          -> Sales rep generates quote in SAR             |
|            |                  Customer reviews pricing & 15% VAT estimate   |
|            v                                                                |
|  [ 2. SALES ORDER ]        -> Customer confirms order                        |
|            |                  Reserve warehouse inventory & enforce credit  |
|            v                                                                |
|  [ 3. DELIVERY NOTE ]      -> Warehouse dispatches goods                    |
|            |                  Stock Ledger automatically decrements balance |
|            v                                                                |
|  [ 4. SALES INVOICE ]      -> Issue Tax Invoice / Simplified Invoice        |
|            |                  - 15% Output VAT calculated (Account 2220)    |
|            |                  - Base64 TLV QR Code generated instantly      |
|            |                  - UBL 2.1 XML generated with sequential ICV   |
|            |                  - Double-entry GL posted: Debit AR/Credit Rev |
|            v                                                                |
|  [ 5. PAYMENT RECEIPT ]    -> Customer settles balance                      |
|                               Bank / Cash account credited; AR cleared      |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 3. Procure-to-Pay (P2P) Detailed Workflow

```
+-----------------------------------------------------------------------------+
|                     PROCURE-TO-PAY (P2P) DETAILED FLOW                      |
+-----------------------------------------------------------------------------+
|                                                                             |
|  [ 1. MATERIAL REQUEST ]   -> Department requests items / replenishment     |
|            |                                                                |
|  [ 2. PURCHASE ORDER ]     -> Approved order sent to authorized supplier    |
|            |                                                                |
|  [ 3. PURCHASE RECEIPT ]   -> Warehouse inspects & receives shipment        |
|            |                  Stock Ledger incremented (FIFO valuation)     |
|            v                                                                |
|  [ 4. PURCHASE INVOICE ]   -> Vendor bill received with 15% VAT             |
|            |                  - 15% Input VAT calculated (Account 1220)     |
|            |                  - Posts GL: Debit Expense/Asset & Input VAT   |
|            |                              Credit Accounts Payable           |
|            v                                                                |
|  [ 5. PAYMENT ENTRY ]      -> Bank wire / settlement in SAR                 |
|                               Accounts Payable cleared; Cash/Bank credited  |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 4. Record-to-Report (R2R) & Saudi VAT Return Workflow
1. **Continuous Ledger Postings:** Every invoice, payment, and expense entry updates `tabGL Entry` in real time.
2. **Double-Entry Reconciliation:** The system maintains perpetual mathematical balance (`Total Debits == Total Credits`).
3. **VAT Computation:**
   - **Total Output VAT Collected:** Sum of all credits in `2220 - VAT on Sales - STC`.
   - **Total Input VAT Paid:** Sum of all debits in `1220 - VAT on Purchases - STC`.
   - **Net Tax Due to ZATCA:** Output VAT minus Input VAT.
4. **Official Return Filing:** Generates the official GAZT/ZATCA VAT Return schedule with Box 1 (Sales) and Box 7 (Purchases).
