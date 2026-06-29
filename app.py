import streamlit as st
from openai import OpenAI
from bazi_engine import get_bazi_chart # 导入上面的物理引擎

st.title("⚡ RADAR X 核心推演终端 (算法版)")
api_key = st.text_input("输入 DeepSeek API Key", type="password")
birth_time = st.text_input("出生时间 (例: 1990-05-03 20:03)")

if st.button("执行扫描"):
    if api_key and birth_time:
        # 1. 物理计算排盘（由 bazi_engine 保证数据绝对客观）
        chart_table = get_bazi_chart(birth_time)
        
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        
        with st.spinner("正在进行算法排盘与深度推演..."):
            try:
                response = client.chat.completions.create(
                    model="deepseek-reasoner",
                    messages=[
                        {"role": "system", "content": "你是一位玄学推演专家。"},
                        {"role": "user", "content": f"""
                        以下是【绝对客观】的八字排盘数据：
                        {chart_table}
                        
                        请严禁重算八字，必须完全基于上述数据，按照以下模块输出：
                        1.【出厂设置】...
                        2.【人生三大真相】...
                        3.【命局诊断】...
                        4.【2026丙午流年风险】...
                        5.【每日运势】...
                        6.【五行通关】...
                        """}
                    ]
                )
                st.markdown("### 📊 八字排盘数据")
                st.write(chart_table) # 先显示算法算出来的表
                st.markdown("### 📊 Radar X 核心推演")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"引擎异常: {e}")
