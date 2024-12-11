import sqlite3
from datetime import datetime


def initialize_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Tworzenie tabel (jeśli jeszcze nie istnieją)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT NOT NULL,
            priority INTEGER NOT NULL,
            task_date TEXT NOT NULL,
            reminder TEXT NOT NULL,
            description TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
        )
    ''')

    # Dodanie kategorii "default" (jeśli jeszcze nie istnieje)
    cursor.execute('''
        INSERT OR IGNORE INTO categories (name) VALUES ('default')
    ''')

    conn.commit()
    conn.close()
    print("Baza danych zainicjowana, kategoria 'default' dodana.")



# Walidacja formatu daty
def validate_datetime_format(date_str):
    try:
        datetime.strptime(date_str, '%d-%m-%Y %H:%M')
        return True
    except ValueError:
        return False


# Walidacja priorytetu
def validate_priority(priority):
    if not isinstance(priority, int) or priority < 1 or priority > 5:
        raise ValueError("Priorytet musi być liczbą całkowitą w zakresie od 1 do 5.")


# Dodawanie kategorii
def add_category(name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError(f"Kategoria o nazwie '{name}' już istnieje.")
    finally:
        conn.close()


# Usuwanie kategorii
def delete_category(category_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
    category = cursor.fetchone()

    if not category:
        conn.close()
        raise ValueError(f"Kategoria '{category_name}' nie istnieje.")

    cursor.execute('DELETE FROM categories WHERE id = ?', (category[0],))

    conn.commit()
    conn.close()


# Pobieranie wszystkich kategorii
def get_categories():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    conn.close()
    return categories


# Dodawanie zadania
def add_task(name, priority, task_date, reminder, description, category_name):
    if not validate_datetime_format(task_date):
        raise ValueError(f"Błędny format task_date: {task_date}. Oczekiwany format: dd-mm-yyyy hh24:mi")
    if not validate_datetime_format(reminder):
        raise ValueError(f"Błędny format reminder: {reminder}. Oczekiwany format: dd-mm-yyyy hh24:mi")
    validate_priority(priority)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Znalezienie lub dodanie kategorii
    cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
    category = cursor.fetchone()
    if not category:
        raise ValueError(f"Kategoria '{category_name}' nie istnieje. Dodaj kategorię przed dodaniem zadania.")

    category_id = category[0]

    cursor.execute('''
        INSERT INTO tasks (name, priority, task_date, reminder, description, category_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, priority, task_date, reminder, description, category_id))

    conn.commit()
    conn.close()


# Pobieranie wszystkich zadań
def get_tasks(order_by="priority"):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if order_by not in ["priority", "task_date", "name"]:
        raise ValueError("Sortowanie może być według: 'priority', 'task_date', 'name'.")
    cursor.execute('''
        SELECT tasks.id, tasks.name, tasks.priority, tasks.task_date, tasks.reminder, tasks.description, categories.name 
        FROM tasks
        JOIN categories ON tasks.category_id = categories.id
        ORDER BY tasks.{}
    '''.format(order_by))
    tasks = cursor.fetchall()
    conn.close()
    return tasks


# Aktualizacja zadania
def update_task(task_id, name=None, priority=None, task_date=None, reminder=None, description=None, category_name=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    updates = []
    parameters = []

    if name:
        updates.append("name = ?")
        parameters.append(name)
    if priority:
        validate_priority(priority)
        updates.append("priority = ?")
        parameters.append(priority)
    if task_date:
        if not validate_datetime_format(task_date):
            raise ValueError(f"Błędny format task_date: {task_date}. Oczekiwany format: dd-mm-yyyy hh24:mi")
        updates.append("task_date = ?")
        parameters.append(task_date)
    if reminder:
        if not validate_datetime_format(reminder):
            raise ValueError(f"Błędny format reminder: {reminder}. Oczekiwany format: dd-mm-yyyy hh24:mi")
        updates.append("reminder = ?")
        parameters.append(reminder)
    if description:
        updates.append("description = ?")
        parameters.append(description)
    if category_name:
        cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
        category = cursor.fetchone()
        if not category:
            raise ValueError(f"Kategoria '{category_name}' nie istnieje.")
        updates.append("category_id = ?")
        parameters.append(category[0])

    if not updates:
        raise ValueError("Nie podano żadnych danych do aktualizacji.")

    parameters.append(task_id)
    sql_query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"

    cursor.execute(sql_query, parameters)
    conn.commit()
    conn.close()


# Usuwanie zadania
def delete_task(task_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
