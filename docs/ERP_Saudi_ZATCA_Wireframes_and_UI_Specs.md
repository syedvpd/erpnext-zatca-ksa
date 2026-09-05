# UI Specifications & Visual Layout Wireframes
## Saudi Accounting & ZATCA ERP Suite (v15)

---

## 1. Executive Dashboard (Desk Workspace)

```
+----------------------------------------------------------------------------------------------------+
|  [LOGO] Saudi ERP   [Search DocTypes, Invoices, Reports...]   [Notifications]  [Administrator v]   |
+----------------------------------------------------------------------------------------------------+
| NAVIGATION          |  DASHBOARD OVERVIEW: Saudi Trading & Services Co.                            |
| ------------------  |  --------------------------------------------------------------------------- |
| > Accounting        |  [ SAR 11,500.00 ]     [ SAR 5,750.00 ]      [ SAR 750.00 ]   [ 100% BAL ]   |
| > ZATCA Invoicing   |  Total Revenue (MTD)   Total Expenses        Net VAT Due      GL Balance     |
| > Selling           |  --------------------------------------------------------------------------- |
| > Buying            |  QUICK ACTIONS:                                                              |
| > Stock / Inventory |  [+ New Sales Invoice]  [+ New Purchase Invoice]  [+ New Payment]  [VAT Rep] |
| > Human Resources   |  --------------------------------------------------------------------------- |
| > Reports           |  RECENT TRANSACTIONS:                                                        |
| > Settings          |  ID                  Customer / Supplier      Grand Total    Status  ZATCA   |
|                     |  --------------------------------------------------------------------------- |
|                     |  ACC-SINV-2026-00001 Al-Madinah Enterprise    SAR 11,500.00  Paid    [QR OK] |
|                     |  ACC-SINV-2026-00002 Retail Walk-in Customer  SAR  4,600.00  Subm    [QR OK] |
|                     |  ACC-PINV-2026-00001 Riyadh Industrial Supply SAR  5,750.00  Subm    [INP OK]|
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Sales Invoice Form View & ZATCA QR Generation

```
+----------------------------------------------------------------------------------------------------+
|  < Back to Invoices  |  Sales Invoice: ACC-SINV-2026-00001                   [Print] [Actions v]   |
+----------------------------------------------------------------------------------------------------+
|  STATUS: [ Submitted / Paid ]                                                                      |
|  ------------------------------------------------------------------------------------------------- |
|  Customer: [ Al-Madinah Enterprise v ]             Posting Date: [ 2026-09-05 ]                    |
|  Customer VAT: [ 310987654300003 ]                 Company: [ Saudi Trading & Services Co. ]       |
|  Invoice Type: (o) Standard (B2B)  ( ) Simplified  Currency: [ SAR ]                               |
|  ------------------------------------------------------------------------------------------------- |
|  LINE ITEMS:                                                                                       |
|  Item Code           Description               Qty    Unit Rate (SAR)   15% VAT (SAR)   Amount     |
|  ------------------------------------------------------------------------------------------------- |
|  ITM-SRV-001         Enterprise Cloud Hosting  1      10,000.00         1,500.00        11,500.00  |
|  ------------------------------------------------------------------------------------------------- |
|  TAXES & CHARGES:                                                                                  |
|  Tax Template: [ Saudi VAT 15% - STC ]                                                             |
|  Net Total: SAR 10,000.00  |  15% VAT: SAR 1,500.00  |  Grand Total: SAR 11,500.00                 |
|  ------------------------------------------------------------------------------------------------- |
|  ZATCA E-INVOICING METADATA:                                                                       |
|  [ QR Code Generated ]  Base64 TLV Length: 104 chars | Hash: 3a7f8b9... | ICV: 1 | Status: Valid   |
+----------------------------------------------------------------------------------------------------+
```

---

## 3. Bilingual Standard Tax Invoice Print Format (ZATCA Phase 1 & 2)

```
+----------------------------------------------------------------------------------------------------+
|                                    TAX INVOICE / فاتورة ضريبية                                     |
+----------------------------------------------------------------------------------------------------+
|  Saudi Trading & Services Co.                                              [ ZATCA QR CODE ]       |
|  شركة الخدمات والتجارة السعودية                                             [ 15% VAT COMPLIANT ]   |
|  VAT No / الرقم الضريبي: 310123456700003                                   [ SCANNABLE TLV ]       |
|  Riyadh, Kingdom of Saudi Arabia                                                                   |
|  ------------------------------------------------------------------------------------------------- |
|  Invoice No / رقم الفاتورة: ACC-SINV-2026-00001            Date / التاريخ: 2026-09-05              |
|  Buyer / العميل: Al-Madinah Enterprise / مؤسسة المدينة    Buyer VAT / ضريبة العميل: 310987654300003|
|  ------------------------------------------------------------------------------------------------- |
|  Item / الصنف              Qty / الكمية   Rate / السعر    VAT (15%)       Total / الإجمالي         |
|  ------------------------------------------------------------------------------------------------- |
|  Enterprise Cloud Hosting  1              SAR 10,000.00   SAR 1,500.00    SAR 11,500.00            |
|  خدمات الاستضافة السحابية                                                                          |
|  ------------------------------------------------------------------------------------------------- |
|  Total Taxable Amount / الإجمالي الخاضع للضريبة:                            SAR 10,000.00          |
|  Total VAT (15%) / مجموع ضريبة القيمة المضافة:                               SAR  1,500.00          |
|  Grand Total (with VAT) / المبلغ الإجمالي مع الضريبة:                        SAR 11,500.00          |
+----------------------------------------------------------------------------------------------------+
```
