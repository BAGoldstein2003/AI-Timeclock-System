import streamlit as st
import pandas as pd
import sqlite3
from db_management import csv_to_db, shifts_to_db, get_all_names, db_to_df
from datetime import datetime
import time


#initialize shift states
if "shifts" not in st.session_state:
    st.session_state.shifts = [{"username": "", "date": "", "start_time": "", "end_time": ""}]
    st.session_state.input_changed = False
    st.session_state.submitted_shifts = []

#function for submitting shifts

        

def add_shift():
    st.session_state.shifts.append({"name": "", "date": "", "start_time": "", "end_time": ""})
    st.rerun()


#static UI elements
st.title("Manage Schedule")
st.write("### Current Schedule:")
st.dataframe(db_to_df(), hide_index = True)
maincol1, maincol2 = st.columns(2, border = True)
with maincol1:
    st.write("### Import a Schedule File:")
    st.write("Please upload a CSV file with the following columns:")
    st.write("name, date, start_time, end_time")
    st.write("The file should contain the schedule for all users")

    #shift upload module
    scheduleFile = st.file_uploader("Choose a CSV file", type="csv")
    if scheduleFile is not None:
        schedule_df = csv_to_db(scheduleFile)
        if schedule_df is not None:
            schedule_df['date'] = pd.to_datetime(schedule_df['date'])
            schedule_df['start_time'] = pd.to_datetime(schedule_df['start_time'], format='%H:%M').dt.time
            schedule_df['end_time'] = pd.to_datetime(schedule_df['end_time'], format='%H:%M').dt.time
            schedule_df = schedule_df.sort_values(by=['name', 'date', 'start_time'])

            st.write("Uploaded Schedule:")
            st.dataframe(schedule_df)
        else:
            st.error("Error: Invalid CSV file OR duplicate shifts found")

#manual shift management module
with maincol2:
    st.write("### OR manually enter the shifts below:")
    st.write("")

    for i, shift in enumerate(st.session_state.shifts):
        with st.container(border = True):
            st.write(f"### Shift {i+1}")
            formcol1, formcol2, formcol3, formcol4= st.columns(4, border = True)
            with formcol1:
                shift["name"] = st.selectbox(f"Name {i+1}", get_all_names(), key=f"Name_{i}")
            with formcol2:
                shift["date"] = st.date_input(f"Date {i+1}", key=f"date_{i}", min_value=datetime.today().date())
            with formcol3:
                shift["start_time"] = st.time_input(f"Start Time {i+1}", key=f"start_{i}")
            with formcol4:
                shift["end_time"] = st.time_input(f"End Time {i+1}", key=f"end_{i}")

    #Buttons for adding or deleting shifts
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Another Shift"):
            add_shift()

    with col2:
        if st.button("Delete recent Shift"):
            if (len(st.session_state.shifts) > 0):
                st.session_state.shifts.pop()
            else:
                st.error("You can't delete non-existent shifts!")
                time.sleep(1)
            st.rerun()




    submitManual = st.button("Submit Shifts")

    def submit_shifts():
        st.session_state.input_changed = False
        st.session_state.submitted_shifts = st.session_state.shifts
        if (shifts_to_db(st.session_state.submitted_shifts)):
            st.success("Shifts submitted successfully!")
            st.rerun()
        else:
            st.error("Error submitting shifts: duplicate shifts found")
    
    if submitManual:
        submit_shifts()
    

st.write("")

