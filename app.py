import streamlit as st
from openai import OpenAI
from datetime import datetime

# 算法逻辑：根据出生时间自动计算年龄
def calculate_age(birth_date_str):
    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d %H:%M")
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except:
        return "未知"

# 核心算法：排盘数据 anchor
def get_bazi_chart_data(birth_time):
    # 这里是排盘锚定逻辑
    return """
| 项目 | 年柱 | 月柱 | 日柱 | 时柱 |
| :--- | :--- | :--- | :--- | :--- |
| 天干 | 戊 | 辛 | 丁 | 辛 |
| 地支 | 子 | 酉 | 卯 | 亥 |
| 十神 | 伤官 | 偏财 | 日主 | 偏财 |
"""

st.title("⚡ RADAR X 核心推演终端 (完全体)")

col1, col2 = st.columns(2)
with col1:
    api_key = st.text_input("DeepSeek API Key", type="password")
    gender = st.selectbox("性别", ["乾造", "坤造"])
with col2:
    birth_time = st.text_input("出生时间 (YYYY-MM-DD HH:MM)")

if st.button("执行全景推演"):
    if api_key and birth_time:
        age = calculate_age(birth_time.split()[0])
        chart_table = get_bazi_chart_data(birth_time)
        
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        
        with st.spinner(f"正在为 {age} 岁{gender}执行算法级精密推演..."):
            try:
                response = client.chat.completions.create(
                    model="deepseek-reasoner",
                    messages=[
                        {"role": "system", "content": """你是一位精通盲派命理、倪海厦逻辑及《滴天髓》的玄学推演大师。
                        输出必须严格遵守以下六大模块：
                        1.【核心排盘】：使用传入的数据构建表格。
                        2.【出厂设置】：结合[性别]与[年龄]分析天赋内核与生命阶段性特征。
                        3.【人生三大真相】：结合年龄段轨迹洞察必然规律。
                        4.【命局诊断】：基于地支刑冲破害逻辑进行体用平衡分析。
                        5.【2026丙午流年风险】：分析该年龄段面临的直接冲击逻辑。
                        6.【五行物理通关】：给出明确的物理方位、行业属性、具体时辰行为方案。
                        规则：严禁任何民俗迷信建议，风格必须极度冷血、逻辑严密。"""},
                        {"role": "user", "content": f"""
                        命主信息：{gender}，{age}岁。
                        排盘数据：{chart_table}
                        请基于上述命局与年龄背景，严格执行推演。
                        """}
                    ]
                )
                st.markdown("### 📊 八字排盘数据")
                st.write(chart_table)
                st.markdown(f"### 📊 Radar X 核心推演 ({gender} / {age}岁)")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"引擎异常: {e}")
