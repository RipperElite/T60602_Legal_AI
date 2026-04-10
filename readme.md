# ⚖️ LexVault: Digital Evidence & AI-Driven Tamper Detection

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Machine Learning](https://img.shields.io/badge/AI-Random_Forest-brightgreen)
![Security](https://img.shields.io/badge/Security-SHA--256_%7C_Fernet-yellow)

**LexVault** is a cryptographically secure, AI-powered digital evidence locker built to guarantee the Chain of Custody for digital files while automatically detecting image tampering and forgery.

🏆 **1st Prize Winning Project** - Built by Team **OUTLIERS** (Problem Statement ID: T60602).

---

## 🔍 Core Features

* **🔐 Cryptographic Sealing:** Automatically generates a SHA-256 digital fingerprint for uploaded evidence and mathematically locks the file in an encrypted local `/vault` using Fernet symmetric encryption.
* **🧠 AI Error Level Analysis (ELA):** Extracts hidden JPEG compression artifacts to reveal internal mathematical inconsistencies. Manipulated regions "glow" to the AI, even without the original image.
* **🤖 Random Forest Classifier:** A highly optimized machine learning model trained on the CASIA 2.0 dataset (flattened to a strict 10,000-feature grayscale array). Achieves a **95% Recall** on tampered images.
* **🕵️ EXIF Metadata Extraction:** Scans and displays hidden metadata attached to the image, catching basic software signature anomalies.
* **📋 Live Audit Ledger:** Tracks every piece of evidence processed during the session in a secure ledger.
* **📄 Court-Ready Reporting:** Generates a 1-click downloadable `.txt` report containing the Chain of Custody, Hash, and AI Forensics Verdict for legal submission.

---

## 🏗️ System Architecture

LexVault operates on a dual-track architecture:
1. **Cryptography Track:** Upload -> SHA-256 Fingerprint -> Fernet Encryption -> Secure Vault.
2. **AI Forensics Track:** Upload -> Error Level Analysis -> Pre-process (100x100 Grayscale) -> Random Forest ML Predictor -> Authentic/Tampered Verdict.

---

## 🚀 Installation & Setup

### Prerequisites
* Python 3.8 or higher installed on your machine.
* Git installed.

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/LexVault-Digital-Forensics.git](https://github.com/yourusername/LexVault-Digital-Forensics.git)
cd LexVault-Digital-Forensics

2. Install Dependencies
It is highly recommended to use a virtual environment. - pip install -r requirements.txt

3.Run application - streamlit run app.py

🖥️ Usage Guide
Upload Evidence: Drag and drop a digital image (.jpg, .jpeg, .png) into the dashboard.

Generate Hash & Encrypt: Click "Encrypt & Store in Vault" to generate the SHA-256 fingerprint and mathematically lock the file.

Analyze Tampering: The AI will automatically process the image and output an AUTHENTIC or TAMPERED verdict with a confidence score.

View ELA Map: Scroll down to see the Error Level Analysis visual map proving the consistency of the image.

Generate Report: Click "Download Court-Ready Report" to export the final audit log.