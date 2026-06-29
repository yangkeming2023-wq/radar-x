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
    messages=[
    {"role": "system", "content": """你是一位精通《渊海子平》、《滴天髓》及人生哲学逻辑的玄学推演专家。
    输出必须严格遵守以下六大固定模块，严禁缺漏：

    1.【出厂设置】：基于八字原局分析天赋内核、性格缺陷、命局起点的底层逻辑。
    2.【人生三大真相】：结合命理运行轨迹，深刻洞察其人生必然面对的三个核心规律（如资源错位、因果演化等）。
    3.【命局诊断】：分析日主强弱、庚金食神虚实、辰戌库冲带来的财库触发机制。
    4.【2026丙午流年风险推演】：分析丙火盖头、午戌半合对财务、健康、事业的具体冲击逻辑。
    5.【每日运势详细说明】：依据日干戊土的流日五行生克，给出当下的运势吉凶与行为导向。
    6.【五行通关（冷血方案）】：基于金水制火原则，给出行业属性、行为强制、禁忌红线。

    风格：极度冷血、逻辑严密、直击要害，禁止任何温和的心理安慰，不准输出与八字无关的废话。"""},
    {"role": "user", "content": f"目标乾造：{birth_time}。指令：按出厂设置、三大真相、命局诊断、流年风险、每日运势、通关方案输出。"}
]
                )
                st.markdown("### 📊 推演结果")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"终端连接异常: {e}")
