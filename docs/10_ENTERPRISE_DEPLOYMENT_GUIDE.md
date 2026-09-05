# Enterprise Production Deployment Guide
## Saudi Accounting & ZATCA ERP Suite (v15)

---

### 1. Recommended Hosting Environments in Saudi Arabia
To ensure strict compliance with Saudi National Cybersecurity Authority (NCA) and CITC data residency mandates, deploy the stack on in-kingdom infrastructure:

1. **Oracle Cloud Infrastructure (OCI) - Saudi Cloud Region (Riyadh / Jeddah)**
2. **Amazon Web Services (AWS) - ME-Central (Riyadh)**
3. **Saudi Telecom Company (STC) Cloud / Zain Cloud / Mobily Cloud**
4. **On-Premise Private Server / Data Center** (Bare-metal Ubuntu 22.04 / 24.04 LTS)

---

### 2. Recommended Server Specifications

| Workload Tier | Concurrent Users | CPU Cores | RAM | Storage |
| :--- | :--- | :--- | :--- | :--- |
| **Small Business** | Up to 15 users | 4 vCPU | 8 GB | 80 GB SSD / NVMe |
| **Mid-Market Enterprise** | Up to 75 users | 8 vCPU | 16 GB | 160 GB SSD / NVMe |
| **High-Volume / Manufacturing** | 200+ users | 16 vCPU | 32 GB | 320 GB NVMe |

---

### 3. Quick-Deploy Script (Ubuntu 22.04/24.04 LTS)

```bash
# 1. Update system & install Docker Engine
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 2. Clone your ERP repository
git clone https://github.com/syedvpd/erpnext-zatca-ksa.git
cd erpnext-zatca-ksa

# 3. Launch the 9-container stack
docker compose up -d

# 4. Verify all 9 services are running
docker compose ps
```

---

### 4. Production Domain & SSL (HTTPS) Configuration
Map your custom corporate domain (e.g., `erp.yourcompany.com.sa`) via Nginx or Traefik with automatic Let's Encrypt SSL:

```nginx
server {
    listen 80;
    server_name erp.yourcompany.com.sa;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name erp.yourcompany.com.sa;

    ssl_certificate /etc/letsencrypt/live/erp.yourcompany.com.sa/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/erp.yourcompany.com.sa/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

### 5. Automated Backup & Disaster Recovery Schedule
Configure daily automated backups using native MariaDB dump tools scheduled in cron:

```bash
# Backup database daily at 02:00 AM
0 2 * * * docker exec $(docker ps -qf "name=db") mariadb-dump -u root -padmin 137b01d369a4 > /backups/erp_backup_$(date +\%Y\%m\%d).sql
```
