import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name TEXT NOT NULL, priority INTEGER NOT NULL, task_date TEXT NOT NULL, reminder TEXT NOT NULL,
description TEXT NOT NULL, kategory TEXT NOT NULL)''')

conn.commit()
conn.close()

def add_task(name, priority, task_date, reminder, description, kategory):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (name, priority, task_date, reminder, description, kategory) VALUES (?,?,?,?,?,?)', (name, priority, task_date, reminder, description, kategory))
    conn.commit()
    conn.close()