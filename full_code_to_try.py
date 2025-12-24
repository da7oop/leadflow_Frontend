```python
!pip install streamlit sqlalchemy pyngrok --quiet

import streamlit as st
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pyngrok import ngrok
import os

DATABASE_URL = "sqlite:///./chat_app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    role = Column(String)
    content = Column(String)

Base.metadata.create_all(bind=engine)

def save_message(username, role, content):
    with SessionLocal() as db:
        db.add(Lead(username=username, role=role, content=content))
        db.commit()

def load_messages(username):
    with SessionLocal() as db:
        return [(m.role, m.content) for m in db.query(Lead).filter(Lead.username == username).all()]

def register_user(username, password):
    with SessionLocal() as db:
        if not db.query(User).filter(User.username == username).first():
            db.add(User(username=username, password=password))
            db.commit()

def check_login(username, password):
    with SessionLocal() as db:
        return db.query(User).filter(User.username == username, User.password == password).first()

def run_agent(text):
    return f"This is a response to: {text}"

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
    background: linear-gradient(135deg, #E0F2FF, #FFFFFF);
}
[data-testid="stHeader"], [data-testid="stToolbar"] {
    background: transparent;
}
.chat-box {
    max-width: 800px;
    margin: auto;
    background: linear-gradient(135deg, #FFFFFF, #E0F2FF);
    padding: 30px;
    border-radius: 25px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
}
.user-msg {
    background:#2563EB;
    color:white;
    padding:12px 16px;
    border-radius:18px;
    margin:8px 0;
    text-align:right;
}
.ai-msg {
    background:#F1F5FF;
    color:#0F172A;
    padding:12px 16px;
    border-radius:18px;
    margin:8px 0;
    text-align:left;
}
button {
    border-radius:14px !important;
    background:#2563EB !important;
    color:white !important;
}
textarea {
    border-radius:14px !important;
}
</style>
""", unsafe_allow_html=True)

def login_page():
    st.markdown("<h2 style='text-align:center;color:#2563EB'>AI Agent</h2>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Login"):
            if check_login(u, p):
                st.session_state.logged_in = True
                st.session_state.username = u
            else:
                st.error("Invalid credentials")
    with c2:
        if st.button("Register"):
            register_user(u, p)
            st.success("Registered")

def chat_page():
    st.session_state.messages = load_messages(st.session_state.username)
    st.markdown("<div class='chat-box'><h1 style='color:#2563EB;text-align:center'>🤖 AI Agent</h1>", unsafe_allow_html=True)
    for r, c in st.session_state.messages:
        if r == "user":
            st.markdown(f"<div class='user-msg'>{c}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-msg'>{c}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    msg = st.chat_input("Type your message here...")
    if msg:
        save_message(st.session_state.username, "user", msg)
        save_message(st.session_state.username, "assistant", run_agent(msg))
        st.experimental_rerun()

if not st.session_state.logged_in:
    login_page()
else:
    chat_page()

url = ngrok.connect(8501)
print("Public URL:", url)
!streamlit run /content/{os.path.basename(__file__)} --server.port 8501
```
