import streamlit as st
from db_management import *
from streamlit_extras.let_it_rain import rain
import time

#Create database if none
create_userdb()



#if logged in, prompt to log out
st.title("Log In")
if (st.session_state["logged_in"] == True):
    st.write("Seems like you already are logged in. Please navigate to the home page and click 'log out'")

#log-in form
else:
    maincol1, maincol2 = st.columns(2)

    #manual login feature
    with maincol1:
        st.write("### Please login using your credentials:")
        with st.form(key = "loginForm"):
            name = st.text_input("Full Name")
            password = st.text_input("Password", type = 'password')
            formcol1, formcol2, formcol3, formcol4, formcol5 = st.columns(5)
            with formcol3:    
                loginSubmit = st.form_submit_button("Log in", icon = ":material/login:")
            if loginSubmit:
                if verify_user(name.lower(), password):
                    st.session_state["logged_in"] = True
                    st.session_state["name"] = name
                    st.success(f"Login successful! Welcome {name}!")
                    rain(
                            emoji= "✔️",
                            falling_speed= 2
                    )
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid Name or Password!")

    #facial recognition login feature
    with maincol2:
        st.write("### OR use facial recognition to log in")
        logInImg = st.camera_input("log-in image", label_visibility="collapsed")
        if logInImg:
            with st.spinner("Detecting Face..."):
                logInImgRaw = logInImg.getvalue()
                result = compare_face_to_db(logInImgRaw)
                if (result == None):
                    st.error("Your face did not match any faces in the database")
                elif (result == "not detected"):
                    st.error("No face detected in image, Clear photo and try again")
                else:
                    st.session_state["logged_in"] = True
                    st.session_state["name"] = result[0]
                    st.session_state["userType"] = result[1]
                    st.success(f"Login successful! Welcome {result[0]}!")
                    rain(
                            emoji= "✔️",
                            falling_speed= 2
                    )
                    time.sleep(2)
                    st.rerun()
            



            