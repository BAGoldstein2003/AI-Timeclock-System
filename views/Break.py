import streamlit as st
from datetime import datetime
from db_management import get_photo
from image_processing import compare
import time

st.title("Take a Break")
st.write("Scan your face to start/conclude your break!")

#if user is not clocked in, throw error
if (st.session_state.clocked_in == False):
    st.error("You must be clocked in to use this feature!")
#if user is clocked in, process image and handle output
else:
    breakImg = st.camera_input("break image", label_visibility = "collapsed")
    #if photo is taken
    if breakImg:
        #if user is clocked in and break has not been started
        if (st.session_state.breakstart_datetime == None):
            with st.spinner("Detecting Face"):
                breakImgRaw = breakImg.getvalue()
                result = compare(breakImgRaw, get_photo(st.session_state.name))
                match result:
                    case 1:
                        st.session_state["breakstart_datetime"] = datetime.now()
                        st.success("You have successfully started your break! Enjoy!")
        elif (st.session_state.breakstart_datetime != None):
            with st.spinner("Detecting Face"):
                breakImgRaw = breakImg.getvalue()
                result = compare(breakImgRaw, get_photo(st.session_state.name))
                match result:
                    case 1:
                        st.session_state["breakend_datetime"] = datetime.now()
                        st.session_state["break_elapsed"] = (st.session_state["breakend_datetime"] -
                                                             st.session_state["breakstart_datetime"]
                                                            )
                        st.success("You have successfully concluded your break!")
                        time.sleep(2)
                        st.rerun()
