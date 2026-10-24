# Fake Product Identification Using Blockchain (TrustChain)

> **B.Tech. VIII SEM PROJECT (PHASE II)** — Code: `D033823(033)`  
> **Institution:** Shri Shankaracharya Institute of Professional Management & Technology (SSIPMT), Raipur  
> **Department:** Department of Information Technology (Session 2022-23)  
> **Project Members:**  
> 1. **Rahul Dewangan** (Enrollment: `BH1821`, rahul.dewangan1@ssipmt.com, +91 6264999654)  
> 2. **Chirag Gajbhiye** (Enrollment: `BH1793`, chirag.gajbhiye@ssipmt.com, +91 7898097230)  

---

## 📌 Executive Summary & Purpose

In modern global retail and e-commerce, counterfeit goods inflict severe financial losses on genuine manufacturers and expose consumers to hazardous, substandard items (e.g., duplicate medicine, electronics, designer wear).

Traditional centralized databases are vulnerable to single-point manipulation, internal tampering by corrupt actors, and forged labels. **This project resolves the counterfeit dilemma by deploying a decentralized, immutable Blockchain ledger paired with high-density cryptographic QR codes.**

### Key System Objectives:
1. **Anti-Counterfeit Architecture:** Maintain an immutable record of every genuine item from factory production to consumer purchase.
2. **Cryptographic QR Code Identification:** Each manufactured unit receives a unique SHA-256 block hash embedded in a scannable QR label.
3. **Consumer Empowerment:** Consumers can scan the packaging using any smartphone camera or webcam before purchasing to verify authenticity in real-time.
4. **Supply Chain Traceability:** Immutable handover checkpoints track the product from Manufacturer → Quality Assurance → Logistics/Depot → Retailer → Customer.
5. **Tamper-Evident Ledger:** Any attempt to inject fake serials or alter existing block records without computing Proof-of-Work breaks the cryptographic hash chain and triggers instant security alarms.

---

## 🛠️ Technology Stack

- **Backend / Blockchain Core:** Python 3 (SHA-256 Hashing, Proof-of-Work Mining, Nonce calculation, Chained validation)
- **Web Framework:** Flask (RESTful APIs and MVC routing)
- **Database / Ledger Persistence:** SQLite / SQL
- **QR Code Engine:** `qrcode` (High-density error-correcting QR generation) + Pillow
- **Frontend UI:** Modern Tailwind CSS, FontAwesome 6, HTML5-QRCode Scanner Library
- **Hardware Compatibility:** Standard Intel Core i3 / 4GB RAM or higher

---

## 🚀 Quick Start & How to Run

### 1. Prerequisites
Ensure Python 3.8+ is installed on your system.

### 2. Install Dependencies
```bash
cd "C:\Users\DELL\.gemini\antigravity\scratch\fake-product-blockchain"
pip install -r requirements.txt
```

### 3. Pre-seed Sample Genuine Data (Optional)
The project comes with a seeding script that generates sample products (Apple iPhone 15 Pro, Nike Jordan Retro, GSK Augmentin Medicine) and their QR codes:
```bash
python seed_data.py
```

### 4. Start the Application Server
```bash
python app.py
```
Open your browser and navigate to:  
👉 **`http://localhost:5000`**

---

## 🧭 System Walkthrough & Portals

### 1. Consumer Verification Portal (`/`)
- **Live Camera Scanner:** Scans product QR labels directly via webcam or smartphone camera.
- **Image Upload:** Drag-and-drop or upload saved QR image files.
- **Manual Product ID Lookup:** Enter product codes directly (e.g. `PROD-AAPL-98210`).
- **Quick Demo Sandbox:** One-click shortcuts to test genuine verified items vs unregistered counterfeit items (`FAKE-GUCCI-9999`).

### 2. Product Verification Certificate (`/verify/<product_id>`)
- Displays an official **Genuine Verification Certificate** with manufacturer details, batch code, manufacture & expiry dates.
- Interactive **Supply Chain Provenance Timeline** displaying every custodial checkpoint.
- Cryptographic Proof (Block index, Block hash, Nonce, Previous block link).
- **Print Certificate** button for consumer warranty and proof of authenticity.

### 3. Manufacturer Portal (`/manufacturer`)
- Allows authorized brands to register new genuine items into the blockchain.
- Mines a new block with Proof of Work.
- Instantly generates and allows downloading of the unique unit QR code for packaging.

### 4. Supply Chain & Logistics Portal (`/supply-chain`)
- Logistics carriers, warehouses, and retailers log checkpoints (e.g., `QUALITY_INSPECTION_PASSED`, `IN_TRANSIT_LOGISTICS`, `DISTRIBUTOR_RECEIVED`, `RETAIL_STORE_ARRIVAL`).
- Extends the blockchain with chronological custodial proof.

### 5. Blockchain Explorer & Adversarial Tamper Simulator (`/explorer`)
- Live visualization of all mined blocks and cryptographic hashes.
- **Project Defense / Viva Feature — Tamper Attack Simulator:**
  - Select any block and inject fake counterfeit data into the database.
  - The system recalculates SHA-256 hashes and immediately catches the breach, showing a **Tamper Detected** red alert!
  - Click **Re-Mine & Repair** to demonstrate how consensus and Proof of Work restore integrity.

### 6. Project Synopsis Page (`/about`)
- Academic documentation containing all specifications, proforma info, objectives, and feasibility details matching SSIPMT Raipur requirements.

---

## 🎓 Viva Voce & Defense Q&A

**Q1: How does this system detect a fake product?**  
> *A:* When a product is manufactured, its details are permanently mined into a block with a unique cryptographic hash and QR code. When a consumer scans the code:
> 1. If the Product ID does not exist in the blockchain ledger, it is instantly flagged as **Counterfeit / Fake**.
> 2. If someone copies a genuine QR code onto duplicate goods, the consumer will see the exact original product name, authorized retailer, and sold status, revealing the duplicate.
> 3. If a rogue database admin modifies product details in the database, the recalculated SHA-256 hash will not match the block header, immediately alerting the consumer of tampering.

**Q2: What is the role of the QR code?**  
> *A:* The QR code serves as the physical-to-digital bridge. It stores the product's immutable digital identity and verification URL, allowing any standard consumer smartphone camera to verify the item without needing proprietary hardware.

**Q3: Why use Blockchain instead of a standard SQL database?**  
> *A:* In a centralized SQL database, anyone with database admin credentials can alter records, forge batch numbers, or delete audit logs. In a blockchain, each block is cryptographically linked to its predecessor via SHA-256 and secured by Proof of Work. Changing a single character invalidates all subsequent block hashes.

---

## 📄 Academic Project Details
- **Institute:** Shri Shankaracharya Institute of Professional Management & Technology, Raipur
- **Branch:** Information Technology
- **Course:** B.Tech. VIII SEM (Phase II) Project
