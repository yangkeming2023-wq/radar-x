import streamlit as st
import google.generativeai as genai

st.title("⚡ RADAR X 系统终端")
api_key = st.text_input("输入 API Key", type="password")
birth_time = st.text_input("出生时间 (例: 1990-05-03 20:03)")

# 核心优化：使用 st.session_state 持久化客户端，避免重复连接消耗配额
if 'client' not in st.session_state:
    st.session_state.client = None

def get_model(key):
    if st.session_state.client is None:
        genai.configure(api_key=key)
        st.session_state.client = genai.GenerativeModel('models/gemini-3.5-flash')
    return st.session_state.client

if st.button("执行扫描"):
    if api_key and birth_time:
        try:
            model = get_model(api_key)
            with st.spinner("正在扫描..."):
                # 简化指令，减少 Token 消耗，提高响应速度
                res = model.generate_content(f"乾造:{birth_time}。推演2026年财务风险与代偿动作。")
                st.markdown("### 📊 API 物理映射回传")
                st.write(res.text)
        except Exception as e:
            st.error("算力中枢暂时繁忙，请在 1 分钟内不要重复点击。")
