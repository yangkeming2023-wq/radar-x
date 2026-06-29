import streamlit as st
import google.generativeai as genai

st.title("⚡ RADAR X 系统终端")
api_key = st.text_input("输入 API Key", type="password")
birth_time = st.text_input("出生时间 (例: 1990-05-03 20:03)")

# 使用缓存装饰器，避免重复请求
@st.cache_data(ttl=3600)
def get_radar_analysis(key, time):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('models/gemini-3.5-flash')
    res = model.generate_content(f"目标乾造：{time}。指令：冷血推演2026年风险及代偿。")
    return res.text

if st.button("执行扫描"):
    if api_key and birth_time:
        with st.spinner("正在扫描..."):
            try:
                result = get_radar_analysis(api_key, birth_time)
                st.markdown("### 📊 API 物理映射回传")
                st.write(result)
            except Exception as e:
                st.error("算力中枢资源耗尽，请等待 60 秒后再试。")
