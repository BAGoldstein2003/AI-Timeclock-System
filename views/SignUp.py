import streamlit as st
from db_management import *
from imageProcessing import *

#Create database if none
create_userdb()

st.write("Please enter your desired credentials and click 'sign-up'")
with st.form(key = "signupForm"):

    #signup form contents
    name = st.text_input("Full Name").lower()
    password = st.text_input("Password", type = 'password')
    pConfirm = st.text_input("Re-enter Password", type = 'password')
    if "photo_taken" not in st.session_state:
        detection = False
        st.session_state.photo_taken = False
    regPic = st.camera_input("Take a picture of your face for facial recognition")

    #process image to store in image DB
    if regPic:
        image_bytes = regPic.getvalue()
        detection = detected(image_bytes)
        if detection:
            st.session_state.photo_taken = True
            st.success("Face successfully found in image")
        else:
            st.session_state.photo_taken = False
            st.error("No face detected in image, Clear photo and try again")
            
    submit = st.form_submit_button("Sign-up", icon = "🚀")

            
    #when submit clicked
    if submit:
        if name == "" or password == "":
            st.error("Please enter your full name and a password!")
        if password != pConfirm:
            st.error("Passwords do not match!")
        #if criteria is met, submit form
        elif name is not "" and password is not "" and st.session_state.photo_taken is True:
            if isUnique(name):
                st.session_state.logged_in = True
                st.session_state.name = name
                add_user(name, password, image_bytes)
                st.success("Account Successfully Created!")
                st.rerun()  
            else:
                st.error("Sorry, this name already exists!")
                    