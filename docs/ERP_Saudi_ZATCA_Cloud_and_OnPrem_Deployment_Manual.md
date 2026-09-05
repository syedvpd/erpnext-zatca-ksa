# Enterprise Cloud & On-Premise Deployment Manual
## Saudi Accounting & ZATCA ERP Suite (v15)

---

## 1. Hosting Architecture & Data Sovereignty Mandate
Under the regulations of the **Communications, Space & Technology Commission (CST / CITC)** and the **National Cybersecurity Authority (NCA)** of Saudi Arabia, government contractors and regulated commercial enterprises must ensure financial and tax records reside on servers physically located inside the Kingdom.

### Recommended In-Kingdom Cloud Providers:
1. **Oracle Cloud Infrastructure (OCI) - Saudi Arabia Cloud Region** (Riyadh & Jeddah)
2. **Amazon Web Services (AWS) - Middle East (Central) Region** (Riyadh)
3. **Saudi Telecom Company (STC) Bluvalt Cloud**
4. **Zain Cloud / Mobily Cloud Infrastructure**
5. **Private On-Premise Data Center** (Bare-metal server running Ubuntu 22.04 / 24.04 LTS)

---

## 2. Hardware & Infrastructure Sizing Matrix

| Deployment Tier | Max Users | vCPU | RAM | NVMe SSD | Network Bandwidth |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Starter (SME)** | 1 - 25 users | 4 Cores | 8 GB | 100 GB | 100 Mbps |
| **Growth (Mid-Market)** | 25 - 100 users | 8 Cores | 16 GB | 250 GB | 250 Mbps |
| **Enterprise (High Volume)** | 100 - 500+ users | 16 Cores | 32 GB | 500 GB | 1 Gbps |

---

## 3. Production Deployment from Scratch (Step-by-Step)

### Step 1: Base Operating System Preparation (Ubuntu 22.04 / 24.04 LTS)
```bash
# Update server packages
sudo apt update && sudo apt upgrade -y

# Install essential administrative tools
sudo apt install -y curl git ufw fail2ban htop unzip

# Install Docker Engine & Docker Compose Plugin
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

### Step 2: Configure System Firewall (UFW)
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP Let's Encrypt
sudo ufw allow 443/tcp   # HTTPS Production
sudo ufw allow 8080/tcp  # ERP Direct Web Port
sudo ufw enable
```

### Step 3: Clone the Repository & Launch Containers
```bash
# Clone the verified repository
git clone https://github.com/syedvpd/erpnext-zatca-ksa.git
cd erpnext-zatca-ksa

# Launch all 9 microservices in detached mode
docker compose up -d

# Verify container operational health
docker compose ps
```

---

## 4. Production Domain & SSL (HTTPS) Configuration
To map your custom domain (e.g., `erp.saudienterprise.com.sa`) with free automatic SSL from Let's Encrypt:

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL Certificate
sudo certbot certonly --standalone -d erp.saudienterprise.com.sa
```

Configure Nginx reverse proxy in `/etc/nginx/sites-available/erp.conf`:
```nginx
server {
    listen 80;
    server_name erp.saudienterprise.com.sa;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name erp.saudienterprise.com.sa;

    ssl_certificate /etc/letsencrypt/live/erp.saudienterprise.com.sa/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/erp.saudienterprise.com.sa/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

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

## 5. Automated Daily Backup & Disaster Recovery
Set up automated nightly database backups via crontab:

```bash
# Open crontab editor
crontab -e

# Add nightly backup at 02:00 AM AST
0 2 * * * docker exec $(docker ps -qf "name=db") mariadb-dump -u root -padmin 137b01d369a4 | gzip > /var/backups/erp_saudi_$(date +\%Y\%m\%d).sql.gz
```
