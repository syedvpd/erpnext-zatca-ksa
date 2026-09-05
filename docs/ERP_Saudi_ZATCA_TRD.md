# Technical Requirements Document (TRD)
## Saudi Accounting & ZATCA ERP Suite (v15)

---

## 1. System Engineering Specifications

### 1.1 Infrastructure & Containerization Topology
The platform is packaged into 9 specialized Docker containers interconnected through an internal bridge network (`frappe_network`):

```
+-----------------------------------------------------------------------------+
|                         DOCKER SERVICE TOPOLOGY                             |
+-----------------------------------------------------------------------------+
| Service Name  | Image / Base                 | Role                         |
+---------------+------------------------------+------------------------------+
| frontend      | erpnext-zatca-ksa:latest     | Nginx 1.26 HTTP Reverse Proxy|
| backend       | erpnext-zatca-ksa:latest     | Gunicorn Python WSGI App     |
| db            | mariadb:11.8                 | InnoDB Relational Database   |
| redis-cache   | redis:7-alpine               | User Session & Schema Cache  |
| redis-queue   | redis:7-alpine               | Asynchronous Task Broker     |
| queue-short   | erpnext-zatca-ksa:latest     | Sub-Second RQ Worker         |
| queue-long    | erpnext-zatca-ksa:latest     | Heavy Batch / Report Worker  |
| scheduler     | erpnext-zatca-ksa:latest     | Periodic Cron Automation     |
| websocket     | erpnext-zatca-ksa:latest     | Real-time Socket.io Push     |
+-----------------------------------------------------------------------------+
```

### 1.2 Technology Component Matrix

| Layer | Component | Version | Technical Configuration |
| :--- | :--- | :--- | :--- |
| **Operating System** | Debian GNU/Linux | 12 (Bookworm) | Container base image with minimal attack surface |
| **Language Runtime** | CPython | 3.11.9 | Async-ready, high-speed bytecode execution |
| **Web Server** | Nginx | 1.26.x | Reverse proxy, static asset compression, SSL termination |
| **Application Server** | Gunicorn | 22.x | WSGI container running multiple sync/gevent workers |
| **Application Core** | Frappe Framework | v15.120.0 | Dynamic DocType ORM, REST API, RBAC engine |
| **Enterprise Logic** | ERPNext | v15.121.0 | Financials, Sales, Purchases, Stock, HR, Manufacturing |
| **ZATCA Module** | KSA Compliance | v0.61.4 | UBL 2.1 XML, Base64 TLV QR engine, ICV & PIH tracking |
| **Database Engine** | MariaDB | 11.8.x | ACID compliance, `utf8mb4_unicode_ci`, row-level locking |
| **Caching Layer** | Redis | 7.x | Low-latency in-memory cache for sessions and schemas |
| **Worker Queue** | Python RQ | 1.16.x | Decoupled background task processing |

---

## 2. Security Architecture & Threat Mitigation

### 2.1 Authentication & Session Management
- **Password Storage:** Hashed using **Argon2id** (memory-hard, resistant to GPU brute-force attacks).
- **Session Tokens:** Cryptographically random 64-character tokens stored in Redis with automated expiry.
- **CSRF Protection:** Double-submit cookie verification on all mutating state calls (`POST`, `PUT`, `DELETE`).
- **Rate Limiting:** IP-based and user-based throttling configured on Nginx and Frappe API endpoints to mitigate DoS and credential stuffing.

### 2.2 Data Encryption & Protection
- **In-Transit:** Mandatory TLS 1.3 encryption across all public endpoints with HSTS (HTTP Strict Transport Security) headers.
- **At-Rest:** MariaDB tablespace encryption support; Docker persistent volumes stored on encrypted host filesystems (LUKS / BitLocker).
- **API Security:** Role-Based Access Control (RBAC) enforced at the ORM layer; API keys and secrets generated with 256-bit entropy.
