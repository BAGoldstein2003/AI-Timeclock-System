import streamlit as st
from db_management import pathExists, setAdminPass


st.set_page_config(
    layout="wide"
)


#initialize states
if ("logged_in" not in st.session_state):
    st.session_state["logged_in"] = False
    st.session_state["userType"] = ""

#page setup
homePage = st.Page(
    page= "views/Home.py",
    title="Home",
    icon=":material/home:",
    default=True
)

clockInPage = st.Page(
    page= "views/ClockIn.py",
    title= "Clock-In",
    icon=":material/hourglass_top:",
)

clockOutPage = st.Page(
    page= "views/ClockOut.py",
    title= "Clock-Out",
    icon=":material/hourglass_bottom:"
)

logInPage = st.Page(
    page= "views/LogIn.py",
    title= "Log-In",
    icon=":material/login:"
)

signUpPage = st.Page(
    page= "views/SignUp.py",
    title= "Sign-Up",
    icon=":material/person_add:"
)

schedulePage = st.Page(
    page= "views/workSchedule.py",
    title= "Manage Schedule",
    icon = ":material/schedule:"
)

settingsPage = st.Page(
    page= "views/Settings.py",
    title= "Settings",
    icon = ":material/settings:"
)



#navbar setup
if (st.session_state["logged_in"] == True):
    if (st.session_state["userType"] == "Employee"):
        pg = st.navigation(
        {
            "Home" : [homePage],
            "Account Management" : [logInPage, signUpPage],
            "Time Card" : [clockInPage, clockOutPage]
        }
    )
    else:
        pg = st.navigation(
            {
                "Home" : [homePage],
                "Account Management" : [logInPage, signUpPage],
                "Time Card" : [clockInPage, clockOutPage],
                "Schedule" : [schedulePage],
                "Settings" : [settingsPage]
            }
        )
else:
    pg = st.navigation(
        {
            "Home" : [homePage],
            "Account Management" : [logInPage, signUpPage]
        }
    )

#create an env file containing the global admin pass if none exists
if not pathExists():
    setAdminPass()

#runs the app
pg.run()