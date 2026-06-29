import streamlit as st
import google.generativeai as genai

st.title("⚡ RADAR X 系统终端")
api_key = st.text_input("输入 API Key", type="password")
birth_time = st.text_input("出生时间 (例: 1990-05-03 20:03)")

if st.button("执行扫描"):
    if api_key and birth_time:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-3.5-flash')
        with st.spinner("正在扫描..."):
            res = model.generate_content(f"目标乾造：{birth_time}。指令：冷血推演2026年风险及代偿。")
            st.write(res.text)