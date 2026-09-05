# System Architecture & Multi-Tier Topology
## Saudi Accounting & ZATCA ERP Suite (v15)

---

### 1. Architectural Overview
The system follows a multi-tier, micro-orchestrated container architecture designed for high throughput, data sovereignty, and isolated operational concerns.

```mermaid
graph TB
    subgraph "Tier 1: Client & Presentation"
        Client[Desktop Web Browser / Mobile Browser]
        REST[External Third-Party APIs / POS Systems]
    end

    subgraph "Tier 2: Reverse Proxy & Gateway"
        NGINX[frontend: NGINX Container - Port 8080]
        Static[Static Compiled Assets /assets/]
    end

    subgraph "Tier 3: Application Server"
        WSGI[backend: Gunicorn WSGI Server]
        Frappe[Frappe Framework v15 Metadata Engine]
        ERP[ERPNext v15 Core Business Modules]
        KSA[KSA Compliance: ZATCA Phase 1 & 2 Engine]
    end

    subgraph "Tier 4: Background Processing Engine"
        QShort[queue-short: Fast RQ Worker]
        QLong[queue-long: Long Batch RQ Worker]
        Sched[scheduler: Cron Background Engine]
        WS[websocket: Socket.io Real-time Push]
    end

    subgraph "Tier 5: Data & In-Memory Persistence"
        MDB[(MariaDB 11.8: ACID Database)]
        RCache[(Redis Cache: In-Memory Key-Value)]
        RQueue[(Redis Queue: Background Job Broker)]
        SitesVol[(Docker Volume: Shared Sites & Assets)]
    end

    Client -->|HTTP/HTTPS :8080| NGINX
    REST -->|REST API :8080| NGINX
    NGINX -->|Direct Serve| Static
    NGINX -->|Reverse Proxy :8000| WSGI
    WSGI --> Frappe
    Frappe --> ERP
    Frappe --> KSA
    Frappe -->|Read / Write SQL| MDB
    Frappe -->|Session & Doc Cache| RCache
    Frappe -->|Enqueue Jobs| RQueue
    RQueue --> QShort
    RQueue --> QLong
    Sched -->|Trigger Tasks| Frappe
    WS -->|Realtime Notifications| Client
    WSGI --> SitesVol
    NGINX --> SitesVol
```

---

### 2. The 9 Docker Containers Explained

1. **`frontend` (Nginx):** Terminates incoming HTTP traffic on port 8080, serves compiled JS/CSS bundles directly from the shared volume, and proxies dynamic `/api/` and `/app/` calls to the Gunicorn WSGI backend.
2. **`backend` (Gunicorn/Frappe):** Runs the Python application server hosting Frappe Framework, ERPNext business logic, and the Saudi ZATCA e-invoicing engine.
3. **`db` (MariaDB 11.8):** High-performance relational database using InnoDB transactional engine, hosting the complete Saudi Chart of Accounts, General Ledger, and transaction history.
4. **`redis-cache`:** In-memory caching layer storing user authentication tokens, system configurations, and pre-compiled DocType schemas for sub-millisecond retrieval.
5. **`redis-queue`:** Message broker managing background asynchronous job queues.
6. **`queue-short`:** Dedicated worker processing sub-second asynchronous tasks (e.g., immediate invoice background validations, print rendering, single emails).
7. **`queue-long`:** Dedicated worker executing long-running batch jobs (e.g., bulk report generation, database backups, monthly payroll runs).
8. **`scheduler`:** Frappe scheduler running periodic cron jobs, automatic bank feeds, and recurring invoice automation.
9. **`websocket`:** Node.js / Socket.io server providing real-time notification push to connected browser sessions.
