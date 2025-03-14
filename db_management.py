import sqlite3
import bcrypt as bc
import pandas as pd
from dotenv import load_dotenv
import os
from pathlib import Path

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
    def __init__(self, startTime, endTime):
        self.startTime = startTime
        self.endTime = endTime


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

def add_user(uname, userType, pword, img):
    newUser = User(uname, userType, pword, img)
    newUser.save()

def verify_user(name, pword):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
    user = cursor.fetchone()
    if user:
        stored_hash = user[2]
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
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                FOREIGN KEY (name) REFERENCES users (name)
            )
        ''')
        # Insert the schedule data into the table
        for _, row in schedule_df.iterrows():
            cursor.execute('''
            SELECT COUNT(*) FROM schedule WHERE name = ? AND date = ? AND start_time = ? AND end_time = ?
        ''', (row['name'], row['date'], row['start_time'], row['end_time']))
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO schedule (name, date, start_time, end_time) VALUES (?, ?, ?, ?)
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
        ''', (shift['name'], str(shift['date']), str(shift['start_time'])[:-3], str(shift['end_time'])[:-3]))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO schedule (name, date, start_time, end_time) VALUES (?, ?, ?, ?)
            ''', (shift['name'], str(shift['date']), str(shift['start_time'])[:-3], str(shift['end_time'])[:-3]))
        else:
            conn.close()
            return False
    
    conn.commit()
    conn.close()
    return True

#converts schedule database to a pandas dataframe for display
def db_to_df():
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
