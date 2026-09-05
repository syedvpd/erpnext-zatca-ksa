# Frontend Architecture & Client Experience
## Saudi Accounting & ZATCA ERP Suite (v15)

---

## 1. Overview & Single-Page Application (SPA) Runtime
The frontend user experience is delivered through **Frappe Desk**, an enterprise single-page application framework built with modern JavaScript components, Vue.js widgets, HTML5, and customized CSS3.

---

## 2. Desk Navigation Architecture

```
+-----------------------------------------------------------------------------+
|                              FRAPPE DESK LAYOUT                             |
+-----------------------------------------------------------------------------+
| [Top Navbar]   Logo | Awesome Bar (Search Anything) | Notifications | User  |
+-----------------------------------------------------------------------------+
| [Sidebar]      | [Main Operational Canvas]                                  |
| - Accounting   |                                                            |
| - ZATCA        | - Real-Time Dashboard KPI Cards (Revenue, Receivables, VAT)|
| - Selling      | - Quick Actions (New Sales Invoice, New Payment, Print)   |
| - Buying       | - Filterable List Views with Kanban & Report views         |
| - Stock        | - Dual-Column Responsive Form Views                        |
| - Reports      | - Print Format Preview with live ZATCA QR code             |
+-----------------------------------------------------------------------------+
```

---

## 3. Bilingual RTL & LTR Parity Engine
The frontend natively supports seamless toggling between **Arabic** and **English**:

### 3.1 Arabic (RTL) Layout
- Right-to-Left CSS transformation automatically mirrors navigation bars, forms, grid columns, and data tables.
- Standard Saudi accounting terminology:
  - *Sales Invoice* -> `فاتورة المبيعات`
  - *Tax Invoice* -> `فاتورة ضريبية`
  - *Simplified Tax Invoice* -> `فاتورة ضريبية مبسطة`
  - *Customer* -> `العميل`
  - *General Ledger* -> `دفتر الأستاذ العام`
  - *Trial Balance* -> `ميزان المراجعة`

### 3.2 Dual-Language Tax Invoice Print Format
Article 53 of the Saudi VAT Implementing Regulations requires tax invoices to be bilingual. The built-in **Standard Tax Invoice** print format generates:
- Parallel Arabic and English column headers.
- Seller and Buyer corporate legal names in both languages.
- High-resolution SVG / Base64 rendered ZATCA QR code in the invoice header.
- Detailed tax breakdown table showing Net Amount, 15% VAT, and Grand Total in SAR.
