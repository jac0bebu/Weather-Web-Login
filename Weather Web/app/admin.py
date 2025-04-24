import streamlit as st
from app.users import load_users, save_users, hash_password

def admin_panel():
    """Admin panel with user management"""
    st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
    
    # Create User Section
    st.markdown("### 👥 Create New User")
    
    with st.form("create_user"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["reporter", "coordinator"])
        
        if st.form_submit_button("Create User"):
            users = load_users()
            if email in users:
                st.error("User already exists!")
                return
                
            users[email] = {
                "password": hash_password(password),
                "role": role,
                "username": "",
                "full_name": ""
            }
            save_users(users)
            st.success(f"{role.capitalize()} account created successfully!")

    # User Management Section
    st.markdown("### 📊 User Management")
    
    users = load_users()
    
    # Create tabs for different roles
    tabs = st.tabs(["Reporters", "Coordinators"])
    
    with tabs[0]:
        st.markdown("#### Reporter Accounts")
        reporters = {email: data for email, data in users.items() 
                    if data["role"] == "reporter"}
        
        if reporters:
            for email, data in reporters.items():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**Email:** {email}")
                with col2:
                    st.write(f"**Name:** {data['full_name'] or data['username'] or 'N/A'}")
                with col3:
                    if st.button("Delete", key=f"del_reporter_{email}"):
                        del users[email]
                        save_users(users)
                        st.rerun()
                st.divider()
        else:
            st.info("No reporter accounts found")

    with tabs[1]:
        st.markdown("#### Coordinator Accounts")
        coordinators = {email: data for email, data in users.items() 
                       if data["role"] == "coordinator"}
        
        if coordinators:
            for email, data in coordinators.items():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**Email:** {email}")
                with col2:
                    st.write(f"**Name:** {data['full_name'] or data['username'] or 'N/A'}")
                with col3:
                    if st.button("Delete", key=f"del_coord_{email}"):
                        del users[email]
                        save_users(users)
                        st.rerun()
                st.divider()
        else:
            st.info("No coordinator accounts found")

    st.markdown('</div>', unsafe_allow_html=True)
