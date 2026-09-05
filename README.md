# Saudi Accounting & ZATCA ERP Suite (v15)

[![ERPNext Version](https://img.shields.io/badge/ERPNext-v15.121.0-blue.svg)](https://github.com/frappe/erpnext)
[![Frappe Framework](https://img.shields.io/badge/Frappe-v15.120.0-orange.svg)](https://github.com/frappe/frappe)
[![ZATCA Compliance](https://img.shields.io/badge/ZATCA-Phase%201%20%26%20Phase%202-green.svg)](https://zatca.gov.sa)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Integrated & Packaged by](https://img.shields.io/badge/Integrated%20by-SYED%20ZUBAIR-purple.svg)](https://github.com/syedvpd/erpnext-zatca-ksa)

A self-hosted, enterprise-grade **ERPNext v15** distribution engineered for businesses operating in the **Kingdom of Saudi Arabia (KSA)**. Features native localization, automated **15% VAT**, a pre-configured Saudi Chart of Accounts, and a complete implementation of **ZATCA (Fatoora) E-Invoicing (Phase 1 Generation & Phase 2 Integration)**.

---

## Architecture Overview

This suite orchestrates a production-ready Frappe/ERPNext multi-container topology using Docker Compose, bundling all required core services, in-memory caches, background workers, and persistent database volumes:

```
                          [ Client Web Browser / Mobile ]
                                         │
                                   Port 8080 (HTTP)
                                         ▼
                            ┌────────────────────────┐
                            │    frontend (NGINX)    │
                            └────────────┬───────────┘
                                         │ Internal Proxy
                                         ▼
                            ┌────────────────────────┐
                            │    backend (Gunicorn)  │
                            │   Frappe v15 + ERPNext │
                            │     + KSA Compliance   │
                            └───────┬────────┬───────┘
                 Internal SQL       │        │ Redis Cache / Queue
                                    ▼        ▼
┌────────────────────────┐    ┌───────────┐    ┌────────────────────────┐
│  db (MariaDB 11.8)     │◄───┤  Storage  ├───►│  redis-cache / queue   │
│  erpnext-saudi-demo    │    │  Volumes  │    │  In-Memory Broker      │
└────────────────────────┘    └───────────┘    └───────────┬────────────┘
                                                           │
                                   ┌───────────────────────┴───────────────────────┐
                                   │                       │                       │
                                   ▼                       ▼                       ▼
                         ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
                         │   queue-short    │    │    queue-long    │    │    scheduler     │
                         │ (Fast RQ Worker) │    │ (Batch RQ Worker)│    │  (Cron Engine)   │
                         └──────────────────┘    └──────────────────┘    └──────────────────┘
```

---

## Key Features

### 1. Saudi Arabian Localization
* **Standard Saudi Chart of Accounts:** Automated categorization for Assets, Liabilities, Equity, Revenue, and Expenses in accordance with SOCPA and Saudi commercial law.
* **15% Value Added Tax (VAT):** Automated tax calculations, tax splitting, and dedicated GL accounts for `VAT 15%` (Output Tax Liability) and `Input VAT 15%` (Input Tax Asset).
* **B2B & B2C Workflows:** Built-in customer separation for commercial entities (with 15-digit Tax Identification Numbers) and individual retail walk-in consumers.

### 2. ZATCA E-Invoicing Compliance Engine
* **Phase 1 (Generation Phase):**
  * Dynamic generation of **Base64 TLV (Tag-Length-Value)** QR codes.
  * Verified extraction of all 5 mandatory ZATCA tags:
    1. Seller Name (`Demo Saudi Trading Company`)
    2. VAT Registration Number (`310123456700003`)
    3. Invoice Timestamp (`YYYY-MM-DDTHH:MM:SSZ`)
    4. Invoice Total with Tax
    5. Total VAT Amount
* **Phase 2 (Integration Phase):**
  * **UBL 2.1 Standard XML Generation:** Compliant with ZATCA electronic invoice data dictionaries.
  * **Invoice Counter Value (ICV):** Tamper-proof sequential counter (`ICV = 1`, `ICV = 2`, etc.).
  * **Previous Invoice Hash (PIH) Chaining:** Cryptographic SHA-256 blockchain-style chaining linking each invoice to its predecessor.
  * **Cryptographic Hashing:** Generates base64 SHA-256 invoice digests for digital signature embedding.
  * **Clearance & Reporting Architecture:** Supports Standard B2B clearance and Simplified B2C 24-hour reporting workflows.

---

## Project Structure

```
.
├── compose.yaml                  # Multi-container production Docker Compose stack
├── Dockerfile                    # Image build recipe bundling ERPNext + KSA Compliance
├── LICENSE                       # MIT License
├── README.md                     # Project documentation
├── docs/                         # Detailed guides and compliance specifications
│   └── COMPLETE_SYSTEM_GUIDE.md  # Comprehensive start-to-finish technical & demo guide
├── samples/                      # Verified ZATCA Phase 2 UBL 2.1 XML output files
│   ├── ACC-SINV-2026-00001.xml   # Standard B2B E-Invoice XML
│   └── ACC-SINV-2026-00002.xml   # Simplified B2C E-Invoice XML
└── scripts/                      # Automated seeding, verification, and audit tools
    ├── 02_seed_master_data.py    # Master data provisioning (Customers, Suppliers, Items)
    ├── 03_execute_transactions.py# Automated real transaction execution
    ├── 04_verify_accounting.py   # Double-entry GL balance and VAT register verification
    ├── 05_verify_zatca_phase1_qr.py # Base64 TLV QR tag verification
    ├── 06_verify_zatca_phase2_xml.py# UBL 2.1 XML, ICV, and PIH chaining audit
    └── 07_test_browser_endpoints.py # Automated HTTP 200 endpoint crawler test
```

---

## Quick Start

### 1. Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (v24+ with WSL2 backend on Windows or native Linux Docker)
* Docker Compose v2.20+
* Minimum 8GB RAM allocated to Docker

### 2. Launch the Environment
```bash
# Clone the repository
git clone https://github.com/syedvpd/erpnext-zatca-ksa.git
cd erpnext-zatca-ksa

# Launch all 9 containers in detached mode
docker compose up -d
```

### 3. Access the System
Open your browser and navigate to:
* **URL:** `http://localhost:8080`
* **Username:** `Administrator`
* **Password:** `admin`

---

## Verified Accounting & Tax Audit Results

All transactions have been posted and verified against the live double-entry general ledger:

| Transaction ID | Document Type | Entity | Net Amount | VAT (15%) | Total | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ACC-PINV-2026-00001` | Purchase Invoice | Saudi Local Supplier | SAR 6,500.00 | SAR 975.00 | SAR 7,475.00 | Submitted (Unpaid) |
| `ACC-SINV-2026-00001` | Standard Sales Invoice | Saudi B2B Customer | SAR 4,000.00 | SAR 600.00 | SAR 4,600.00 | Paid |
| `ACC-PAY-2026-00001` | Payment Entry | Demo Bank Account | SAR 4,600.00 | - | SAR 4,600.00 | Submitted (Reconciled)|
| `ACC-SINV-2026-00002` | Simplified Sales Invoice| Saudi B2C Customer | SAR 1,000.00 | SAR 150.00 | SAR 1,150.00 | Submitted (Unpaid) |

### Mathematical Ledger Balance Proof
$$\sum \text{Debits} = \text{SAR } 21,525.00 \quad \equiv \quad \sum \text{Credits} = \text{SAR } 21,525.00 \quad \mathbf{[PASS]}$$

* **Output VAT Collected (Sales):** SAR 750.00
* **Input VAT Paid (Purchases):** SAR 975.00
* **Net VAT Position:** SAR -225.00 (Tax Credit / Refund Claim Position)
* **Gross Profit:** SAR 1,300.00 (Revenue: SAR 5,000.00 - COGS: SAR 3,700.00)

---

## Verification & Audit Scripts

Execute automated system verification directly inside the running container:

```bash
# Verify double-entry GL balance and trial balance
docker compose exec -T backend /home/frappe/frappe-bench/env/bin/python /workspace/scripts/04_verify_accounting.py

# Verify ZATCA Phase 1 QR TLV tags
docker compose exec -T backend /home/frappe/frappe-bench/env/bin/python /workspace/scripts/05_verify_zatca_phase1_qr.py

# Verify ZATCA Phase 2 UBL 2.1 XML and hash chaining
docker compose exec -T backend /home/frappe/frappe-bench/env/bin/python /workspace/scripts/06_verify_zatca_phase2_xml.py
```

---

## ZATCA Onboarding & Deployment Readiness

| Capability | Local Verification | Client / Production Requirement |
| :--- | :---: | :--- |
| **B2B Standard Invoicing** | **Verified** | Ready for operational billing |
| **B2C Simplified Invoicing** | **Verified** | Ready for retail / POS billing |
| **Phase 1 Dynamic QR Code (5 TLV Tags)**| **Verified** | 100% locally generated and verified |
| **Phase 2 UBL 2.1 XML Generation** | **Verified** | Validated against ZATCA schema |
| **Tamper-Proof ICV & PIH Chaining** | **Verified** | Sequential counter & SHA-256 chaining |
| **ZATCA Portal CSID Onboarding** | *Ready for Input* | Requires official OTP from client's ZATCA portal |
| **Live Production API Transmission** | *Ready for Input* | Requires client's registered cryptographic certificate |

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author & Maintainer

**SYED ZUBAIR**  
GitHub: [@syedvpd](https://github.com/syedvpd)  
Email: zubairkhadri123@gmail.com

---

---

---

---

## 📚 Enterprise Platform Documentation

A comprehensive, institutional-grade engineering and business documentation suite is available in the [`docs/`](docs/) directory:

1. [**Product Requirements Document (PRD)**](docs/01_PRODUCT_REQUIREMENTS_DOCUMENT_PRD.md) — Strategic vision, user personas (CFO, Chief Accountant, Sales Manager), functional scope, and acceptance criteria.
2. [**Software Requirements Specification (SRS)**](docs/02_SOFTWARE_REQUIREMENTS_SPECIFICATION_SRS.md) — ZATCA Phase 1 (TLV QR) and Phase 2 (UBL 2.1 XML / ICV / PIH) regulatory specifications and use cases.
3. [**Technical Requirements Document (TRD)**](docs/03_TECHNICAL_REQUIREMENTS_DOCUMENT_TRD.md) — Full technology stack, Python 3.11, MariaDB 11.8, Gunicorn, Redis, and port architecture.
4. [**System Architecture & Multi-Tier Topology**](docs/04_SYSTEM_ARCHITECTURE_AND_LAYERS.md) — 5-tier architectural blueprint explaining the 9-container micro-topology.
5. [**Backend Architecture & Execution Flow**](docs/05_BACKEND_ARCHITECTURE.md) — Request lifecycle, Frappe DocType ORM, Hook system, and transaction boundaries.
6. [**Frontend Architecture & UI**](docs/06_FRONTEND_ARCHITECTURE.md) — Frappe Desk SPA, Awesome Bar, Jinja2 print formats, and Arabic (RTL) / English bilingual support.
7. [**Database Architecture & ERD**](docs/07_DATABASE_ARCHITECTURE_AND_ERD.md) — MariaDB 11.8 InnoDB schema, Mermaid ERD diagrams, and live GL balance audit.
8. [**Business Workflows & Flowcharts**](docs/08_BUSINESS_WORKFLOWS_AND_MODULE_FLOWCHARTS.md) — End-to-end Order-to-Cash (O2C), Procure-to-Pay (P2P), and ZATCA Phase 2 Clearance/Reporting flowcharts.
9. [**Client First-Time Exploration Guide**](docs/09_CLIENT_FIRST_TIME_EXPLORATION_GUIDE.md) — 5-minute interactive onboarding walkthrough for clients and evaluators.
10. [**Enterprise Production Deployment Guide**](docs/10_ENTERPRISE_DEPLOYMENT_GUIDE.md) — Production hosting in Saudi cloud regions (Oracle Cloud, AWS Riyadh, STC Cloud), Let's Encrypt SSL, and automated backups.

---

## License & Open-Source Attribution

This integrated suite is distributed under a multi-license model respecting all upstream open-source authors and projects:

- **Custom Integration, Docker Orchestration, Automation Scripts & Tooling**: [MIT License](LICENSE) (c) 2026 SYED ZUBAIR.
- **Core ERP & Financial Accounting Engine**: [ERPNext](https://github.com/frappe/erpnext) - Licensed under GNU General Public License v3.0 (GPLv3) by Frappe Technologies Pvt. Ltd. and contributors.
- **Underlying Web & Metadata Framework**: [Frappe Framework](https://github.com/frappe/frappe) - Licensed under MIT License by Frappe Technologies Pvt. Ltd.
- **Saudi Regulatory & ZATCA Compliance Module**: [KSA Compliance](https://github.com/Lavaloon/ksa_compliance) - Licensed under GNU Affero General Public License v3.0 (AGPLv3) by LavaLoon and contributors.
- **Docker Compose & Container Topology Templates**: [Frappe Docker](https://github.com/frappe/frappe_docker) - Licensed under MIT License by Frappe Technologies Pvt. Ltd.

All trademarks, logos, and brand names are the property of their respective owners.