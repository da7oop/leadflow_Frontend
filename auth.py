import streamlit as st
from db import SessionLocal, User

def register_user(username, password):
    with SessionLocal() as db:
        if not db.query(User).filter(User.username == username).first():
            new_user = User(username=username, password=password)
            db.add(new_user)
            db.commit()

def check_login(username, password):
    with SessionLocal() as db:
        return db.query(User).filter(User.username == username, User.password == password).first()

def login():
    st.markdown("""
    <div style='max-width:380px; margin:auto; padding:35px; border-radius:18px;
                background:#F8FAFF; box-shadow:0 10px 25px rgba(0,0,0,0.05); text-align:center;'>
        <h3>🔐 Login</h3>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            if username and password:
                user = check_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                else:
                    st.error("❌ Invalid username or password")
    with col2:
        if st.button("Register"):
            register_user(username, password)
            st.success("✅ User registered. Please login.")
