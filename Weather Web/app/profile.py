import streamlit as st
from app.users import load_users, save_users

def profile_section():
    """User profile section"""
    if not st.session_state.logged_in:
        st.error("Please login first")
        return
        
    users = load_users()
    user_data = users.get(st.session_state.user, {})
    
    st.markdown('<div class="profile-header">', unsafe_allow_html=True)
    st.markdown(f"### {user_data.get('full_name', 'User Profile')}")
    st.markdown('</div>', unsafe_allow_html=True)

    with st.form("profile_form"):
        st.markdown("**Email (verified)**")
        st.write(st.session_state.user)
        
        username = st.text_input("Username", value=user_data.get("username", ""))
        full_name = st.text_input("Full Name", value=user_data.get("full_name", ""))
        st.markdown("**Role**")
        st.write(user_data.get("role", "").capitalize())
        
        if st.form_submit_button("Update Profile"):
            user_data.update({
                "username": username,
                "full_name": full_name
            })
            users[st.session_state.user] = user_data
            save_users(users)
            st.success("Profile updated successfully!")
