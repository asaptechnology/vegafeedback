import sqlite3
import datetime

def initialize_database():
    """
    Initializes the SQLite database and the 'submissions' table if they don't exist.
    """
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    
    # SQL command to create the table with the specified schema
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            q1_name TEXT NOT NULL,
            q2_grade TEXT,
            q3_subject TEXT,
            q4_satisfaction INTEGER,
            q5_expectations INTEGER,
            q6_duration INTEGER,
            q7_recommend INTEGER,
            q8_relevance INTEGER,
            q9_clarity INTEGER,
            q10_pace INTEGER,
            q11_theory_focus INTEGER,
            q12_perspectives INTEGER,
            q13_takeaway TEXT,
            q14_ideas TEXT,
            q15_unclear TEXT,
            q16_changes TEXT,
            q17_topics TEXT,
            q18_comments TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_submission(data):
    """
    Inserts a new form submission into the database.
    :param data: A tuple containing the form data in the correct order.
    """
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    
    # SQL command to insert a new record
    c.execute('''
        INSERT INTO submissions (
            q1_name, q2_grade, q3_subject, q4_satisfaction, q5_expectations, 
            q6_duration, q7_recommend, q8_relevance, q9_clarity, q10_pace, 
            q11_theory_focus, q12_perspectives, q13_takeaway, q14_ideas, 
            q15_unclear, q16_changes, q17_topics, q18_comments
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    
    conn.commit()
    conn.close()

def get_all_submissions():
    """
    Retrieves all submissions from the database.
    :return: A list of tuples, where each tuple is a row from the database.
    """
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute("SELECT * FROM submissions ORDER BY submission_time DESC")
    records = c.fetchall()
    conn.close()
    return records

