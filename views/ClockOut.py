import streamlit as st
from db_management import *
from image_processing import *
from streamlit_extras.let_it_rain import rain
from datetime import datetime

st.title("Clock-Out")
st.write("Please Clock-Out using the Facial Detection Camera below:")

#clock out feature
clockOutImg = st.camera_input(label = "clock-out image", label_visibility = "collapsed")
if clockOutImg:
    #if clocked in, continue detecting face
    if (st.session_state.clocked_in == True):
        with st.spinner("Detecting Face..."):
            clockInImgRaw = clockOutImg.getvalue()
            result = compare(clockInImgRaw, get_photo(st.session_state.name))
            match result:
                case 1:
                    st.session_state["clocked_in"] = False
                    st.session_state["clockout_datetime"] = datetime.now()
                    st.session_state["shift_elapsed"] = (st.session_state["clockout_datetime"] -
                                                        st.session_state["clockin_datetime"])
                    shift = Work(
                                str(st.session_state["name"]),
                                str(st.session_state["clockin_datetime"])[:-7],
                                str(st.session_state["breakstart_datetime"])[:-7],
                                str(st.session_state["breakend_datetime"])[:-7],
                                str(st.session_state["clockout_datetime"])[:-7],
                                str(st.session_state["shift_elapsed"])[:-7],
                                str(st.session_state["break_elapsed"])[:-7]
                                )   
                    shift.save()
                    st.success("You successfully clocked out!")
                    rain(
                            emoji= "✔️",
                            falling_speed= 2  
                        )
                    
                case 0:
                    st.error(f"Face did not match {st.session_state.name}'s face")
                case -1:
                    st.error("Your picture does not contain a face. Please retake the picture.")
    else:
        #throw error if not clocked in
        st.error("You are not clocked in! Please clock in before trying to clock out")