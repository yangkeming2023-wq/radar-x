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
               # 修改 app.py 中的 messages 部分，替换为：
messages=[
    {"role": "system", "content": """你是一位精通《渊海子平》、《三命通会》、《滴天髓》的玄学推演专家。
    请按以下严谨逻辑进行分析：
    1.【命局体用】：先定原局旺衰，指出庚金食神与壬水偏财的虚实。
    2.【库冲联动】：重点分析辰戌冲对财库（辰）和火库（戌）的破坏与触发机制。
    3.【流年推演】：2026丙午年，火土过燥，必须明确指出“丙火盖头”对庚金的灼伤及“午戌半合”对印库的影响。
    4.【五行通关】：不要给民俗迷信建议。必须提供符合五行逻辑的“通关”方案（如：金水木的行业属性如何化解火土燥气）。
    语言风格要求：冷血、专业、直接，禁止使用任何含糊的心理安慰语。"""},
    {"role": "user", "content": f"目标乾造：{birth_time}。指令：全面推演2026年风险及代偿。"}
]
                )
                st.markdown("### 📊 推演结果")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"终端连接异常: {e}")
