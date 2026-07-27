import sqlite3


# ---------------- TOTAL FARMERS ----------------
def get_total_farmers(cursor):
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='Farmer'")
    return cursor.fetchone()[0]


# ---------------- TOTAL CUSTOMERS ----------------
def get_total_customers(cursor):
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='Customer'")
    return cursor.fetchone()[0]


# ---------------- TOTAL VEGETABLES ----------------
def get_total_vegetables(cursor):
    cursor.execute("SELECT COUNT(*) FROM vegetables")
    return cursor.fetchone()[0]


# ---------------- AVAILABLE VEGETABLES ----------------
def get_available_vegetables(cursor):
    cursor.execute("""
        SELECT *
        FROM vegetables
        WHERE quantity > 0
        ORDER BY vegetable_name
    """)
    return cursor.fetchall()


# ---------------- TOTAL ORDERS ----------------
def get_total_orders(cursor):
    cursor.execute("SELECT COUNT(*) FROM orders")
    return cursor.fetchone()[0]


# ---------------- TRENDING VEGETABLES ----------------
def get_trending_vegetables(cursor):
    cursor.execute("""
        SELECT vegetable,
               SUM(quantity) AS sold
        FROM orders
        GROUP BY vegetable
        ORDER BY sold DESC
        LIMIT 5
    """)
    return cursor.fetchall()


# ---------------- FARMER VEGETABLES ----------------
def get_farmer_vegetables(cursor, username):
    cursor.execute("""
        SELECT *
        FROM vegetables
        WHERE farmer_name=?
        ORDER BY id DESC
    """, (username,))
    return cursor.fetchall()


# ---------------- FARMER SALES ----------------
def get_farmer_sales(cursor, username):
    cursor.execute("""
        SELECT
            o.vegetable,
            o.quantity,
            o.order_date
        FROM orders o
        JOIN vegetables v
        ON o.vegetable=v.vegetable_name
        WHERE v.farmer_name=?
        ORDER BY o.order_date DESC
    """, (username,))
    return cursor.fetchall()


# ---------------- FARMER TOTAL INCOME ----------------
def get_farmer_income(cursor, username):
    cursor.execute("""
        SELECT
            SUM(o.quantity * v.price)
        FROM orders o
        JOIN vegetables v
        ON o.vegetable=v.vegetable_name
        WHERE v.farmer_name=?
    """, (username,))

    income = cursor.fetchone()[0]

    if income is None:
        return 0

    return income


# ---------------- BEST SELLING VEGETABLE ----------------
def get_best_selling(cursor):
    cursor.execute("""
        SELECT vegetable,
               SUM(quantity) AS sold
        FROM orders
        GROUP BY vegetable
        ORDER BY sold DESC
        LIMIT 1
    """)

    return cursor.fetchone()


# ---------------- CUSTOMER ORDERS ----------------
def get_customer_orders(cursor, username):
    cursor.execute("""
        SELECT
            vegetable,
            quantity,
            order_date
        FROM orders
        WHERE customer=?
        ORDER BY id DESC
    """, (username,))

    return cursor.fetchall()


# ---------------- UPDATE STOCK ----------------
def update_stock(conn, cursor, vegetable_id, quantity):

    cursor.execute("""
        UPDATE vegetables
        SET quantity = quantity - ?
        WHERE id = ?
    """, (quantity, vegetable_id))

    conn.commit()


# ---------------- DELETE VEGETABLE ----------------
def delete_vegetable(conn, cursor, vegetable_id):

    cursor.execute("""
        DELETE FROM vegetables
        WHERE id = ?
    """, (vegetable_id,))

    conn.commit()


# ---------------- GET VEGETABLE BY ID ----------------
def get_vegetable(cursor, vegetable_id):

    cursor.execute("""
        SELECT *
        FROM vegetables
        WHERE id=?
    """, (vegetable_id,))

    return cursor.fetchone()


# ---------------- LOW STOCK ITEMS ----------------
def get_low_stock(cursor):

    cursor.execute("""
        SELECT vegetable_name,
               quantity
        FROM vegetables
        WHERE quantity <= 5
        ORDER BY quantity
    """)

    return cursor.fetchall()


# ---------------- DASHBOARD STATS ----------------
def get_dashboard_stats(cursor):

    return {
        "farmers": get_total_farmers(cursor),
        "customers": get_total_customers(cursor),
        "vegetables": get_total_vegetables(cursor),
        "orders": get_total_orders(cursor)
    }