import pandas as pd
from datetime import datetime
import streamlit as st
import joblib
import numpy as np
import os
from PIL import Image
from evidence_security import generate_sha256, encrypt_file, initialize_key, get_ela_image

# Initialize Session State for the Audit Log
if 'audit_trail' not in st.session_state:
    st.session_state.audit_trail = []

# 1. UI Setup
st.set_page_config(page_title="Legal AI Evidence Vault", layout="wide")
st.title("LexVault: cryptographically secure, AI-powered digital evidence locker")

# 2. Safely Load the Model and Key
@st.cache_resource
def load_ai_model():
    try:
        return joblib.load('tampering_model.pkl')
    except Exception as e:
        return None

model = load_ai_model()
key = initialize_key()



# 3. Bulletproof Prediction Logic
def predict_tampering(img_path):
    if model is None:
        return "MODEL NOT LOADED (Check .pkl file)", 0.0
    try:
        ela_img = get_ela_image(img_path)
        ela_img = ela_img.resize((100, 100)).convert('L')
        ela_flat = np.array(ela_img).flatten().reshape(1, -1)
        
        prediction = model.predict(ela_flat)[0]
        confidence = model.predict_proba(ela_flat).max()
        
        label = "TAMPERED" if prediction == 1 else "AUTHENTIC"
        return label, confidence
    except Exception as e:
        return f"ERROR: {str(e)}", 0.0

# 4. The Dashboard
st.write("Upload digital evidence to verify integrity, check for AI tampering, and securely lock the file.")
uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Save the upload safely to the disk so PIL and hashlib can read it
    temp_path = "temp_upload.jpg"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Evidence")
        st.image(uploaded_file, use_column_width=True)
        
        # Objective 2: Fingerprint
        file_hash = generate_sha256(temp_path)
        st.info(f"**SHA-256 Fingerprint:**\n\n`{file_hash}`")
        
        # Objective 1: Vault Encryption
        if st.button("🔒 Encrypt & Store in Vault"):
            encrypt_file(temp_path, key)
            st.success("Evidence mathematically locked in /vault directory!")

    with col2:
        st.subheader("AI Tampering Analysis")
        
        # Objective 3: ML Prediction
        label, confidence = predict_tampering(temp_path)

        # Log the evidence to the system
        if st.button("💾 Log Evidence to System Ledger"):
            st.session_state.audit_trail.append({
                "Timestamp": datetime.now().strftime("%H:%M:%S"),
                "File Name": uploaded_file.name,
                "Hash (Truncated)": file_hash[:12] + "...",
                "AI Verdict": label,
                "Confidence": f"{confidence*100:.1f}%"
            })
            st.success("Logged to ledger!")
        
        if label == "AUTHENTIC":
            st.success(f"✅ **{label}** (AI Confidence: {confidence*100:.1f}%)")
        elif label == "TAMPERED":
            st.error(f"🚨 **{label}** (AI Confidence: {confidence*100:.1f}%)")
        else:
            st.warning(label) # Prints exactly what went wrong if it fails
            
        # Display the ELA map so judges can see the "Proof"
        try:
            st.image(get_ela_image(temp_path), caption="Error Level Analysis (ELA) Map", use_column_width=True)
        except:
            st.write("Could not generate ELA visual.")

        # --- PASTE THE NEW EXIF CODE HERE ---
        from evidence_security import extract_metadata
        st.divider() # Adds a nice visual line
        with st.expander("🔍 View Hidden Metadata (EXIF)"):
            st.json(extract_metadata(temp_path))

        st.divider()
        st.subheader("📄 Generate Official Report")
        
        report_content = f"""
        ========================================
        DIGITAL EVIDENCE INTEGRITY REPORT
        ========================================
        Team: Gradient Dissent
        Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        [ CHAIN OF CUSTODY ]
        Original File Name: {uploaded_file.name}
        SHA-256 Fingerprint: {file_hash}
        
        [ FORENSIC AI ANALYSIS ]
        Final Verdict: {label}
        AI Confidence Score: {confidence*100:.1f}%
        ========================================
        """
        
        st.download_button(
            label="⬇️ Download Court-Ready Report (.txt)",
            data=report_content,
            file_name=f"evidence_report.txt",
            mime="text/plain"
        )
        
        # --- THE AUDIT TRAIL TABLE ---
        st.divider()
        st.subheader("📋 Session Audit Ledger")
        if st.session_state.audit_trail:
            st.dataframe(pd.DataFrame(st.session_state.audit_trail), use_container_width=True)
else:
    st.info("No evidence processed in this session yet.")


