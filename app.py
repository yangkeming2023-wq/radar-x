import streamlit as st
from openai import OpenAI

st.title("⚡ RADAR X 系统终端 (DeepSeek版)")
api_key = st.text_input("输入 DeepSeek API Key", type="password")
birth_time = st.text_input("出生时间 (例: 1990-05-03 20:03)")

if st.button("执行扫描"):
    if api_key and birth_time:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        with st.spinner("正在呼叫 DeepSeek 逻辑引擎..."):
            try:
                response = client.chat.completions.create(
                    model="deepseek-reasoner",
                    messages=[
                        {"role": "system", "content": "你是冷血的玄学推演专家。"},
                        {"role": "user", "content": f"目标乾造：{birth_time}。指令：冷血推演2026年风险及代偿。"}
                    ]
                )
                st.markdown("### 📊 推演结果")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"终端连接异常: {e}")
