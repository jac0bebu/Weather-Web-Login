import streamlit as st
import os
import sys
import json

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize session state variables if they don't exist
if "logged_in" not in st.session_state:
    # Try to load from cached session
    try:
        with open('.streamlit/session.json', 'r') as f:
            session_data = json.load(f)
            st.session_state.logged_in = session_data.get('logged_in', False)
            st.session_state.user = session_data.get('user', None)
            st.session_state.role = session_data.get('role', None)
    except:
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None

from app.auth import login_section
from app.users import initialize_admin
from app.profile import profile_section
from app.admin import admin_panel

def save_session_state():
    """Save session state to file"""
    os.makedirs('.streamlit', exist_ok=True)
    session_data = {
        'logged_in': st.session_state.logged_in,
        'user': st.session_state.user,
        'role': st.session_state.role
    }
    with open('.streamlit/session.json', 'w') as f:
        json.dump(session_data, f)

def main():
    # Initialize admin
    initialize_admin()
    
    # Load CSS
    css_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'style.css')
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if not st.session_state.logged_in:
        login_section()
    else:
        # Add a logout button
        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.role = None
                # Clear saved session
                if os.path.exists('.streamlit/session.json'):
                    os.remove('.streamlit/session.json')
                st.rerun()
        
        profile_section()
        if st.session_state.role == "admin":
            admin_panel()
        
        # Save session state after successful login
        save_session_state()

if __name__ == "__main__":
    main()
