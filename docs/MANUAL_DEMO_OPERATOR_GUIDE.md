# 🚀 MANUAL DEMO OPERATOR CHEAT SHEET (NO AI REQUIRED)
**Your Step-by-Step Terminal & Operational Guide to Run the Entire System Manually**

---

## 📋 PRE-DEMO CHECKLIST (5 MINUTES BEFORE THE CLIENT CALL)

### Step 1: Open PowerShell as Administrator
1. Press `Win + S`, type **PowerShell**, right-click and select **Run as Administrator**.
2. Navigate to your project folder:
   ```powershell
   cd C:\Users\HP\erpnext-env\erpnext-saudi-demo
   ```

### Step 2: Check System Status
Run this command to see if all 9 services are running:
```powershell
docker compose ps
```
* **Expected Output:** You should see 9 containers (`frontend`, `backend`, `db`, `redis-cache`, `redis-queue`, `queue-short`, `queue-long`, `scheduler`, `websocket`) with status **`Up`**.

---

## ⚡ ESSENTIAL COMMANDS REFERENCE

### 1. How to Start Everything (If system is stopped):
```powershell
cd C:\Users\HP\erpnext-env\erpnext-saudi-demo
docker compose up -d
```
*(Starts all 9 containers in the background. Wait ~30 seconds for the web server to initialize).*

### 2. How to Stop Everything (After demo is finished):
```powershell
cd C:\Users\HP\erpnext-env\erpnext-saudi-demo
docker compose stop
```
*(Gracefully shuts down containers without losing any database records or configurations).*

### 3. How to Restart the Web Server (If browser gets stuck):
```powershell
cd C:\Users\HP\erpnext-env\erpnext-saudi-demo
docker compose restart backend frontend
```

### 4. Emergency Asset Fix (If CSS ever looks unstyled):
If you ever see plain HTML without styles, run this single command:
```powershell
docker compose exec backend bash -c "rm -rf /home/frappe/frappe-bench/sites/assets/frappe /home/frappe/frappe-bench/sites/assets/erpnext /home/frappe/frappe-bench/sites/assets/ksa_compliance && cp -r /home/frappe/frappe-bench/apps/frappe/frappe/public /home/frappe/frappe-bench/sites/assets/frappe && cp -r /home/frappe/frappe-bench/apps/erpnext/erpnext/public /home/frappe/frappe-bench/sites/assets/erpnext && cp -r /home/frappe/frappe-bench/apps/ksa_compliance/ksa_compliance/public /home/frappe/frappe-bench/sites/assets/ksa_compliance && chown -R frappe:frappe /home/frappe/frappe-bench/sites/assets"
```
*(Then do `Ctrl + F5` on your browser).*

---

## 🌐 HOW TO GIVE THE CLIENT A LIVE PUBLIC LINK (100% FREE)

If the client wants to open the demo on their phone or computer during the call:

1. In PowerShell, install the free Cloudflare tool (one-time setup):
   ```powershell
   winget install --id Cloudflare.cloudflared -e
   ```
2. Start the live public tunnel:
   ```powershell
   cloudflared tunnel --url http://localhost:8080
   ```
3. Cloudflare will output a public HTTPS link:
   ```
   https://your-random-name.trycloudflare.com
   ```
4. **Copy that link and paste it into WhatsApp / Google Meet chat for the client.**
5. The client can open that link from Saudi Arabia and log in directly!

---

## 🔑 LOGIN CREDENTIALS & DEMO DATA

* **Local Web URL:** [http://localhost:8080](http://localhost:8080)
* **Username:** `Administrator`
* **Password:** `admin`

### Key Entities Already Pre-Loaded:
* **Company:** `Demo Saudi Trading Company` (Tax ID: `310123456700003`, SAR)
* **B2B Customer:** `Saudi B2B Customer` (Tax ID: `300000000000003`)
* **B2C Customer:** `Saudi B2C Customer` (Retail walk-in)
* **Supplier:** `Saudi Local Supplier` (Tax ID: `310000000000003`)
* **Items:** `Laptop` (2,000 SAR), `Trading Product` (1,000 SAR)

---

## 🎬 10-MINUTE DEMO CLICK SCRIPT (WHAT TO CLICK ON SCREEN)

| Minute | Where to Click in Browser | What to Show on Screen | What to Say to Client |
| :---: | :--- | :--- | :--- |
| **00:00** | Open `http://localhost:8080` | Log in as `Administrator` / `admin` | *"Welcome. Here is our localized ERPNext system tailored for Saudi commercial regulations."* |
| **02:00** | Top Search Bar $\rightarrow$ Type `Company` $\rightarrow$ Click `Demo Saudi Trading Company` | Country: Saudi Arabia, Currency: SAR, Tax ID: `310123456700003` | *"The company is configured with the official 15-digit Saudi VAT ID and SOCPA Chart of Accounts."* |
| **04:00** | Top Search Bar $\rightarrow$ Type `Sales Invoice` $\rightarrow$ Click `ACC-SINV-2026-00001` | Subtotal: 4,000 SAR, VAT 15%: 600 SAR, Total: 4,600 SAR, Status: **Paid** | *"Here is a completed B2B sales invoice. The 15% VAT is calculated automatically."* |
| **06:00** | Bottom of invoice $\rightarrow$ Click **Connections** $\rightarrow$ Click `ACC-PAY-2026-00001` | Payment Entry of SAR 4,600 received into Bank Account | *"The payment entry fully reconciles the invoice and updates bank balances in real time."* |
| **08:00** | Top right menu of invoice $\rightarrow$ Click **Printer icon** $\rightarrow$ Select `ZATCA Phase 1 Print Format` | **ZATCA QR Code** rendered dynamically on the printed invoice | *"Here is the Phase 1 QR code. Feel free to scan it with your phone camera right now to see the 5 tax tags."* |
| **10:00** | Top Search Bar $\rightarrow$ Type `General Ledger` $\rightarrow$ Select Company $\rightarrow$ Click Refresh | Bottom row shows **Total Debits = SAR 21,525.00 == Total Credits = SAR 21,525.00** | *"Our double-entry accounting engine is 100% balanced, with separate accounts for Input and Output VAT."* |

---

## 🛡️ CLIENT FAQ QUICK CHEAT SHEET

* **Q: "Does this support Arabic?"**  
  * **A:** *"Yes, full bilingual support in Arabic and English for both the interface and printed invoices."*
* **Q: "Can we install this on our own private server in Saudi Arabia?"**  
  * **A:** *"Yes, it is containerized with Docker and can be deployed on your local office server or any Saudi cloud provider (Oracle Cloud Jeddah, AWS, or local telecom data centers)."*
* **Q: "Can we connect it to our ZATCA Fatoora Portal for live Phase 2?"**  
  * **A:** *"Yes. During onboarding, we input the one-time OTP from your ZATCA portal to generate your official CSID security certificate, enabling automated live clearance and reporting."*
