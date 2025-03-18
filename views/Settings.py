from dotenv import load_dotenv
from pathlib import Path
import os
import streamlit as st
import time
from db_management import *


st.title("Settings")
with st.form(key="Settings Form"):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col3:
        
        st.write("### Change Manager Password")
        passVerify = st.text_input("Old Manager Password", type="password")
        newPass = st.text_input("New Manager Password")
        submit = st.form_submit_button("Submit Changes", icon="🔒")
        if submit:
            if passVerify == getAdminPass():
                if newPass != "":
                    setAdminPass(newPass)
                    st.success("Password successfully changed! *RESTART THE STREAMLIT SERVER TO APPLY CHANGES*")
                else:
                    st.error("Password must not be empty!")
            else:
                st.error("Incorrect password!")



