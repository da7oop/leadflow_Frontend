import streamlit as st
from auth import login
from agent import run_agent
from utils import save_message, load_messages
from db import engine, Base, SessionLocal

# ---------- Streamlit ----------
st.set_page_config(page_title="AI Agent", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "username" not in st.session_state:
    st.session_state.username = ""

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #E0F7FF, #FFFFFF);
}
[data-testid="stHeader"], [data-testid="stToolbar"] {
    background: transparent;
}
textarea {
    border-radius: 14px !important;
    border: 1px solid #2563EB !important;
}
button {
    border-radius: 14px !important;
    background-color: #2563EB !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Routing ----------
if not st.session_state.logged_in:
    login()
else:
    st.session_state.messages = load_messages(st.session_state.username)

    st.markdown("""
    <div style='max-width:800px; margin:auto; padding:30px; 
                background: linear-gradient(to right, #FFFFFF, #E0F2FF); 
                border-radius:25px; box-shadow:0 15px 35px rgba(0,0,0,0.1); 
                text-align:center;'>
        <h1 style='color:#2563EB; margin-bottom:0;'>🤖 AI Agent</h1>
    </div>
    """, unsafe_allow_html=True)

    for role, content in st.session_state.messages:
        if role == "user":
            st.markdown(f"<div style='background-color:#2563EB; color:white; padding:12px 16px; border-radius:18px; margin:6px 0; max-width:70%; float:right;'>{content}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color:#F1F5FF; color:#0F172A; padding:12px 16px; border-radius:18px; margin:6px 0; max-width:70%; float:left;'>{content}</div>", unsafe_allow_html=True)

    st.markdown("<div style='clear:both'></div>", unsafe_allow_html=True)

    user_input = st.chat_input("Type your message here...")
    if user_input:
        st.session_state.messages.append(("user", user_input))
        save_message(st.session_state.username, "user", user_input)

        response = run_agent(user_input)
        st.session_state.messages.append(("assistant", response))
        save_message(st.session_state.username, "assistant", response)

        st.experimental_rerun()
