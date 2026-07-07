import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = os.path.join("database", "nexus.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables_and_seed_data():
    """بتعمل الجداول وتحطلها بيانات وهمية، مرة واحدة بس"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            salary INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            product_name TEXT,
            price INTEGER,
            total_sales INTEGER
        )
    """)

    # نتأكد إن الجداول فاضية قبل ما نحط بيانات، عشان منكررش البيانات كل مرة
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        employees = [
            (1, "Ahmed Salah", "Engineering", 15000),
            (2, "Mona Hassan", "Marketing", 12000),
            (3, "Youssef Adel", "Engineering", 17000),
            (4, "Nour Ibrahim", "HR", 11000),
            (5, "Karim Fathy", "Sales", 13000),
        ]
        cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", employees)
        logger.info("Employees table seeded.")

    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        products = [
            (1, "Laptop Stand", 450, 320),
            (2, "Wireless Mouse", 250, 800),
            (3, "Mechanical Keyboard", 900, 150),
            (4, "USB-C Hub", 350, 600),
            (5, "Monitor Arm", 700, 90),
        ]
        cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)
        logger.info("Products table seeded.")

    conn.commit()
    conn.close()
    logger.info("Database ready.")


def run_query(sql_query: str):
    """بتشغل جملة SQL وترجع النتيجة"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        logger.info(f"Query executed: {sql_query}")
        return {"columns": columns, "rows": results}
    except Exception as e:
        logger.error(f"SQL Error: {e}")
        return {"error": str(e)}
    finally:
        conn.close()