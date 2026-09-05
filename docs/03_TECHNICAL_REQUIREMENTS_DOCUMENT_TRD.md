# Technical Requirements Document (TRD)
## Saudi Accounting & ZATCA ERP Suite (v15)

---

### 1. Technology Stack Specification

| Component Layer | Technology / Package | Version | Justification |
| :--- | :--- | :--- | :--- |
| **Base OS / Kernel** | Debian Bookworm (Containerized) | 12.x | Stable enterprise Linux runtime |
| **Language Runtime** | Python (CPython) | 3.11.x | Standard runtime for Frappe & ERPNext v15 |
| **Web Server / Proxy** | Nginx | 1.26.x | Reverse proxy, static asset cache, SSL offloader |
| **WSGI Server** | Gunicorn (gevent/sync workers) | 22.x | High-throughput asynchronous HTTP process manager |
| **Application Core** | Frappe Framework | v15.120.0 | Python metadata engine, ORM, REST API, RBAC |
| **ERP Logic Engine** | ERPNext | v15.121.0 | Complete financial, sales, buying, and stock modules |
| **Compliance Module**| KSA Compliance (LavaLoon) | v0.61.4 | ZATCA Phase 1 QR generator and Phase 2 UBL XML |
| **Database Engine** | MariaDB | 11.8.x | ACID-compliant relational DB with InnoDB row locking |
| **Cache Broker** | Redis | 7.x | In-memory key-value cache for user sessions and DocTypes |
| **Worker Queue** | Python RQ (Redis Queue) | 1.16.x | Background task processing (invoicing, emails, reports)|
| **Job Scheduler** | Frappe Scheduler (Cron daemon) | Built-in | Periodic reconciliations, recurring invoices, backups |

---

### 2. Communication Protocols & Ports

```
[ Client Browser ] 
        |  HTTP / HTTPS (Port 8080 / 443)
        v
[ frontend (Nginx) ]
        |  Proxy Pass (Port 8000)
        v
[ backend (Gunicorn WSGI) ]
   |                  |
   | SQL (Port 3306)  | Redis Protocol (Port 6379)
   v                  v
[ db (MariaDB) ]   [ redis-cache / redis-queue ]
```

---

### 3. Data Storage & Persistence Volumes
All critical enterprise data is mapped to external Docker named volumes to ensure zero data loss across container recreations:

| Volume Name | Mount Path | Purpose |
| :--- | :--- | :--- |
| `sites` | `/home/frappe/frappe-bench/sites` | Multi-tenant site configs, uploaded attachments, public files |
| `db-data` | `/var/lib/mysql` | MariaDB tables, InnoDB log files, transaction logs |
| `redis-cache-data`| `/data` | Redis snapshot persistence |
| `redis-queue-data`| `/data` | Background job state persistence |
