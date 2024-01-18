from flask import g
import sqlite3
from BookStore import app

# Database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('bookstore.db')
    return db

# Create the database tables
with app.app_context():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Publisher (
                        publisher_id TEXT PRIMARY KEY,
                        publisher_name TEXT,
                        publication_address TEXT,
                        publication_phone TEXT,
                        publication_web TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                            user_id TEXT PRIMARY KEY,
                            username TEXT,
                            email TEXT,
                            password TEXT,
                            confirm_password TEXT
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        author TEXT,
                        price REAL,
                        publication_year INTEGER,
                        publisher_id INTEGER,
                        FOREIGN KEY (publisher_id) REFERENCES Publisher (publisher_id) 
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Customers (
                        customer_id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT,
                        phone TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
                        order_id INTEGER PRIMARY KEY,
                        customer_id INTEGER,
                        book_id INTEGER,
                        quantity INTEGER,
                        order_date TEXT,
                        Total_price INTEGER,
                        FOREIGN KEY (customer_id) REFERENCES Customers (customer_id),
                        FOREIGN KEY (book_id) REFERENCES Books (book_id)
                    )''')
    conn.commit()
    cursor.close()
    conn.close()
