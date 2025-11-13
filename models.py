import sqlite3
from datetime import datetime

DB_PATH = "db.sqlite"

def get_conn(path=None):
    return sqlite3.connect(path or DB_PATH)

def init_db(path=None):
    p = path or DB_PATH
    conn = get_conn(p)
    cur = conn.cursor()
    # feedback, products, clients, orders, order_items
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT,
        created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL DEFAULT 0,
        stock INTEGER NOT NULL DEFAULT 0,
        created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        status TEXT DEFAULT 'pending',
        total REAL DEFAULT 0,
        created_at TEXT,
        FOREIGN KEY(client_id) REFERENCES clients(id)
    );
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    );
    """)
    conn.commit()
    conn.close()

# Feedback CRUD
def create_feedback(name, email, message):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO feedback (name,email,message,created_at) VALUES (?,?,?,?)",
                (name, email, message, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_feedbacks():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,email,message,created_at FROM feedback ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_feedback(fid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,email,message,created_at FROM feedback WHERE id=?", (fid,))
    row = cur.fetchone()
    conn.close()
    return row

def delete_feedback(fid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM feedback WHERE id=?", (fid,))
    conn.commit()
    conn.close()

# Products
def create_product(name, description, price, stock):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name,description,price,stock,created_at) VALUES (?,?,?,?,?)",
                (name, description, float(price), int(stock), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_products():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,description,price,stock,created_at FROM products ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_product(pid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,description,price,stock FROM products WHERE id=?", (pid,))
    row = cur.fetchone()
    conn.close()
    return row

def delete_product(pid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()

def update_product_stock(pid, new_stock):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE products SET stock=? WHERE id=?", (new_stock, pid))
    conn.commit()
    conn.close()

# Clients
def create_client(name, email, phone):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO clients (name,email,phone,created_at) VALUES (?,?,?,?)",
                (name, email, phone, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_clients():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,email,phone,created_at FROM clients ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

# Orders
def create_order(client_id, items):
    """
    items: list of dicts [{'product_id':id,'quantity':q}]
    """
    conn = get_conn()
    cur = conn.cursor()
    created = datetime.utcnow().isoformat()
    total = 0.0
    # compute prices and update stock
    for it in items:
        cur.execute("SELECT price,stock FROM products WHERE id=?", (it['product_id'],))
        p = cur.fetchone()
        if not p:
            conn.close()
            raise ValueError("Product not found")
        price, stock = p
        if stock < it['quantity']:
            conn.close()
            raise ValueError("Not enough stock for product %s" % it['product_id'])
        total += price * it['quantity']

    cur.execute("INSERT INTO orders (client_id,status,total,created_at) VALUES (?,?,?,?)",
                (client_id, 'pending', total, created))
    order_id = cur.lastrowid
    for it in items:
        cur.execute("SELECT price,stock FROM products WHERE id=?", (it['product_id'],))
        price, stock = cur.fetchone()
        cur.execute("INSERT INTO order_items (order_id,product_id,quantity,price) VALUES (?,?,?,?)",
                    (order_id, it['product_id'], it['quantity'], price))
        cur.execute("UPDATE products SET stock=? WHERE id=?", (stock - it['quantity'], it['product_id']))

    conn.commit()
    conn.close()
    return order_id

def get_orders():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,client_id,status,total,created_at FROM orders ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_order_items(order_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT oi.id,oi.product_id,p.name,oi.quantity,oi.price FROM order_items oi JOIN products p ON oi.product_id=p.id WHERE oi.order_id=?",
                (order_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def update_order_status(order_id, status):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    conn.commit()
    conn.close()