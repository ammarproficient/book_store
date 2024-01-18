from flask import render_template, request, redirect, url_for, flash, Flask
from BookStore import app
from BookStore.models import get_db
import uuid


# Home page
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Home')

# About page
@app.route('/about')
def about():
    return render_template('about.html', title='About')

# Signup page
@app.route('/signup')
def signup():
    return render_template('signup.html', title='Sign Up')


# Login page
@app.route('/login')
def login():
    return render_template('login.html', title='Login')

# Publisher page
@app.route('/publishers')
def display_publishers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Publisher')
    publishers = cursor.fetchall()
    return render_template('publishers.html', publishers=publishers, title='Publishers')

# Books page
@app.route('/books')
def display_books():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    return render_template('books.html', books=books, title='Books')

# Customer page
@app.route('/customers')
def display_customers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    return render_template('customers.html', customers=customers, title='Customers')

# Order page
@app.route('/orders')
def display_orders():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT Orders.order_id, Customers.customer_id, Customers.name, Books.title, Orders.quantity, Orders.order_date, Orders.Total_Price
                    FROM Orders
                    JOIN Customers ON Orders.customer_id = Customers.customer_id
                    JOIN Books ON Orders.book_id = Books.book_id''')
    orders = cursor.fetchall()
    return render_template('orders.html', orders=orders, title='Orders')


# Customer order page
@app.route('/customers/orders/<int:customer_id>')
def display_customer_orders(customer_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT Orders.order_id, Customers.customer_id, Customers.name, Books.title, Orders.quantity, Orders.order_date, Orders.Total_price
                    FROM Orders
                    JOIN Customers ON Orders.customer_id = Customers.customer_id
                    JOIN Books ON Orders.book_id = Books.book_id
                    WHERE Customers.customer_id = ?''', (customer_id,))
    customer_orders = cursor.fetchall()
    return render_template('customer_orders.html', customer_orders=customer_orders, title='Customer Order(s)')


# Search Customer
@app.route('/customers/search', methods=['GET'])
def search_customers():
    conn = get_db()
    cursor = conn.cursor()
    search_query = request.args.get('query', '').strip()

    if search_query:
        # Perform the search query
        cursor.execute('SELECT * FROM Customers WHERE customer_id LIKE ? OR name LIKE ?',
                       ('%' + search_query + '%', '%' + search_query + '%'))
        customers = cursor.fetchall()
    else:
        # If no search query provided, return all customers
        cursor.execute('SELECT * FROM Customers')
        customers = cursor.fetchall()

    return render_template('customers.html', customers=customers, title='Search Customer')

# Search orders
@app.route('/orders/search', methods=['GET'])
def search_orders():
    conn = get_db()
    cursor = conn.cursor()

    # Get the search query parameters
    order_id_query = request.args.get('order_id', '').strip()

    # Construct the SQL query based on the provided parameters
    if order_id_query:
        query = 'SELECT * FROM Orders WHERE order_id LIKE ?'
        cursor.execute(query, ('%' + order_id_query + '%',))
        orders = cursor.fetchall()
    else:
        # If no search query provided, return all orders
        cursor.execute('SELECT * FROM Orders')
        orders = cursor.fetchall()

    return render_template('orders.html', orders=orders, title='Search Orders')




# Search publishers
@app.route('/publishers/search', methods=['GET'])
def search_publishers():
    conn = get_db()
    cursor = conn.cursor()

    # Get the search query parameters
    publisher_name_query = request.args.get('publisher_name', '').strip()

    # Construct the SQL query based on the provided parameters
    if publisher_name_query:
        query = 'SELECT * FROM Publisher WHERE publisher_id LIKE ?'
        cursor.execute(query, ('%' + publisher_name_query + '%',))
        publishers = cursor.fetchall()
    else:
        # If no search query provided, return all publishers
        cursor.execute('SELECT * FROM Publisher')
        publishers = cursor.fetchall()

    return render_template('publishers.html', publishers=publishers, title='Publishers')


