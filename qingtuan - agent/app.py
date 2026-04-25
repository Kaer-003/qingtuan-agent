import streamlit as st
from openai import OpenAI
import os

# -------------------------- 配置区（从环境变量读取） --------------------------
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.moonshot.cn/v1"  # Kimi改为https://api.moonshot.cn/v1
MODEL = "moonshot-v1-8k"  # Kimi改为moonshot-v1-8k
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """
你是共青团志愿服务智能助手，积极向上、青春正能量。
擅长：志愿活动文案、策划方案、宣传口号、活动通知、文明引导语。
语气正式得体，充满青年朝气，不讨论无关敏感内容。
"""

# 页面配置
st.set_page_config(
    page_title="青团志愿服务助手",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 极简兼容CSS（避免前端渲染报错）
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
    }
    .main-title {
        color: #2E7D32;
        font-size: 2.2rem;
        font-weight: bold;
        text-align: center;
        margin: 2rem 0 0.5rem 0;
    }
    .subtitle {
        color: #4CAF50;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .intro {
        color: #388E3C;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #81C784;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #66BB6A;
    }
</style>
""", unsafe_allow_html=True)

# 页面标题
st.markdown('<div class="main-title">💚 共青团志愿服务助手</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">青春心向党 · 志愿建新功</div>', unsafe_allow_html=True)
st.markdown('<div class="intro">📚 为青年志愿服务提供文案、策划、宣传等智能支持</div>', unsafe_allow_html=True)

# 快捷按钮
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📝 写宣传文案", use_container_width=True):
        st.session_state.prompt = "帮我写一段社区志愿活动宣传文案"
with col2:
    if st.button("📋 做活动方案", use_container_width=True):
        st.session_state.prompt = "帮我设计图书馆志愿活动方案"
with col3:
    if st.button("📢 想宣传标语", use_container_width=True):
        st.session_state.prompt = "帮我写5条志愿活动宣传标语"
with col4:
    if st.button("📜 写活动通知", use_container_width=True):
        st.session_state.prompt = "帮我写社区志愿活动通知"

# 初始化对话
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 显示历史消息
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 输入框
prompt = st.chat_input("请输入你的问题，例如：帮我写一段志愿活动文案")
if not prompt and "prompt" in st.session_state:
    prompt = st.session_state.prompt
    del st.session_state.prompt

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("正在生成回答..."):
            try:
                client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=1024
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"生成失败：{str(e)}")