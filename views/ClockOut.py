import streamlit as st
from db_management import *
from imageProcessing import *
from streamlit_extras.let_it_rain import rain
from datetime import datetime

st.title("Clock-Out")
st.write("Please Clock-Out using the Facial Detection Camera below:")

#clock out feature
clockInImg = st.camera_input(label = "")
if clockInImg:
    #if clocked in, continue detecting face
    if (st.session_state.clocked_in == True):
        with st.spinner("Detecting face..."):
            clockInImgRaw = clockInImg.getvalue()
            result = compare(clockInImgRaw, get_photo(st.session_state.name))
            match result:
                case 1:
                    st.session_state["clocked_in"] = False
                    st.session_state["clockout_datetime"] = datetime.now()
                    shift = Work(
                                str(st.session_state["name"]),
                                str(st.session_state["clockin_datetime"])[:-7],
                                str(st.session_state["clockout_datetime"])[:-7]
                                )   
                    shift.save()
                    st.success("You successfully clocked out!")
                    rain(
                            emoji="✔️",
                            falling_speed=2  
                        )
                    
                case 0:
                    st.error(f"Face did not match {st.session_state.name}'s face")
                case -1:
                    st.error("Your picture does not contain a face. Please retake the picture.")
    else:
        #throw error if not clocked in
        st.error("You are not clocked in! Please clock in before trying to clock out")