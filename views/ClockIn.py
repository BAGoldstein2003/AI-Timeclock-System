import streamlit as st
from db_management import *
from image_processing import *
from datetime import datetime
from streamlit_extras.let_it_rain import rain

st.title("Clock-In")
st.write("Please Clock-In using the Facial Detection Camera below:")
clockInImg = st.camera_input(label = "clock-in image", label_visibility = "collapsed")
if clockInImg:
    if (st.session_state.clocked_in == False):
        with st.spinner("Detecting Face..."):
            clockInImgRaw = clockInImg.getvalue()
            result = compare(clockInImgRaw, get_photo(st.session_state.name))
            match result:
                case 1:
                    st.session_state["clocked_in"] = True
                    st.session_state["breakstart_datetime"] = None
                    st.session_state["breakend_datetime"] = None
                    st.session_state["clockin_datetime"] = datetime.now()
                    st.session_state["clockout_datetime"] = "pending"
                    st.success("You successfully clocked in!")
                    rain(
                            emoji= "✔️",
                            falling_speed= 2
                        )
                case 0:
                    st.error(f"Face did not match {st.session_state.name}'s face")
                case -1:
                    st.error("Your picture does not contain a face. Please retake the picture.")
    else:
        st.error("You are already clocked in!")
