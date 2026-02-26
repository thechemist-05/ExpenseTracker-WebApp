from datetime import datetime
from db import get_connection

def add_expense(amount, category, date, description):
    if not date or date.strip() == "":
        date = datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
        (amount, category, date, description)
    )

    conn.commit()
    conn.close()

def get_all_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows

def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def update_expense(expense_id, amount, category, date, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE expenses
    SET amount = ?, category = ?, date = ?, description = ?
    WHERE id = ?
    """, (amount, category, date, description, expense_id))

    conn.commit()
    conn.close()

def get_expense_by_id(expense_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    row = cursor.fetchone()

    conn.close()
    return row

# 🥧 For category doughnut chart
def get_category_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    ORDER BY SUM(amount) DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

# 📈 For daily spending line chart
def get_daily_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT date, SUM(amount)
    FROM expenses
    GROUP BY date
    ORDER BY date
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows
def get_category_summary_by_month(month):  # month format: YYYY-MM
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    WHERE substr(date, 1, 7) = ?
    GROUP BY category
    ORDER BY SUM(amount) DESC
    """, (month,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_daily_summary_by_month(month):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT date, SUM(amount)
    FROM expenses
    WHERE substr(date, 1, 7) = ?
    GROUP BY date
    ORDER BY date
    """, (month,))

    rows = cursor.fetchall()
    conn.close()
    return rows
