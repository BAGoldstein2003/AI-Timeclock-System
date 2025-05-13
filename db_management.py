import sqlite3
import bcrypt as bc
import pandas as pd
from dotenv import load_dotenv
import os
from pathlib import Path
import streamlit as st
from datetime import datetime
from image_processing import *

class User:
    def __init__(self, name, userType, password, image):
        self.name = name
        self.userType = userType
        self.password = password
        self.image = image
    
    def save(self):
        hashPw = bc.hashpw(self.password.encode('utf-8'), bc.gensalt())
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, userType, password, image) VALUES (?, ?, ?, ?)
        ''', (self.name, self.userType, hashPw, self.image))
        conn.commit()

class Work:
    def __init__(self, name, startTime, breakStart, breakEnd, endTime, shiftElapsed, breakElapsed):
        self.name = name 
        self.startTime = startTime
        self.breakStart = breakStart
        self.breakEnd = breakEnd
        self.endTime = endTime
        self.shiftElapsed = shiftElapsed
        self.breakElapsed = breakElapsed
    
    def save(self):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shifts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                startTime TEXT NOT NULL,
                breakStart TEXT NOT NULL,
                breakEnd TEXT NOT NULL,
                endTime TEXT NOT NULL,
                shiftElapsed TEXT NOT NULL,
                breakElapsed TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            INSERT INTO shifts (name, startTime, breakStart, breakEnd, endTime, shiftElapsed, breakElapsed) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',  (self.name, self.startTime, self.breakStart, self.breakEnd, self.endTime, self.shiftElapsed,
                self.breakElapsed
            )
        )
        conn.commit()



#Creates User Database with user table
def create_userdb():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            userType TEXT NOT NULL,
            password TEXT NOT NULL,
            image BLOB
                
        )
    ''')
    conn.commit()

def create_shiftsdb():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            startTime TEXT NOT NULL,
            breakStart TEXT NOT NULL,
            breakEnd TEXT NOT NULL,
            endTime TEXT NOT NULL,
            shiftElapsed TEXT NOT NULL,
            breakElapsed TEXT NOT NULL
        )
    ''')
    conn.commit()

def add_user(uname, userType, pword, img):
    newUser = User(uname, userType, pword, img)
    newUser.save()

def verify_user(name, pword):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
    user = cursor.fetchone()
    if user:
        stored_hash = user[3]
        if bc.checkpw(pword.encode('utf-8'), stored_hash):
            return True
    return False


def csv_to_db(csvfile):
    schedule_df = pd.read_csv(csvfile)
    reqColumns = {"name", "date", "start_time", "end_time"}
    if not reqColumns.issubset(schedule_df.columns):
        return None
    else:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        # Create the schedule table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                startTime TEXT NOT NULL,
                endTime TEXT NOT NULL,
                FOREIGN KEY (name) REFERENCES users (name)
            )
        ''')
        # Insert the schedule data into the table
        for _, row in schedule_df.iterrows():
            cursor.execute('''
            SELECT COUNT(*) FROM schedule WHERE name = ? AND date = ? AND startTime = ? AND endTime = ?
        ''', (row['name'], row['date'], row['start_time'], row['end_time']))
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO schedule (name, date, startTime, endTime) VALUES (?, ?, ?, ?)
                ''', (row['name'], row['date'], row['start_time'], row['end_time']))
            else:
                conn.close()
                return None
        conn.commit()
        conn.close()

        return schedule_df

def shifts_to_db(submitted_shifts):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Ensure the schedule table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            FOREIGN KEY (name) REFERENCES users (name)
        )
    ''')
    
    # Insert the submitted shifts into the schedule table
    for shift in submitted_shifts:
        #check for any duplicate shifts
        cursor.execute('''
            SELECT COUNT(*) FROM schedule WHERE name = ? AND date = ? AND start_time = ? AND end_time = ?
        ''', (shift['name'], str(shift['date']), str(shift['start_time']), str(shift['end_time'])))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO schedule (name, date, start_time, end_time) VALUES (?, ?, ?, ?)
            ''', (shift['name'], str(shift['date']), str(shift['start_time']), str(shift['end_time'])))
            
        else:
            conn.close()
            return False
    
    conn.commit()
    conn.close()
    return True

#converts schedule database to a pandas dataframe for display
def scheduledb_to_df():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            FOREIGN KEY (name) REFERENCES users (name)
        )
    ''')
    cursor.execute('SELECT * FROM schedule')
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows, columns=['id','name', 'date', 'start_time', 'end_time'])

def shiftsdb_to_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            startTime TEXT NOT NULL,
            breakStart TEXT NOT NULL,
            breakEnd TEXT NOT NULL,
            endTime TEXT NOT NULL,
            shiftElapsed TEXT NOT NULL,
            breakElapsed TEXT NOT NULL
        )
    ''')
    cursor.execute('SELECT * FROM shifts WHERE name = ?', (st.session_state["name"],))
    rows = cursor.fetchall()
    conn.close()
    for i, shift in enumerate(rows): 
        with st.container(border = True):
            st.write(f"### Shift {i+1}:")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"Shift {i+1} started at: {shift[2]} and lasted {shift[6]}")
            with col2:
                st.write(f"Shift {i+1} ended at: {shift[5]}")
            with col3:
                st.write(f"You took a break at {shift[3]} which lasted {shift[7]}")

def compare_face_to_db(imgblob):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, userType, image FROM users')
    for name, userType, img in cursor.fetchall():
        if compare(imgblob, img) == -1:
            return "not detected"
        if compare(imgblob, img) == 1:
            return name, userType
    conn.close()
    return None



#returns all names in the user table
def get_all_names():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM users')
    users = cursor.fetchall()
    conn.close()
    return [user[0] for user in users]

#get the logged in user's verification photo
def get_photo(uname):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE name = ?', (uname,))
    user = cursor.fetchone()
    img = user[4]
    return img

def isUnique(name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
    if cursor.fetchone():
        return False
    else:
        return True
    
#env file functions
def pathExists():
    folder = Path("secrets")
    file = folder / ".env"
    if not file.exists():
        return False
    return True

def setAdminPass(pw="admin123"):
    folder = Path("secrets")
    file = folder / ".env"
    content = f"ADMIN_PASSWORD={pw}"
    
    with open(file, "w") as f:
        f.write(content)

def getAdminPass():
    load_dotenv("secrets/.env")
    pw = os.getenv("ADMIN_PASSWORD")
    return pw