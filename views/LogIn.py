import streamlit as st
from db_management import verify_user, create_userdb

#Create database if none
create_userdb()



#if logged in, prompt to log out
if (st.session_state["logged_in"] == True):
    st.write("Seems like you already are logged in. Please navigate to the home page and click 'log out'")

#log-in form
else:
    st.write("Please login using your credentials:")
    with st.form(key = "loginForm"):
        name = st.text_input("Full Name")
        password = st.text_input("Password", type = 'password')
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:    
            loginSubmit = st.form_submit_button("Log in", icon = ":material/login:")
        if loginSubmit:
            if verify_user(name.lower(), password):
                 st.session_state["logged_in"] = True
                 st.session_state["name"] = name
                 st.rerun()
                 st.success(f"Login successful! Welcome {name}!")

            else:
                 st.error("Invalid Name or Password!")