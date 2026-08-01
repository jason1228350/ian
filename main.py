import streamlit as st
import time
import pandas as pd

# ==========================================
# 頁面基本設定 (Page Configuration)
# ==========================================
st.set_page_config(
    page_title="IoT/車聯網韌體自動化漏洞檢測平台",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂標題與風格
st.title("🛡️ SentinelFuzz:物聯網韌體 Zero-Day 漏洞自動化檢測系統")
st.caption("基於 QEMU 全系統模擬與動態監控架構 | 專題評審控制台 v1.0")
st.markdown("---")

# ==========================================
# 側邊欄：韌體載入與參數設定 (Sidebar)
# ==========================================
st.sidebar.header("⚙️ 模擬器與目標設定")

firmware_file = st.sidebar.file_uploader("1. 上傳目標韌體檔案 (.bin / .img)", type=["bin", "img", "zip"])

arch_type = st.sidebar.selectbox(
    "2. 選擇模擬架構 (QEMU Target)",
    ["MIPS (Big Endian)", "MIPS (Little Endian)", "ARM32 Cortex-A9", "AArch64 (ARM64)"]
)

fuzz_speed = st.sidebar.slider("3. Fuzzing 變異頻率 (Execs/sec)", 100, 5000, 1200)

start_button = st.sidebar.button("🚀 啟動 QEMU 自動化測試", type="primary")

# ==========================================
# 主畫面內容 (Main Area)
# ==========================================

# 1. 系統狀態概觀 (Metrics)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="QEMU 模擬狀態", value="運行中 (Running)" if start_button else "就緒 (Ready)")
with col2:
    st.metric(label="測試總次數 (Execs)", value="142,850" if start_button else "0")
with col3:
    st.metric(label="捕獲異常 (Crashes)", value="3" if start_button else "0", delta="需關注" if start_button else None)
with col4:
    st.metric(label="代碼覆蓋率 (Coverage)", value="68.4%" if start_button else "0.0%")

st.markdown("---")

# 2. 測試主分頁
tab1, tab2, tab3 = st.tabs(["📊 即時檢測儀表板", "⚠️ 異常分析報告 (Crash Analysis)", "📝 QEMU 系統日誌 (System Logs)"])

with tab1:
    st.subheader("📈 記憶體狀態與測試覆蓋率趨勢")
    
    if start_button:
        # 模擬即時動態數據
        chart_data = pd.DataFrame({
            '時間(秒)': list(range(1, 11)),
            '程式碼覆蓋率 (%)': [12, 25, 38, 45, 52, 58, 61, 65, 67, 68.4],
            '記憶體異常開銷 (MB)': [15, 18, 22, 45, 80, 30, 28, 95, 32, 30]
        })
        st.line_chart(chart_data.set_index('時間(秒)'))
        st.success("✅ 自動化變異測試持續進行中... QEMU 模擬核心運行正常。")
    else:
        st.info("👈 請於左側選單上傳韌體檔並點擊「啟動 QEMU 自動化測試」開始模擬。")

with tab2:
    st.subheader("🚨 捕獲之 Zero-Day 記憶體異常")
    if start_button:
        st.error("【警報】於位址 `0x800412A0` 檢測到 Heap Buffer Overflow（堆疊溢位漏洞）！")
        
        with st.expander("🔍 檢視詳細記憶體 Dump 與漏洞成因分析"):
            st.code("""
[CRASH DETECTED]
Target Architecture: MIPS32
Faulting Address   : 0x800412A0 (strcpy in httpd_parse_header)
Registers State    :
  $pc : 0x800412A0    $ra : 0x800411B0
  $a0 : 0x7fff5c00    $a1 : 0x41414141 (Overwritten)
Vulnerability Type : Heap-based Buffer Overflow
Remediation        : Replace unsafe strcpy with strncpy in HTTP header handler.
            """, language="text")
    else:
        st.write("尚無觸發之異常紀錄。")

with tab3:
    st.subheader("📋 系統即時監控 Console")
    st.text_area(
        "QEMU Console Output",
        value="[+] QEMU Full-System Emulator Initialized.\n[+] Target Firmware Loaded: ./sample_firmware.bin\n[+] Virtual Network Interface Active (192.168.1.1)\n[+] Fuzzing Engine Attached to Port 80/TCP...",
        height=200
    )