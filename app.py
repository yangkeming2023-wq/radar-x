import streamlit as st
from openai import OpenAI
from datetime import datetime, date
from lunar_python import Solar

# 核心：计算年龄
def calculate_age(birth_date_obj):
    today = date.today()
    return today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))

# 核心：动态排盘算法
def get_bazi_chart_data(birth_date, time_str):
    hour = int(time_str.split(':')[0])
    solar = Solar.fromYmdHms(birth_date.year, birth_date.month, birth_date.day, hour, 0, 0)
    bazi = solar.getLunar().getEightChar()
    return f"""
| 项目 | 年柱 | 月柱 | 日柱 | 时柱 |
| :--- | :--- | :--- | :--- | :--- |
| 天干 | {bazi.getYearGan()} | {bazi.getMonthGan()} | {bazi.getDayGan()} | {bazi.getTimeGan()} |
| 地支 | {bazi.getYearZhi()} | {bazi.getMonthZhi()} | {bazi.getDayZhi()} | {bazi.getTimeZhi()} |
"""

st.title("⚡ RADAR X 核心推演终端 (最终严谨版)")

# --- 安全 API 调用逻辑 (从云端读取，不再硬编码) ---
api_key = st.secrets["DEEPSEEK_API_KEY"]
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
# -----------------------------------------------

col1, col2, col3 = st.columns(3)
with col1: gender = st.selectbox("性别", ["男", "女"])
with col2: 
    birth_date = st.date_input("出生日期", value=date(2008, 9, 24), min_value=date(1900, 1, 1), format="YYYY/MM/DD")
with col3: birth_time = st.text_input("出生时间", "22:16")

if st.button("执行全景推演"):
    if birth_date:
        age = calculate_age(birth_date)
        chart_table = get_bazi_chart_data(birth_date, birth_time)
        
        st.markdown("### 📊 八字排盘数据")
        st.write(chart_table)
        st.markdown("### 📊 Radar X 核心推演")
        
        placeholder = st.empty()
        full_response = ""
        
        try:
            stream = client.chat.completions.create(
                model="deepseek-chat",
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
                    1.【出厂设置】：结合{gender}与{age}岁特征，分析天赋内核与性格逻辑。
                    2.【人生三大真相】：结合盘面轨迹洞察必然规律。
                    3.【命局诊断】：基于刑冲破害逻辑进行体用平衡分析。
                    4.【2026丙午流年风险】：流年与原局的化学反应。
                    5.【每日运势详细说明】：依据日干五行生克给出详细指导。
                    6.【五行物理通关】：给出明确的物理方位、行业属性、具体时辰行为方案，拒绝民俗迷信。
                    """}
                ],
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"引擎异常: {e}")
