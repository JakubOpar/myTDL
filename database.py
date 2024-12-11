import sqlite3
import re
from datetime import datetime

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name TEXT NOT NULL, priority INTEGER NOT NULL, task_date TEXT NOT NULL, reminder TEXT NOT NULL,
description TEXT NOT NULL, kategory TEXT NOT NULL)''')

conn.commit()
conn.close()

def validate_datetime_format(date_str):
    try:
        datetime.strptime(date_str, '%d-%m-%Y %H %M')
        return True
    except ValueError:
        return False


def add_task(name, priority, task_date, reminder, description, kategory):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (name, priority, task_date, reminder, description, kategory) VALUES (?,?,?,?,?,?)', (name, priority, task_date, reminder, description, kategory))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(id, name = None, priority = None, task_date = None, reminder = None, description = None, kategory = None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    updates = []
    parameters = []

    if name:
        updates.append(name)
        parameters.append(name)
    if priority:
        updates.append(priority)
    if task_date:
        if not validate_datetime_format(task_date): raise ValueError(f"Podano zły format daty i czasu! {task_date} Oczekiwano: dd-mm-yyyy hh24:mi")
        updates.append(task_date)
        parameters.append(task_date)


