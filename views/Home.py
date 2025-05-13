import streamlit as st
from datetime import datetime
import time

#initialize states
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "name" not in st.session_state:
    st.session_state["name"] = ""
if "clocked_in" not in st.session_state:
    st.session_state["clocked_in"] = False
if "clocked_out" not in st.session_state:
    st.session_state["clocked_out"] = False
if "clock_time" not in st.session_state:
    st.session_state["clock_time"] = None

#Home UI
st.title("Facial Recognition Timeclock ⏰")
if (st.session_state["logged_in"] == True):
    st.write('Welcome, {st.session_state["name"]}!')
    logOutButton = st.button("Log Out", icon=":material/logout:")
    if logOutButton:
        st.session_state["logged_in"] = False
        st.session_state["name"] = ""
        st.session_state["clocked_in"] = False
        st.session_state["clocked_out"] = False
        st.rerun()
else:
    st.write("Welcome! To create an account or log in, please follow the sidebar on the left!")

#if clocked in and havent started break
if st.session_state["clocked_in"]:
    if st.session_state["breakstart_datetime"] == None:
        clockTimeDisplay = st.empty()
        clockStartTime = st.session_state["clockin_datetime"]
        while True:
            elapsedShiftTime =  datetime.now() - clockStartTime
            clockTimeDisplay.text(f"Elapsed time clocked in: {str(elapsedShiftTime)[:-7]}")
            time.sleep(1)
    else:
        clockStartTime = st.session_state["clockin_datetime"]
        breakStartTime = st.session_state["breakstart_datetime"]
        clockTimeDisplay = st.empty()
        breakTimeDisplay = st.empty()
        while True:
            elapsedBreakTime = datetime.now() - breakStartTime
            elapsedShiftTime =  datetime.now() - clockStartTime
            clockTimeDisplay.text(f"Elapsed time clocked in: {str(elapsedShiftTime)[:-7]}")
            breakTimeDisplay.text(f"Elapsed time on break: {str(elapsedBreakTime)[:-7]}")
            time.sleep(1)