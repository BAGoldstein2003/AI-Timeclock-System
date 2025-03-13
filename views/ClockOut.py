import streamlit as st
from db_management import get_photo
from imageProcessing import compare

st.write("Please Clock-Out using the Facial Detection Camera below:")

clockInImg = st.camera_input(label = "")
if clockInImg:
    clockInImgRaw = clockInImg.getvalue()
    result = compare(clockInImgRaw, get_photo(st.session_state.name))
    match result:
        case 1:
            st.session_state["clocked_in"] = False
            st.session_state["clock_time"] = None
            st.success("You successfully clocked out!")
        case 0:
            st.error(f"Face did not match {st.session_state.name}'s face")
        case -1:
            st.error("Your picture does not contain a face. Please retake the picture.")