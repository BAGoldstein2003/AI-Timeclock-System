import streamlit as st

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
    icon=":material/hourglass_top:"
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
                "Schedule" : [schedulePage]
            }
        )
else:
    pg = st.navigation(
        {
            "Home" : [homePage],
            "Account Management" : [logInPage, signUpPage]
        }
    )

pg.run()