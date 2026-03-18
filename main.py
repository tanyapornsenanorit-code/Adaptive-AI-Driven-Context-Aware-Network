import streamlit as st
import pandas as pd
import time
import random

# --- ตั้งค่าหน้าจอ ---
st.set_page_config(page_title="AI Network & Privacy Dashboard", layout="wide")

st.title("🧠 Adaptive AI Network & Privacy Control Center")
st.markdown("ระบบจำลองเครือข่ายอัจฉริยะพร้อมการวิเคราะห์บริบทแบบ Real-time (Sprint 4: Optimization Logic)")

# --- 1. Sidebar: การตั้งค่าระบบ ---
st.sidebar.header("🛠 การตั้งค่าระบบ")
scenario = st.sidebar.selectbox("เลือกสถานการณ์ (Scenario)", ["Smart Campus", "Smart Stadium", "Emergency"])
is_manual = st.sidebar.checkbox("ปิดระบบ AI (Manual Mode)")

st.sidebar.markdown("---")
st.sidebar.header("🔐 Security & Privacy")
is_anonymized = st.sidebar.toggle("เปิดโหมดปกปิดตัวตน (Anonymization ON)")

# --- 2. Logic สำหรับการปกปิดตัวตน (Privacy) ---
def process_user_name(name, active):
    if active:
        return "🛡️ Hidden_User_" + str(random.randint(100, 999))
    return name

mock_users = ["User_Alice", "User_Bob", "User_Charlie", "User_David", "User_Eve"]

# --- 3. Improved Adaptive AI Logic (Context-Aware Optimization) ---
def calculate_ai_decision(users, scenario):
    # กำหนดค่าคงที่ตามบริบท (Contextual Constraints)
    if scenario == "Emergency":
        priority_weight = 2.5  
        capacity_threshold = 200 
    elif scenario == "Smart Stadium":
        priority_weight = 1.2  
        capacity_threshold = 1000 
    else: # Smart Campus
        priority_weight = 1.0  
        capacity_threshold = 500 

    # คำนวณ Load Ratio
    load_ratio = users / capacity_threshold
    
    # Adaptive Bandwidth Formula: Base * Load * Priority
    base_bw = 150 
    allocated_bw = int(base_bw * load_ratio * priority_weight)
    
    # กำหนดขอบเขตความปลอดภัย (Optimization Boundaries)
    allocated_bw = max(100, min(allocated_bw, 1500))

    # จำลองค่าดั้งเดิม (Baseline) เพื่อใช้เปรียบเทียบ
    baseline_bw = int(base_bw * priority_weight) * 2

    # วิเคราะห์สถานะและเหตุผลของ AI (XAI)
    if scenario == "Emergency":
        status = "🚨 CRITICAL"
        reason = f"AI มอบลำดับความสำคัญสูงสุด จัดสรร Bandwidth {allocated_bw} Mbps"
    elif load_ratio > 0.85:
        status = "🔥 HIGH LOAD"
        reason = f"AI ตรวจพบความหนาแน่น {int(load_ratio*100)}% จึงขยายช่องสัญญาณเพื่อลด Latency"
    else:
        status = "✅ OPTIMIZED"
        reason = "AI อยู่ในโหมดประหยัดพลังงาน จัดสรรทรัพยากรตามปริมาณการใช้งานจริง"
        
    return status, reason, allocated_bw, baseline_bw

# --- 4. การแสดงผลแบบ Real-time ---
if 'data_list' not in st.session_state:
    st.session_state.data_list = []

placeholder = st.empty()

# วนลูปจำลองการทำงานของเครือข่าย
for i in range(100):
    with placeholder.container():
        # สุ่มจำนวนผู้ใช้ตาม Scenario
        if scenario == "Smart Stadium":
            current_user_count = random.randint(400, 1200)
        elif scenario == "Emergency":
            current_user_count = random.randint(50, 150)
        else:
            current_user_count = random.randint(20, 450)

        # เรียกใช้ AI Logic
        status, ai_reason, bw, baseline = calculate_ai_decision(current_user_count, scenario)
        
        if is_manual:
            ai_reason = "⚠️ Manual Override: ระบบ AI ถูกปิดการทำงานโดยผู้ดูแล"

        # --- ส่วนแสดง Metrics ---
        c1, c2, c3 = st.columns(3)
        c1.metric("จำนวนผู้ใช้ขณะนี้", f"{current_user_count} User", delta=None)
        c2.metric("Bandwidth ที่จัดสรร", f"{bw} Mbps", delta=f"{status}")
        c3.metric("Privacy Mode", "🔒 Protected" if is_anonymized else "🔓 Public")

        st.info(f"**AI Reasoning:** {ai_reason}")

        # --- ส่วนกราฟเปรียบเทียบ (Bandwidth Optimization Chart) ---
        st.subheader("📊 Network Bandwidth Optimization (AI vs. Traditional)")
        
        # เพิ่มข้อมูลสำหรับเปรียบเทียบเข้าไปในประวัติ
        st.session_state.data_list.append({
            "Time": i, 
            "Users": current_user_count, 
            "Adaptive AI Bandwidth": bw,
            "Traditional Bandwidth (Fixed)": baseline
        })
        
        # เก็บข้อมูลย้อนหลัง 20 จุดล่าสุดเพื่อความสวยงาม
        history_df = pd.DataFrame(st.session_state.data_list).tail(20)
        
        # สร้างกราฟแท่งเปรียบเทียบ
        st.bar_chart(history_df.set_index("Time")[["Adaptive AI Bandwidth", "Traditional Bandwidth (Fixed)"]], color=["#2e765e", "#b0bec5"])
        
        # --- ส่วนตาราง Live Logs ---
        st.subheader("👥 Live Network Access Logs")
        display_users = []
        for u in mock_users:
            display_users.append({
                "User ID": process_user_name(u, is_anonymized),
                "Access Status": "Active",
                "IP (Pseudo)": "10.0.0.XXX" if is_anonymized else f"10.0.0.{random.randint(2,254)}"
            })
        st.table(pd.DataFrame(display_users))
        
        time.sleep(1)