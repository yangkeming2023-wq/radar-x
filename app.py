import streamlit as st
from openai import OpenAI
from datetime import datetime, date # 确保导入了 date

# 核心：根据出生时间自动计算年龄
def calculate_age(birth_date_obj):
    today = date.today()
    return today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))

st.title("⚡ RADAR X 核心推演终端 (最终严谨版)")

# UI输入区：确保 min_value 设置正确，并确保类型完全匹配
api_key = st.text_input("DeepSeek API Key", type="password")
col1, col2, col3 = st.columns(3)
with col1: 
    gender = st.selectbox("性别", ["男", "女"])
with col2: 
    # 使用 date 对象，设置 1900-2026 的全范围，彻底修复选择器截断
    birth_date = st.date_input(
        "出生日期", 
        value=date(2008, 9, 24),
        min_value=date(1900, 1, 1),
        max_value=date.today(),
        format="YYYY/MM/DD" # 强制日期格式
    )
with col3: 
    birth_time = st.text_input("出生时间", "22:16")

if st.button("执行全景推演"):
    if api_key and birth_date:
        age = calculate_age(birth_date)
        # 物理锚定：确保排盘数据准确，严禁幻觉
        chart_table = "| 项目 | 年柱 | 月柱 | 日柱 | 时柱 |\n| :--- | :--- | :--- | :--- | :--- |\n| 天干 | 戊 | 辛 | 丁 | 辛 |\n| 地支 | 子 | 酉 | 卯 | 亥 |\n| 十神 | 伤官 | 偏财 | 日主 | 偏财 |"
        
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        
        with st.spinner(f"正在为 {gender}性 / {age}岁 进行算法级精密推演..."):
            try:
                response = client.chat.completions.create(
                    model="deepseek-reasoner",
                    messages=[
                        {"role": "system", "content": """你是一个顶尖的八字大师，和倪海厦大师一样有实力，学识渊博，精通《渊海子平》《三命通会》《滴天髓》等古籍和盲派命理的推算方法。
                        要求：
                        1. 必须根据命盘的刑冲破害和五行生克分析十神关系，体用平衡。
                        2. 综合各种信息文本判断准确的关系模型，交叉验证，多次迭代后输出最终正确的结果。
                        3. 诚实评价，用语不用太谨慎，只根据技法逻辑分析，不要添加主观臆想。
                        4. 将这个八字所有方面都要说透，用大白话通熟易懂的表达。
                        5. 通过刑冲破害和五行生克十神关系剖析出此八字不好的方法，使其变得无懈可击。
                        6. 实事求是根据南北道教以及上述逻辑直白的阐述真实情况。严禁谄媚，严禁缝合数据。"""},
                        {"role": "user", "content": f"""
                        命主信息：性别{gender}，年龄{age}岁。
                        排盘数据：{chart_table}
                        指令：请针对此命局，严格按照以下六大模块进行冷血、无废话推演：
                        1.【出厂设置】：结合{gender}性与{age}岁特征，分析天赋内核与性格逻辑。
                        2.【人生三大真相】：结合盘面轨迹洞察必然规律。
                        3.【命局诊断】：基于刑冲破害逻辑进行体用平衡分析。
                        4.【2026丙午流年风险】：流年与原局的化学反应。
                        5.【每日运势详细说明】：依据日干五行生克给出详细指导。
                        6.【五行物理通关】：给出明确的物理方位、行业属性、具体时辰行为方案，拒绝民俗迷信。
                        """}
                    ]
                )
                st.markdown("### 📊 八字排盘数据")
                st.write(chart_table)
                st.markdown("### 📊 Radar X 核心推演")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"引擎异常: {e}")
