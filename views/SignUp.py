import streamlit as st
from db_management import *
from image_processing import *
import time
from streamlit_extras.let_it_rain import rain

#Create database if none
create_userdb()

st.title("Sign Up")
st.write("Please enter your desired credentials and click 'sign-up'")
with st.form(key = "signupForm"):

    #signup form contents
    name = st.text_input("Full Name").lower()
    userType = st.selectbox("User Type", ["Employee", "Manager"])
    password = st.text_input("Password", type = 'password')
    pConfirm = st.text_input("Re-enter Password", type = 'password')
    regPic = st.camera_input("Take a picture of your face for facial recognition")
    st.session_state.photo_taken = False
    

    #process image to store in image DB
    if regPic:
        with st.spinner("Detecting Face..."):
            image_bytes = regPic.getvalue()
            faceAlreadyInDB = compare_face_to_db(image_bytes)
            if faceAlreadyInDB == None:
                st.session_state.photo_taken = True
                st.success("Face successfully found in image")
            elif faceAlreadyInDB == "not detected":
                st.session_state.photo_taken = False
                st.error("No face detected in image, Clear photo and try again")
            else:
                st.session_state.photo_taken = False
                st.error("Face already detected in database. Please log in using your account!")

    #center the submit button
    col1, col2, col3, col4, col5 = st.columns(5)
    with col3:
        submit = st.form_submit_button("Sign-up", icon = "🚀")

            
    #when submit clicked
    if submit:
        if name == "" or password == "":
            st.error("Please enter your full name and a password!")
        if password != pConfirm:
            st.error("Passwords do not match!")
        if st.session_state.photo_taken == False:
            st.error("Please take a picture of your face for facial recognition!")

        #if criteria is met, check if user is employee or a manager
        elif name != "" and password != "" and st.session_state.photo_taken is True:
            if (userType == "Manager"):
                adminPass = st.text_input("Enter the Manager Password", type = 'password')
                currentPass = getAdminPass()
                if adminPass == currentPass:
                    if isUnique(name):
                        rain(
                            emoji= "✔️",
                            falling_speed= 2
                        )
                        st.session_state.logged_in = True
                        st.session_state.name = name
                        st.session_state.userType = userType
                        add_user(name, userType, password, image_bytes)
                        st.success("Account Successfully Created!")
                        time.sleep(1)
                        st.rerun() 
                    else:
                        st.error("Sorry, this name already exists!")
                else:
                    st.error("Incorrect Manager Password!")
            else:
                if isUnique(name):
                    rain(
                            emoji="✔️",
                            falling_speed=2
                        )
                    st.session_state.logged_in = True
                    st.session_state.name = name
                    st.session_state.userType = userType
                    add_user(name, userType, password, image_bytes)
                    st.success("Account Successfully Created!")
                    time.sleep(3)
                    st.rerun() 
                else:
                    st.error("Sorry, this name already exists!")
        
            
                    