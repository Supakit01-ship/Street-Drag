import streamlit as st
import time
import random
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. ตั้งค่าหน้าเพจ & ธีม Racing
# ==========================================
st.set_page_config(page_title="Street Tuner: Ultimate", page_icon="🏁", layout="wide")

st.markdown("""
<style>
    .stApp { 
        background-color: #09090b; 
        color: #f8fafc; 
    }
    h1, h2, h3, h4 { 
        font-family: 'Arial Black', sans-serif; 
        color: #0ea5e9; 
        font-style: italic; 
    }
    
    .status-panel { 
        display: flex; 
        justify-content: space-between; 
        background: #1e293b; 
        padding: 20px; 
        border-radius: 15px; 
        border-bottom: 4px solid #0ea5e9; 
        margin-bottom: 20px; 
    }
    .stat-box { 
        text-align: center; 
        width: 20%; 
    }
    .stat-title { 
        font-size: 13px; 
        color: #94a3b8; 
        letter-spacing: 1px; 
    }
    .stat-value { 
        font-size: 30px; 
        font-weight: 900; 
        color: #fbbf24; 
    }
    
    .part-card { 
        background: #18181b; 
        padding: 15px; 
        border-radius: 12px; 
        border: 1px solid #27272a; 
        margin-bottom: 15px; 
        transition: 0.3s; 
        min-height: 180px; 
        display: flex; 
        flex-direction: column; 
        justify-content: space-between;
    }
    .part-card:hover { 
        border-color: #38bdf8; 
        box-shadow: 0 0 15px rgba(56,189,248,0.4); 
        transform: translateY(-3px); 
    }
    .tag-hp { color: #ef4444; font-weight: bold; } 
    .tag-kg { color: #3b82f6; font-weight: bold; } 
    .tag-grip { color: #10b981; font-weight: bold; }
    .item-desc { 
        font-size: 11px; 
        color: #a1a1aa; 
        margin-bottom: 10px; 
        line-height: 1.4; 
    }
    .alert-text { 
        color: #ef4444; 
        font-size: 14px; 
        font-weight: bold; 
        animation: blink 1s infinite;
    }
    
    .boss-intel-sidebar { 
        background: #18181b; 
        padding: 15px; 
        border-radius: 12px; 
        border: 2px solid #ef4444; 
        box-shadow: 0 0 10px rgba(239,68,68,0.2); 
        margin-bottom: 15px; 
    }
    .boss-stat { 
        font-size: 15px; 
        margin-bottom: 5px; 
        color: #e2e8f0; 
    }
    .boss-val { 
        color: #fbbf24; 
        font-weight: bold; 
        font-family: monospace; 
        font-size: 18px; 
        float: right; 
    }
    
    .mechanic-note-sidebar { 
        background: rgba(30, 41, 59, 0.7); 
        padding: 12px; 
        border-radius: 12px; 
        border-left: 4px solid #facc15; 
        margin-bottom: 15px; 
        font-size: 13px; 
        color: #cbd5e1;
    }
    .terminal-box-sidebar { 
        background: #000; 
        color: #10b981; 
        font-family: monospace; 
        padding: 12px; 
        border-radius: 8px; 
        font-size: 11px; 
        margin-bottom: 15px; 
        border: 1px solid #10b981; 
        box-shadow: inset 0 0 10px rgba(16,185,129,0.2); 
    }
    
    button[kind="primary"] {
        background: radial-gradient(circle, #ef4444 0%, #7f1d1d 100%); 
        border: 2px solid #fca5a5;
        border-radius: 30px; 
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.6); 
        color: white !important;
        font-family: 'Arial Black', sans-serif; 
        font-size: 20px !important; 
        letter-spacing: 1px; 
        transition: 0.2s;
    }
    button[kind="primary"]:hover { 
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.9); 
        transform: scale(1.02); 
    }
    button[kind="primary"]:active { 
        transform: scale(0.95); 
    }
    
    @keyframes blink { 
        50% { opacity: 0.5; } 
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. ฐานข้อมูลเกม
# ==========================================
STAGES = [
    {"name": "Rank F: มือใหม่ป้ายแดง", "hp": 130, "weight": 1200, "grip": 40, "prize": 35000, "bot_name": "Honda Brio (Rank F)"},
    {"name": "Rank C: นักซิ่งมิดไนท์", "hp": 200, "weight": 1100, "grip": 55, "prize": 65000, "bot_name": "Civic FD (Rank C)"},
    {"name": "Rank B: โปรเซอร์กิต", "hp": 300, "weight": 1050, "grip": 80, "prize": 125000, "bot_name": "Supra JZA80 (Rank B)"},
    {"name": "Rank A: ราชาเถื่อน", "hp": 480, "weight": 950, "grip": 110, "prize": 250000, "bot_name": "Nissan GT-R R35 (Rank A)"},
    {"name": "Rank S: เทพเจ้าทางเรียบ", "hp": 1000, "weight": 900, "grip": 220, "prize": 500000, "bot_name": "Bugatti Chiron (Rank S)"},
    {"name": "Champion: ตำนานไร้พ่าย", "hp": 9999, "weight": 999, "grip": 999, "prize": 0, "bot_name": "None"}
]

SHOP_PARTS = {
    "Intake & Exhaust": {"price": 10000, "hp": 15, "weight": -5, "grip": 0, "icon": "💨", "desc": "เปลี่ยนกรองเปลือยและท่อไอเสีย (คุ้มค่าสำหรับเงินที่เหลือเศษหมื่น)"},
    "ECU Remap": {"price": 15000, "hp": 25, "weight": 0, "grip": 0, "icon": "💻", "desc": "จูนกล่อง เพิ่มแรงม้าเพียวๆ ไม่เพิ่มน้ำหนักรถ"},
    "Runstop Brakes": {"price": 20000, "hp": 0, "weight": 5, "grip": 20, "icon": "🛑", "desc": "เบรคจานโต ช่วยล็อกล้อตอนออกตัว (เพิ่มขีดจำกัดม้าลงพื้น)"},
    "Weight Reduction": {"price": 20000, "hp": 0, "weight": -50, "grip": -2, "icon": "🪶", "desc": "รื้อเบาะ ใส่พาร์ทคาร์บอน รถเบาหวิว แต่ถ้ารถเบาไปท้ายจะปัดง่าย"},
    "Toyo R888R Tires": {"price": 30000, "hp": 0, "weight": 0, "grip": 35, "icon": "🛞", "desc": "ยางกึ่งสลิคสุดหนึบ ดันเพดาน 'ขีดจำกัดยาง' ขั้นสุด ล้อไม่ฟรีทิ้ง"},
    "Turbocharger": {"price": 35000, "hp": 80, "weight": 15, "grip": 0, "icon": "🐌", "desc": "อัดอากาศเข้าห้องเผาไหม้ แรงม้าพุ่งปรี๊ด (แนะนำให้ซื้อคู่กับยางหรือเบรค)"},
    "NOS Injection Kit": {"price": 40000, "hp": 0, "weight": 5, "grip": 0, "icon": "🔥", "desc": "ระบบฉีดไนตรัสแบบตั้งเวลา ช่วยลดเวลาเข้าเส้นชัย (ใช้พลิกเกมตอนแข่ง)"}
}

# ==========================================
# 3. Session State
# ==========================================
def init_game():
    st.session_state.money = 50000  
    st.session_state.hp = 110  
    st.session_state.weight = 1250
    st.session_state.grip = 35
    st.session_state.owned = []
    st.session_state.phase = "garage"
    st.session_state.stage_idx = 0

if "money" not in st.session_state:
    init_game()

current_stage = STAGES[st.session_state.stage_idx]
max_traction_hp = st.session_state.grip * 6 
excess_hp = max(0, st.session_state.hp - max_traction_hp)

# ==========================================
# 4. แถบ Sidebar
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ ระบบจัดการเกม")
    if st.button("🔄 รีเซ็ตเริ่มเกมใหม่", use_container_width=True):
        init_game()
        st.rerun()
    
    st.write("---")
    
    if st.session_state.stage_idx < 5:
        st.markdown(f"""
        <div class="boss-intel-sidebar">
            <h5 style="color:#ef4444; margin-top:0; border-bottom: 1px solid #3f3f46; padding-bottom: 8px;">🎯 RIVAL INTEL</h5>
            <div style="color:#ef4444; font-weight:bold; margin-bottom: 10px;">{current_stage['bot_name']}</div>
            <div class="boss-stat">🐎 แรงม้า: <span class="boss-val">{current_stage['hp']}</span></div>
            <div class="boss-stat">⚖️ น้ำหนัก: <span class="boss-val">{current_stage['weight']}</span></div>
            <div class="boss-stat">🛞 ยึดเกาะ: <span class="boss-val">{current_stage['grip']}</span></div>
            <div style="margin-top: 15px; font-size:12px; color:#a1a1aa;">
                💰 รางวัล: <span style="color:#4ade80; font-size:16px; font-weight:bold; float:right;">฿{current_stage['prize']:,}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"🔴 PUSH START (RACE)", type="primary", use_container_width=True):
            st.session_state.phase = "race"
            st.rerun()
            
        mechanic_msg = "ม้าลงพื้น 100% บาลานซ์รถตอนนี้สวยจัดๆ ครับลูกพี่!"
        if excess_hp > 0:
            mechanic_msg = f"ลูกพี่! รถเราแรงเกินไป ม้าล้นอยู่ {excess_hp} ตัว ล้อฟรีแน่ๆ แนะนำให้ซื้อเบรค Runstop หรือ ยาง Toyo มาใส่ด่วน!"
        elif st.session_state.hp < current_stage['hp']:
            mechanic_msg = "ม้าเรายังน้อยกว่าบอสอยู่ อาจจะเหนื่อยหน่อย ลองหาเงินยัด Turbo หรือ ECU ดูครับ"
            
        st.markdown(f"""
        <div class="mechanic-note-sidebar">
            <strong style="color: #facc15;">👨‍🔧 Mechanic's Note</strong><br>{mechanic_msg}
        </div>
        """, unsafe_allow_html=True)
        
        trac_color = "#ef4444" if excess_hp > 0 else "#10b981"
        trac_status = "WARNING: WHEEL SPIN" if excess_hp > 0 else "OPTIMAL"
        st.markdown(f"""
        <div class="terminal-box-sidebar">
            > SYSTEM DIAGNOSTIC<br>
            > ECU: <span style="color:#38bdf8;">SYNCED</span><br>
            > WEIGHT: <span style="color:#38bdf8;">{st.session_state.weight} KG</span><br>
            > TRACTION: <span style="color:{trac_color};">{trac_status}</span><br>
            <br>
            <div style="text-align:center; animation: blink 2s infinite;">[ STANDBY ]</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("🏆 โค่นบอสครบทุกคนแล้ว!")

# ==========================================
# 5. โหมดอู่แต่งรถ (Garage)
# ==========================================
if st.session_state.phase == "garage":
    st.title("🔧 THE GARAGE: ศูนย์ปรับแต่งรถยนต์")
    
    warning_html = ""
    if excess_hp > 0:
        warning_html = f"<div class='alert-text' style='text-align:center; margin-bottom:10px;'>⚠️ ม้าลงพื้นไม่ได้! รถแรงเกินยางจะรับไหว ล้อจะฟรีทิ้งตอนแข่ง! (ซื้อยาง/เบรคเพื่อขยายขีดจำกัด)</div>"

    st.markdown(f"""
    {warning_html}
    <div class="status-panel">
        <div class="stat-box">
            <div class="stat-title">งบประมาณ</div>
            <div class="stat-value" style="color:#4ade80;">฿{st.session_state.money:,}</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">แรงม้า (HP)</div>
            <div class="stat-value">{st.session_state.hp}</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">น้ำหนัก (KG)</div>
            <div class="stat-value">{st.session_state.weight}</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">การยึดเกาะ (GRIP)</div>
            <div class="stat-value">{st.session_state.grip}</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">ขีดจำกัดม้าลงพื้น</div>
            <div class="stat-value" style="color:#e2e8f0;">{max_traction_hp} HP</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("---")

    st.subheader("🛒 PERFORMANCE SHOP")
    cols = st.columns(3)
    for i, (p_name, stats) in enumerate(SHOP_PARTS.items()):
        with cols[i % 3]:
            count = st.session_state.owned.count(p_name)
            lv_txt = f"<span style='color:#fbbf24;'>(Lv.{count})</span>" if count > 0 else ""
            
            st.markdown(f"""
            <div class="part-card">
                <div>
                    <h4 style="margin-top:0;">{stats['icon']} {p_name} {lv_txt}</h4>
                    <div class="item-desc">{stats['desc']}</div>
                    <div style="margin-bottom: 10px;">
                        <span class='tag-hp'>HP: +{stats['hp']}</span> | 
                        <span class='tag-kg'>KG: {stats['weight']}</span> | 
                        <span class='tag-grip'>Grip: +{stats['grip']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"ซื้อ ฿{stats['price']:,}", key=f"buy_{p_name}", use_container_width=True):
                if st.session_state.money >= stats["price"]:
                    st.session_state.money -= stats["price"]
                    st.session_state.hp += stats["hp"]
                    st.session_state.weight = max(500, st.session_state.weight + stats["weight"])
                    st.session_state.grip += stats["grip"]
                    st.session_state.owned.append(p_name)
                    st.rerun()
                else:
                    st.error("❌ เงินไม่พอ หาเงินมาใหม่นะไอ้หนุ่ม!")
            st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 6. โหมดสนามแข่ง (Race)
# ==========================================
elif st.session_state.phase == "race":
    st.title(f"🚦 DRAG STRIP 402m: {current_stage['name']}")
    
    if st.button("🔙 กลับอู่แต่งรถ"):
        st.session_state.phase = "garage"
        st.rerun()
        
    c1, c2 = st.columns(2)
    c1.info(f"**🚗 รถของคุณ** ➔ HP: {st.session_state.hp} | KG: {st.session_state.weight} | Grip: {st.session_state.grip}")
    c2.error(f"**🏎️ {current_stage['bot_name']}** ➔ HP: {current_stage['hp']} | KG: {current_stage['weight']} | Grip: {current_stage['grip']}")
    
    st.write("---")
    col_rpm, col_nos = st.columns(2)
    
    with col_rpm:
        optimal_rpm = 2500 + (st.session_state.grip * 25)
        st.subheader("⚙️ LAUNCH CONTROL")
        st.caption(f"💡 คำใบ้จากช่างยนต์: เพื่อการพุ่งตัวที่ 100% ให้จูนรอบเครื่องไว้ที่ **{optimal_rpm} RPM**")
        launch_rpm = st.slider("เลือกรอบเครื่อง:", min_value=1000, max_value=15000, value=4000, step=25)
    
    with col_nos:
        has_nos = st.session_state.owned.count("NOS Injection Kit") > 0
        nos_timing = 0.0
        if has_nos:
            nos_count = st.session_state.owned.count("NOS Injection Kit")
            st.subheader(f"🔥 NOS SYSTEM (LV.{nos_count})")
            st.caption("⚠️ คำเตือน: อย่าตั้งฉีดช่วง 0 - 1.5 วิแรก ล้อจะฟรีทิ้ง! ให้ฉีดช่วงกลางทางเพื่อดึงท็อปสปีด")
            nos_timing = st.slider("ตั้งเวลาฉีด NOS (วินาทีที่):", min_value=0.0, max_value=6.0, value=3.0, step=0.1)
        else:
            st.subheader("🔥 NOS SYSTEM")
            st.caption("❌ ยังไม่ได้ติดตั้งระบบ NOS (ซื้อได้ที่ร้านค้า)")
    
    st.write("")
    if st.button("🔴 PUSH START (RACE!)", type="primary", use_container_width=True):
        
        # --- 1. คำนวณฟิสิกส์ ---
        effective_hp = min(st.session_state.hp, max_traction_hp)
        p_base = 5.825 * ((st.session_state.weight / effective_hp) ** (1/3))
        ai_time = 5.825 * ((current_stage['weight'] / current_stage['hp']) ** (1/3)) + random.uniform(-0.1, 0.2)
        
        rpm_error = abs(launch_rpm - optimal_rpm) / 6000.0
        traction_penalty = excess_hp * 0.010 
        p_time = (p_base * (1.0 + rpm_error)) + traction_penalty
        
        nos_status_msg = ""
        nos_success = False
        if has_nos:
            nos_power = 0.8 * nos_count 
            if nos_timing <= 1.5:
                p_time += 1.5 * nos_count
                nos_status_msg = f"💥 บรรลัยแล้ว! ฉีด NOS ตอนล้อยังไม่เกาะถนน รถส่ายเสียเวลาไป {1.5 * nos_count:.2f} วินาที!"
            else:
                p_time = max(3.0, p_time - nos_power)
                nos_success = True
                nos_status_msg = f"🚀 ไนตรัสทำงานสมบูรณ์แบบ! ดึงท็อปสปีดหักเวลาลงไป {nos_power:.2f} วินาที!"
        
        # --- 2. แอนิเมชันรถแข่ง & โมเดลรถ AI 2 มิติ ด้านข้าง (SVG) ---
        track_html = f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&display=swap');
            
            .track-bg {{ 
                width: 100%; 
                height: 280px; 
                background-color: #1c1917; 
                border-radius: 10px; 
                position: relative; 
                overflow: hidden; 
                border: 4px solid #444; 
                border-bottom: 8px solid #292524; 
            }}
            .road-lines {{ 
                position: absolute; 
                top: 140px; 
                left: 0; 
                width: 200%; 
                height: 8px; 
                background: repeating-linear-gradient(90deg, transparent, transparent 50px, #facc15 50px, #facc15 120px); 
                animation: moveRoad 0.3s linear infinite; 
            }}
            .finish-line {{ 
                position: absolute; 
                left: 85%; 
                top: 0; 
                width: 25px; 
                height: 100%; 
                background: repeating-linear-gradient(45deg, #000 0px, #000 10px, #fff 10px, #fff 20px); 
                z-index: 10; 
                border-left: 3px solid #ef4444; 
                box-shadow: -10px 0 20px rgba(0,0,0,0.8); 
            }}
            .flag-icon {{ 
                position: absolute; 
                left: 86%; 
                top: 10px; 
                font-size: 35px; 
                z-index: 15; 
            }}
            .led-container {{ 
                position: absolute; 
                top: 10px; 
                left: 50%; 
                transform: translateX(-50%); 
                display: flex; 
                gap: 15px; 
                z-index: 5; 
            }}
            .led-board {{ 
                background: #000; 
                border: 2px solid #3f3f46; 
                border-radius: 5px; 
                padding: 5px 15px; 
                color: #ef4444; 
                font-family: 'Orbitron', sans-serif; 
                font-size: 18px; 
                text-align: center; 
                box-shadow: 0 0 15px rgba(239, 68, 68, 0.3); 
                min-width: 140px; 
            }}
            .led-title {{ 
                font-size: 10px; 
                color: #94a3b8; 
                margin-bottom: 3px; 
                font-family: sans-serif; 
                letter-spacing: 1px; 
            }}
            
            /* รถผู้เล่น (พลิกกลับด้านให้หันขวาและควันออกท้าย) */
            #car-player {{ 
                position: absolute; 
                font-size: 70px; 
                left: 2%; 
                top: 30px; 
                z-index: 20; 
                transform: scaleX(-1); 
                filter: drop-shadow(-10px 10px 5px rgba(0,0,0,0.6)); 
                animation: racePlayer {p_time}s ease-in forwards; 
            }}
            
            /* 🟢 รถ AI 2D ด้านข้าง (วาดหันขวาโดยตรงพร้อมเอฟเฟกต์ไฟท่อไอเสีย) */
            #car-ai {{ 
                position: absolute; 
                width: 145px; 
                height: 65px; 
                left: 2%; 
                top: 168px; 
                z-index: 20; 
                filter: drop-shadow(8px 10px 6px rgba(0,0,0,0.7)); 
                animation: raceAI {ai_time}s ease-in forwards; 
            }}
            
            .flame-anim {{
                animation: flickerFlame 0.08s infinite alternate;
                transform-origin: right center;
            }}
            
            @keyframes flickerFlame {{
                0% {{ transform: scaleX(0.85) scaleY(0.9); opacity: 0.8; }}
                100% {{ transform: scaleX(1.25) scaleY(1.1); opacity: 1; }}
            }}
            @keyframes moveRoad {{ 
                0% {{ transform: translateX(0); }} 
                100% {{ transform: translateX(-140px); }} 
            }}
            @keyframes racePlayer {{ 
                0% {{ left: 2%; }} 
                100% {{ left: calc(85% - 20px); }} 
            }}
            @keyframes raceAI {{ 
                0% {{ left: 2%; }} 
                100% {{ left: calc(85% - 20px); }} 
            }}
        </style>
        
        <div class="track-bg">
            <div class="led-container">
                <div class="led-board"><div class="led-title">PLAYER (YOU)</div><span id="timer-p">0.00s</span></div>
                <div class="led-board"><div class="led-title">RIVAL (AI)</div><span id="timer-ai">0.00s</span></div>
            </div>
            <div class="road-lines"></div>
            <div class="flag-icon">🏁</div>
            <div class="finish-line"></div>
            
            <!-- รถผู้เล่น -->
            <div id="car-player">🏎️💨</div>
            
            <!-- 🟢 รูปรถ 2 มิติ มุมมองด้านข้าง (2D Side-View SVG) สำหรับบอท AI -->
            <div id="car-ai">
                <svg viewBox="0 0 240 90" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="aiBodyGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#7f1d1d" />
                            <stop offset="50%" stop-color="#dc2626" />
                            <stop offset="100%" stop-color="#991b1b" />
                        </linearGradient>
                        <linearGradient id="glassGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stop-color="#09090b" />
                            <stop offset="100%" stop-color="#27272a" />
                        </linearGradient>
                    </defs>
                    
                    <!-- ควันและเปลวไฟท่อไอเสีย (ด้านซ้าย/ท้ายรถ) -->
                    <g class="flame-anim">
                        <polygon points="38,58 4,48 16,58 0,63 18,65 8,72 38,65" fill="#f97316" opacity="0.9"/>
                        <polygon points="38,59 15,54 24,60 12,63 38,64" fill="#fde047"/>
                    </g>
                    
                    <!-- สปอยเลอร์หลัง GT Wing -->
                    <polygon points="45,42 36,22 44,22 52,42" fill="#18181b" stroke="#3f3f46" stroke-width="1.5"/>
                    <polygon points="30,19 56,22 55,26 29,23" fill="#ef4444"/>
                    
                    <!-- สเกิร์ตล่างและดิฟฟิวเซอร์ -->
                    <polygon points="35,66 226,66 232,61 32,61" fill="#18181b"/>
                    
                    <!-- ตัวถังรถซิ่ง 2D ด้านข้าง -->
                    <path d="M 36,62 L 36,42 L 60,40 L 92,22 L 145,22 L 178,39 L 222,46 L 228,62 Z" fill="url(#aiBodyGrad)" stroke="#fca5a5" stroke-width="1"/>
                    
                    <!-- ลายคาดข้างรถซิ่ง (Racing Stripe) -->
                    <polygon points="40,51 224,53 226,57 40,56" fill="#18181b" opacity="0.85"/>
                    <polygon points="65,45 185,47 190,50 60,48" fill="#fbbf24"/>
                    
                    <!-- กระจกหน้าต่างด้านข้าง -->
                    <polygon points="68,39 95,25 142,25 170,39" fill="url(#glassGrad)" stroke="#52525b" stroke-width="1.5"/>
                    <line x1="120" y1="25" x2="115" y2="39" stroke="#3f3f46" stroke-width="2.5"/>
                    
                    <!-- ไฟหน้า LED & ไฟท้าย -->
                    <polygon points="212,45 224,47 226,53 210,51" fill="#fef08a" stroke="#facc15" stroke-width="1"/>
                    <rect x="35" y="44" width="7" height="8" rx="1" fill="#ff0000" stroke="#fca5a5" stroke-width="1"/>
                    
                    <!-- ซุ้มล้อหลัง & ล้อแม็กหลัง -->
                    <circle cx="80" cy="63" r="20" fill="#09090b"/>
                    <circle cx="80" cy="63" r="17" fill="#18181b" stroke="#3f3f46" stroke-width="3"/>
                    <circle cx="80" cy="63" r="11" fill="#27272a" stroke="#eab308" stroke-width="2"/>
                    <circle cx="75" cy="60" r="4" fill="#ef4444"/> <!-- คาลิปเปอร์เบรกแดง -->
                    <line x1="80" y1="52" x2="80" y2="74" stroke="#eab308" stroke-width="2"/>
                    <line x1="69" y1="63" x2="91" y2="63" stroke="#eab308" stroke-width="2"/>
                    <circle cx="80" cy="63" r="3" fill="#facc15"/>
                    
                    <!-- ซุ้มล้อหน้า & ล้อแม็กหน้า -->
                    <circle cx="185" cy="63" r="20" fill="#09090b"/>
                    <circle cx="185" cy="63" r="17" fill="#18181b" stroke="#3f3f46" stroke-width="3"/>
                    <circle cx="185" cy="63" r="11" fill="#27272a" stroke="#eab308" stroke-width="2"/>
                    <circle cx="180" cy="60" r="4" fill="#ef4444"/> <!-- คาลิปเปอร์เบรกแดง -->
                    <line x1="185" y1="52" x2="185" y2="74" stroke="#eab308" stroke-width="2"/>
                    <line x1="174" y1="63" x2="196" y2="63" stroke="#eab308" stroke-width="2"/>
                    <circle cx="185" cy="63" r="3" fill="#facc15"/>
                </svg>
            </div>
        </div>
        
        <script>
            const timerP = document.getElementById('timer-p');
            const timerAI = document.getElementById('timer-ai');
            let startTime = Date.now();
            let pTimeLimit = {p_time};
            let aiTimeLimit = {ai_time};
            let maxTimeLimit = Math.max(pTimeLimit, aiTimeLimit);
            
            function updateTimer() {{
                let elapsed = (Date.now() - startTime) / 1000;
                
                if (elapsed >= pTimeLimit) {{
                    timerP.innerText = pTimeLimit.toFixed(2) + "s";
                    timerP.style.color = "#38bdf8"; 
                }} else {{
                    timerP.innerText = elapsed.toFixed(2) + "s";
                }}
                
                if (elapsed >= aiTimeLimit) {{
                    timerAI.innerText = aiTimeLimit.toFixed(2) + "s";
                    timerAI.style.color = "#ef4444"; 
                }} else {{
                    timerAI.innerText = elapsed.toFixed(2) + "s";
                }}
                
                if (elapsed < maxTimeLimit) {{
                    requestAnimationFrame(updateTimer);
                }}
            }}
            requestAnimationFrame(updateTimer);
        </script>
        """
        st.components.v1.html(track_html, height=300)
        
        # --- 3. รายงานสถานะระหว่างออกตัว ---
        status_box = st.empty()
        if excess_hp > 0:
            status_box.error(f"⚠️ ยางรับม้าไม่ไหว ล้อฟรีทิ้งเสียเวลาไป {traction_penalty:.2f} วินาที!")
        elif rpm_error > 0.15:
            status_box.warning("⚠️ ออกตัวสะดุด! ตั้งรอบเครื่องไม่สัมพันธ์กับ Grip!")
        else:
            if has_nos:
                if nos_success: 
                    status_box.success(f"🔥 PERFECT LAUNCH! ออกตัวเนียนกริบ! และ {nos_status_msg}")
                else: 
                    status_box.error(f"🔥 PERFECT LAUNCH! แต่ออกตัวแรงไป {nos_status_msg}")
            else:
                status_box.success("🔥 PERFECT LAUNCH! ออกตัวเนียนกริบ!")
            
        # --- 4. การจัดการหน่วงเวลาของ Python ให้ซิงค์กับการเข้าเส้นชัยของคันแรก ---
        winner_time = min(p_time, ai_time) 
        render_delay = 0.3 
        
        with st.spinner("🏁 กำลังพุ่งทะยานเข้าสู่เส้นชัย..."):
            if has_nos:
                if nos_timing < winner_time:
                    time.sleep(nos_timing)
                    if nos_success: 
                        st.info(nos_status_msg)
                    else: 
                        st.error(nos_status_msg)
                    
                    sleep_remain = winner_time - nos_timing
                    if sleep_remain > 0: 
                        time.sleep(sleep_remain + render_delay)
                else:
                    time.sleep(winner_time + render_delay)
            else:
                time.sleep(winner_time + render_delay)
            
        # ==========================================
        # 🏁 หน้าจอ WIN (เด้งเป๊ะๆ ตอนแตะเส้นชัย!)
        # ==========================================
        st.write("---")
        if p_time < ai_time:
            st.session_state.money += current_stage['prize']
            if st.session_state.stage_idx < len(STAGES) - 1:
                st.session_state.stage_idx += 1 
            
            victory_html = f"""
            <style>
                .victory-border {{ 
                    background: linear-gradient(45deg, #0ea5e9, #10b981, #0ea5e9); 
                    background-size: 200% 200%; 
                    padding: 6px; 
                    border-radius: 12px; 
                    margin: 10px 0; 
                    animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
                    box-shadow: 0 10px 30px rgba(16,185,129,0.4); 
                }}
                .victory-inner {{ 
                    background: #09090b; 
                    text-align: center; 
                    padding: 25px; 
                    border-radius: 8px; 
                }}
                .vic-title {{ 
                    font-size: 55px; 
                    font-weight: 900; 
                    color: #10b981; 
                    text-shadow: 0 0 20px #10b981; 
                    margin: 0; 
                    font-style: italic; 
                    font-family: 'Arial Black', sans-serif; 
                    letter-spacing: 3px;
                }}
                .vic-stat {{ 
                    font-size: 18px; 
                    color: #94a3b8; 
                    margin-top: 10px; 
                    font-family: monospace; 
                    letter-spacing: 1px;
                }}
                .vic-prize {{ 
                    font-size: 32px; 
                    color: #fbbf24; 
                    margin-top: 15px; 
                    font-weight: bold; 
                    text-shadow: 0 0 15px rgba(251,191,36,0.5); 
                }}
                @keyframes popIn {{ 
                    0% {{ transform: scale(0.5); opacity: 0; }} 
                    100% {{ transform: scale(1); opacity: 1; }} 
                }}
            </style>
            <div class="victory-border">
                <div class="victory-inner">
                    <p class="vic-title">🏆 YOU WIN! 🏆</p>
                    <p class="vic-stat">PLAYER TIME: <span style="color:#fff;">{p_time:.2f}s</span> &nbsp;|&nbsp; AI TIME: <span style="color:#ef4444;">{ai_time:.2f}s</span></p>
                    <p class="vic-prize">CASH REWARD: +฿{current_stage['prize']:,}</p>
                </div>
            </div>
            """
            st.markdown(victory_html, unsafe_allow_html=True)
            
        else:
            wasted_html = f"""
            <style>
                .wasted-border {{ 
                    background: #ef4444; 
                    padding: 3px; 
                    border-radius: 12px; 
                    margin: 10px 0; 
                    animation: shake 0.5s; 
                    box-shadow: 0 10px 30px rgba(239,68,68,0.3); 
                }}
                .wasted-inner {{ 
                    background: #09090b; 
                    text-align: center; 
                    padding: 25px; 
                    border-radius: 10px; 
                }}
                .was-title {{ 
                    font-size: 50px; 
                    font-weight: 900; 
                    color: #ef4444; 
                    text-shadow: 0 0 20px #ef4444; 
                    margin: 0; 
                    font-family: 'Arial Black', sans-serif; 
                    letter-spacing: 5px;
                }}
                .was-stat {{ 
                    font-size: 18px; 
                    color: #94a3b8; 
                    margin-top: 10px; 
                    font-family: monospace; 
                    letter-spacing: 1px;
                }}
                @keyframes shake {{ 
                    0%, 100% {{transform: translateX(0);}} 
                    25% {{transform: translateX(-10px);}} 
                    75% {{transform: translateX(10px);}} 
                }}
            </style>
            <div class="wasted-border">
                <div class="wasted-inner">
                    <p class="was-title">DEFEAT</p>
                    <p class="was-stat">PLAYER TIME: <span style="color:#ef4444;">{p_time:.2f}s</span> &nbsp;|&nbsp; AI TIME: <span style="color:#fff;">{ai_time:.2f}s</span></p>
                    <p style="color:#cbd5e1; margin-top:10px;">กลับไปจูนรถให้ดี ตั้งจังหวะ NOS ใหม่ แล้วมาล้างแค้น!</p>
                </div>
            </div>
            """
            st.markdown(wasted_html, unsafe_allow_html=True)

        # ==========================================
        # 📊 คำนวณข้อมูล Telemetry Data (ความเร็ว, อัตราเร่ง)
        # ==========================================
        t_max = max(p_time, ai_time) + 1.0
        time_arr = np.linspace(0, t_max, 100)
        
        def calc_speed_profile(t_array, finish_time, wheel_spin_penalty=0, used_nos=False, nos_time=0):
            speeds = []
            for t in t_array:
                if t <= wheel_spin_penalty:
                    speeds.append(random.uniform(10, 25))
                elif t <= finish_time:
                    eff_time = finish_time - wheel_spin_penalty
                    a = (2 * 402) / (eff_time**2)
                    v = a * (t - wheel_spin_penalty)
                    if used_nos and t >= nos_time:
                        v *= 1.3 
                    speeds.append(v * 3.6) 
                else:
                    speeds.append(speeds[-1] if speeds else 0)
            return np.array(speeds)

        p_speed_data = calc_speed_profile(time_arr, p_time, traction_penalty, nos_success, nos_timing)
        ai_speed_data = calc_speed_profile(time_arr, ai_time, 0, False, 0)
        
        zero_to_100_time = "N/A"
        if max(p_speed_data) >= 100:
            idx_100 = np.argmax(p_speed_data >= 100)
            zero_to_100_time = f"{time_arr[idx_100]:.2f}s"
            
        top_speed_kmh = max(p_speed_data)
        power_efficiency = (effective_hp / st.session_state.hp) * 100 

        # ==========================================
        # 💡 ระบบ AI Mechanic (Tuning Tips แนะนำหลังแข่ง)
        # ==========================================
        st.write("---")
        st.subheader("💡 ช่างยนต์แนะนำ (Post-Race Tuning Tips)")
        
        tips = []
        if excess_hp > 0:
            tips.append("⚠️ **รถแรงเกินยางจะรับไหว!** ล้อฟรีทิ้งช่วงออกตัว ทำให้เสียเวลาไปมาก ไปซื้อ **Toyo R888R Tires** หรือ **Runstop Brakes** เพื่อเพิ่ม Grip ด่วน!")
        if rpm_error > 0.15:
            tips.append(f"⚙️ **รอบออกตัวพลาด!** คุณจูนรอบเครื่องห่างจากจุดที่ดีที่สุด ทำให้เสียจังหวะตอนสับเกียร์ (ควรตั้งไว้แถวๆ **{optimal_rpm} RPM**)")
        if has_nos and nos_timing <= 1.5:
            tips.append("💨 **ฉีด NOS เร็วไป!** กดตอนรถยังไม่เกาะถนนทำให้ท้ายปัดเสียหลัก ลองเปลี่ยนไปตั้งฉีดช่วงกลางทาง (ประมาณ 2.5 - 3.5 วิ) เพื่อดึงท็อปสปีดปลาย")
        if p_time > ai_time and excess_hp <= 0 and rpm_error <= 0.15:
            if st.session_state.weight > current_stage['weight'] + 100:
                tips.append("🪶 **รถหนักเกินไป!** อัตราเร่งช่วงปลายคุณสู้บอทไม่ได้ ลองซื้อ **Weight Reduction** เพื่อรื้อเบาะลดน้ำหนักดู")
            else:
                tips.append("🐌 **แรงม้ายังน้อยไป!** รถเกาะถนนเยี่ยมแล้ว แต่กำลังเครื่องไม่พอตามบอท ลองเก็บเงินยัด **Turbocharger** หรืออัปเกรด **ECU Remap**")
                
        if not tips:
            tips.append("🔥 **เพอร์เฟกต์แมตช์!** คุณเซ็ตรถมาได้สมบูรณ์แบบ ทั้งการจูนรอบเครื่องและการเกาะถนนไร้ที่ติ!")

        for tip in tips:
            st.info(tip)

        # ==========================================
        # 📊 แสดง Dashboard ตัวเลขสถิติ และ กราฟ
        # ==========================================
        st.subheader("📊 POST-RACE TELEMETRY")
        
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        col_kpi1.metric(label="🏁 อัตราเร่ง 0-100 km/h", value=zero_to_100_time)
        col_kpi2.metric(label="🚀 ความเร็วสูงสุดเข้าเส้นชัย (Top Speed)", value=f"{top_speed_kmh:.0f} km/h")
        
        efficiency_color = "normal" if power_efficiency == 100 else "inverse"
        col_kpi3.metric(label="⚙️ ประสิทธิภาพม้าลงพื้น (Power to Ground)", value=f"{power_efficiency:.0f}%", delta=f"-{excess_hp} HP ล้อฟรี" if excess_hp > 0 else "Optimal", delta_color=efficiency_color)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_arr, y=p_speed_data, mode='lines', name='Player (You)', line=dict(color='#38bdf8', width=3), fill='tozeroy', fillcolor='rgba(56, 189, 248, 0.1)'))
        fig.add_trace(go.Scatter(x=time_arr, y=ai_speed_data, mode='lines', name='AI Bot', line=dict(color='#ef4444', width=3, dash='dot')))
        
        if has_nos and nos_success:
            fig.add_vline(x=nos_timing, line_width=2, line_dash="solid", line_color="#facc15", annotation_text=f"🔥 NOS INJECTED!", annotation_position="top left")

        fig.add_vline(x=p_time, line_width=1, line_dash="dash", line_color="#38bdf8", annotation_text=f"Player Finish")
        fig.add_vline(x=ai_time, line_width=1, line_dash="dash", line_color="#ef4444", annotation_text=f"AI Finish")

        fig.update_layout(
            plot_bgcolor='#0e1117', 
            paper_bgcolor='#0e1117', 
            font_color='#e2e8f0',
            xaxis=dict(title='Time (Seconds)', showgrid=True, gridcolor='#1e293b'),
            yaxis=dict(title='Speed (km/h)', showgrid=True, gridcolor='#1e293b'),
            hovermode="x unified", 
            height=450,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        st.plotly_chart(fig, use_container_width=True)