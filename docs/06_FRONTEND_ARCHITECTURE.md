# Frontend Architecture & User Interface
## Saudi Accounting & ZATCA ERP Suite (v15)

---

### 1. Frontend Architecture Overview
The user interface is powered by **Frappe Desk**, an enterprise single-page application (SPA) runtime engineered with Vue.js, HTML5, CSS3, and responsive JavaScript components.

```mermaid
graph TD
    UI[Frappe Desk Enterprise UI] --> Search[Awesome Bar: Global Search & Shortcuts]
    UI --> Nav[Workspace Sidebar: Accounting, ZATCA, Buying, Selling]
    UI --> Views[Dynamic Data Views]
    UI --> Print[Print Format Engine]

    Views --> List[List View: Filters, Kanban, Gantt]
    Views --> Form[Form View: Dual-Column Responsive Grid]
    Views --> Reports[Script Reports: P&L, Balance Sheet, VAT Return]
    Views --> Dashboard[Executive Dashboard: Real-Time KPI Cards]

    Print --> Jinja[Jinja2 Server-Side Print Template]
    Print --> RTL[Arabic RTL Print Stylesheet]
    Print --> QR[Dynamic SVG / Base64 QR Code Renderer]
```

---

### 2. Bilingual Support (Arabic RTL & English LTR)
The interface supports on-the-fly switching between:
- **Arabic (العربية):** Full Right-to-Left (RTL) layout alignment, translated labels, and Saudi tax invoice terminology (فاتورة ضريبية / فاتورة ضريبية مبسطة).
- **English:** Left-to-Right (LTR) international financial layout.
- **Dual-Language Invoices:** Print formats generate bilingual invoices compliant with Article 53 of the Saudi VAT Implementing Regulations requiring bilingual tax invoices.
