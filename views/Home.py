import streamlit as st
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
    st.session_state["clock_time"] = time.time()

#Home UI
st.title("Facial Recognition Timeclock ⏰")
if (st.session_state["logged_in"] == True):
    st.write(f"Welcome, {st.session_state["name"]}!")
    logOutButton = st.button("Log Out", icon=":material/logout:")
    if logOutButton:
        st.session_state["logged_in"] = False
        st.session_state["name"] = ""
        st.session_state["clocked_in"] = False
        st.session_state["clocked_out"] = False
        st.rerun()
else:
    st.write("Welcome! To create an account or log in, please follow the sidebar on the left!")

if st.session_state["clocked_in"]:
    clockTime = st.session_state.clock_time
    clockDisplay = st.empty()
    while True:
        currTime = time.time()
        elapsedTime = currTime - clockTime
        elapsedHours = int(elapsedTime // 3600)
        elapsedMinutes = int((elapsedTime % 3600) // 60)
        elapsedSeconds = int(elapsedTime % 60)
        elapsedToStr = f"{elapsedHours:02}:{elapsedMinutes:02}:{elapsedSeconds:02}"
        clockDisplay.text(f"Elapsed time clocked in: {elapsedToStr}")
        time.sleep(1)
