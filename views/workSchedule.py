import streamlit as st
import pandas as pd
import sqlite3
from db_management import *
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

def delete_shifts():
    delButton = st.button("Delete Already-Made Shifts")
    if delButton:
        with st.form():
            select = st.selectbox(label="Select a shift to delete")

def submit_shifts():
    st.session_state.submitted_shifts = st.session_state.shifts
    submitted = shifts_to_db(st.session_state.submitted_shifts)
    if (submitted):
        st.success("Shifts submitted successfully!")
        time.sleep(1)
        st.rerun()
    else:
        st.error("Error submitting shifts: duplicate shifts found")

#static UI elements
st.title("Manage Schedule")
st.write("### Current Schedule:")
st.dataframe(scheduledb_to_df(), hide_index = True)
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
            schedule_df = schedule_df.sort_values(by=['date', 'start_time', 'name'])

            st.write("Uploaded Schedule:")
            st.dataframe(schedule_df)
            st.success("Successfully entered shifts!")
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
        if st.button("Delete last Shift"):
            if (len(st.session_state.shifts) > 0):
                st.session_state.shifts.pop()
            else:
                st.error("You can't delete non-existent shifts!")
                time.sleep(1)
            st.rerun()

    submitManual = st.button("Submit Shifts")
    if submitManual:
        submit_shifts()