import streamlit as st
from db_management import *

#create databases
create_userdb()
create_shiftsdb()

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

clockHistoryPage = st.Page(
    page="views/ClockHistory.py",
    title= "Clock History",
    icon= ":material/history:"
)

breakPage = st.Page(
    page= "views/Break.py",
    title= "Take Break",
    icon= ":material/pause_circle:"
)



#navbar setup
if (st.session_state["logged_in"] == True):
    if (st.session_state["userType"] == "Employee"):
        #if user is an employee
        pg = st.navigation(
        {
            "Home" : [homePage],
            "Account Management" : [logInPage, signUpPage],
            "Time Card" : [clockInPage, breakPage, clockOutPage, clockHistoryPage]
        }
    )
    elif (st.session_state["userType"] == "Manager"):
        #if user is a manager
        pg = st.navigation(
            {
                "Home" : [homePage],
                "Account Management" : [logInPage, signUpPage],
                "Time Card" : [clockInPage, breakPage, clockOutPage, clockHistoryPage],
                "Schedule" : [schedulePage],
                "Settings" : [settingsPage]
            }
        )
else:
    #if user is not logged in
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