# Search books
@app.route('/books/search', methods=['GET'])
def search_books():
    search_query = request.args.get('query', '').strip()

    if not search_query:
        # If the search query is empty, display all books
        return redirect('/books')

    conn = get_db()
    cursor = conn.cursor()

    # Perform the search query using SQL LIKE clause to filter the results
    cursor.execute('SELECT * FROM Books WHERE book_id LIKE ? OR title LIKE ? OR author LIKE ?', ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
    books = cursor.fetchall()

    return render_template('books.html', books=books, title='Search Books')


# Add a new publisher
@app.route('/publishers/add', methods=['GET', 'POST'])
def add_publisher():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        publisher_name = request.form['publisher_name']
        publication_address = request.form['publication_address']
        publication_phone = request.form['publication_phone']
        publication_web = request.form['publication_email']

        # Generate a 6-digit unique publisher ID
        publisher_id = str(uuid.uuid4().int)[:7]

        cursor.execute('INSERT INTO Publisher (publisher_id, publisher_name, publication_address, publication_phone, publication_web) VALUES (?, ?, ?, ?, ?)',
                       (publisher_id, publisher_name, publication_address, publication_phone, publication_web))
        conn.commit()
        return redirect('/publishers')

    return render_template('add_publisher.html', title='Add Publisher')

# Add a new book
@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        publication_year = request.form['publication_year']
        publisher_id = request.form['publisher_id']  # Get the selected publisher_id from the form

        # Generate a 6-digit unique book ID
        book_id = str(uuid.uuid4().int)[:6]

        cursor.execute('INSERT INTO Books (book_id, title, author, price, publication_year, publisher_id) VALUES (?, ?, ?, ?, ?, ?)',
                       (book_id, title, author, price, publication_year, publisher_id))
        conn.commit()
        return redirect('/books')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT publisher_id, publisher_name FROM Publisher')
    publishers = cursor.fetchall()  # Fetch all the publishers to display in the dropdown select field

    return render_template('add_book.html', publishers=publishers, title='Add Book')


# Add a new customer
@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Generate a 10-digit customer ID
        customer_id = str(uuid.uuid4().int)[:10]

        cursor.execute('INSERT INTO Customers (customer_id, name, email, phone) VALUES (?, ?, ?, ?)',
                       (customer_id, name, email, phone))
        conn.commit()
        return redirect('/customers')

    return render_template('add_customer.html', title='Add Customer')


# Add a new order
@app.route('/orders/add', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()

        customer_id = request.form['customer_id']
        book_id = request.form['book_id']
        quantity = request.form['quantity']
        order_date = request.form['order_date']

        # Generate the Order ID
        order_id = str(uuid.uuid4().int)[:8]

        # Retrieve the book price
        cursor.execute('SELECT price FROM Books WHERE book_id = ?', (book_id,))
        book_price = cursor.fetchone()[0]

        # Calculate the order price
        order_price = float(quantity) * float(book_price)

        # Insert the order into the database with the customer_id included
        cursor.execute('INSERT INTO Orders (order_id, customer_id, book_id, quantity, order_date, Total_price) VALUES (?, ?, ?, ?, ?, ?)',
                       (order_id, customer_id, book_id, quantity, order_date, order_price))

        conn.commit()
        return redirect('/orders')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()

    return render_template('add_order.html', customers=customers, books=books, title='Add Order')

# Update a publisher
@app.route('/publishers/update/<string:publisher_id>', methods=['GET', 'POST'])
def update_publisher(publisher_id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        publisher_name = request.form['publisher_name']
        publication_address = request.form['publication_address']
        publication_phone = request.form['publication_phone']
        publication_web = request.form['publication_web']

        cursor.execute('UPDATE Publisher SET publisher_name=?, publication_address=?, publication_phone=?, publication_web=? WHERE publisher_id=?',
                       (publisher_name, publication_address, publication_phone, publication_web, publisher_id))
        conn.commit()
        return redirect('/publishers')

    cursor.execute('SELECT * FROM Publisher WHERE publisher_id=?', (publisher_id,))
    publisher = cursor.fetchone()
    return render_template('update_publisher.html', publisher=publisher, publisher_id=publisher_id, title='Update Publisher')


# Update a book
@app.route('/books/update/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        publication_year = request.form['publication_year']
        publisher_id = request.form['publisher_id']  # Get the selected publisher_id from the form

        cursor.execute('UPDATE Books SET title=?, author=?, price=?, publication_year=?, publisher_id=? WHERE book_id=?',
                       (title, author, price, publication_year, publisher_id, book_id))
        conn.commit()
        return redirect('/books')

    cursor.execute('SELECT * FROM Books WHERE book_id=?', (book_id,))
    book = cursor.fetchone()

    cursor.execute('SELECT publisher_id, publisher_name FROM Publisher')
    publishers = cursor.fetchall()  # Fetch all the publishers to display in the dropdown select field

    return render_template('update_book.html', book=book, publishers=publishers, title='Update Book')


# Update a customer
@app.route('/customers/update/<int:customer_id>', methods=['GET', 'POST'])
def update_customer(customer_id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute('UPDATE Customers SET name=?, email=?, phone=? WHERE customer_id=?',
                       (name, email, phone, customer_id))
        conn.commit()
        return redirect('/customers')

    cursor.execute('SELECT * FROM Customers WHERE customer_id=?', (customer_id,))
    customer = cursor.fetchone()
    return render_template('update_customer.html', customer=customer, customer_id=customer_id, title='Update Customer')


# Update an order
@app.route('/orders/update/<int:order_id>', methods=['GET', 'POST'])
def update_order(order_id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        book_id = request.form['book_id']
        quantity = request.form['quantity']
        order_date = request.form['order_date']

        # Retrieve the book price
        cursor.execute('SELECT price FROM Books WHERE book_id = ?', (book_id,))
        book_price = cursor.fetchone()[0]

        # Calculate the order price
        order_price = float(quantity) * float(book_price)

        cursor.execute('UPDATE Orders SET customer_id=?, book_id=?, quantity=?, order_date=?, Total_price=? WHERE order_id=?',
                       (customer_id, book_id, quantity, order_date, order_price, order_id))
        conn.commit()
        return redirect('/orders')

    cursor.execute('''SELECT Orders.order_id, Customers.name, Books.title, Orders.quantity, Orders.order_date, Orders.Total_price
                    FROM Orders
                    JOIN Customers ON Orders.customer_id = Customers.customer_id
                    JOIN Books ON Orders.book_id = Books.book_id
                    WHERE order_id=?''', (order_id,))
    order = cursor.fetchone()
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()

    return render_template('update_order.html', order=order, customers=customers, books=books, title='Update Order')



# Delete a publisher
@app.route('/publishers/delete/<string:publisher_id>', methods=['POST'])
def delete_publisher(publisher_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Publisher WHERE publisher_id=?', (publisher_id,))
    conn.commit()
    return redirect('/publishers')

# Delete a book
@app.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Books WHERE book_id=?', (book_id,))
    conn.commit()
    return redirect('/books')

# Delete an order
@app.route('/orders/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Orders WHERE order_id=?', (order_id,))
    conn.commit()
    return redirect('/orders')

# Delete a customer
@app.route('/customers/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Customers WHERE customer_id=?', (customer_id,))
    conn.commit()
    return redirect('/customers')

# Display publisher details
@app.route('/publishers/<string:publisher_id>')
def display_publisher_details(publisher_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Publisher WHERE publisher_id=?', (publisher_id,))
    publisher = cursor.fetchone()

    if publisher:
        return render_template('publisher_details.html', publisher=publisher, title='Publisher Details')
    else:
        return "Publisher not found.", 404