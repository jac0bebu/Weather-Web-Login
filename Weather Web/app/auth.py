import streamlit as st
from app.users import load_users, check_password

def login_section():
    """Login section"""
    st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem !important;
        }
        
        .stTitle {
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        
        .login-form {
            max-width: 400px;
            margin: 2rem auto;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: var(--shadow-md);
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Weather Web Login 🌦️")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            if not email or not password:
                st.error("Please fill in all fields!")
                return
                
            users = load_users()
            if email in users and check_password(password, users[email]["password"]):
                st.session_state.logged_in = True
                st.session_state.user = email
                st.session_state.role = users[email]["role"]
                # Save session immediately after successful login
                from app.main import save_session_state
                save_session_state()
                st.rerun()
            else:
                st.error("Invalid credentials")
