from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime
from calendar import monthrange

from db import init_db
from expense_manager import (
    add_expense,
    get_all_expenses,
    delete_expense,
    update_expense,
    get_expense_by_id,
    get_category_summary_by_month,
    get_daily_summary_by_month
)

app = Flask(__name__)

# -------------------- Dashboard --------------------

@app.route("/")
def dashboard():
    # Get selected month from URL or default to current month
    selected_month = request.args.get("month")
    if not selected_month:
        selected_month = datetime.now().strftime("%Y-%m")

    # ---------------- Category Summary ----------------
    summary = get_category_summary_by_month(selected_month)
    labels = [row[0] for row in summary]
    values = [row[1] for row in summary]
    total = sum(values) if values else 0

    # ---------------- Daily Summary ----------------
    daily = get_daily_summary_by_month(selected_month)

    # Convert DB result to dict: { "2026-01-05": 500, ... }
    daily_map = { row[0]: row[1] for row in daily }

    # Get number of days in selected month
    year, month = map(int, selected_month.split("-"))
    num_days = monthrange(year, month)[1]  # 28, 30, or 31

    # Build full X axis: 1..num_days
    day_labels = list(range(1, num_days + 1))
    day_values = []

    for day in day_labels:
        date_str = f"{year:04d}-{month:02d}-{day:02d}"
        day_values.append(daily_map.get(date_str, 0))  # 0 if no expense that day

    return render_template(
        "dashboard.html",
        labels=json.dumps(labels),
        values=json.dumps(values),
        total=total,
        day_labels=json.dumps(day_labels),
        day_values=json.dumps(day_values),
        selected_month=selected_month
    )

# -------------------- Add Expense --------------------

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        date = request.form["date"]
        description = request.form["description"]

        add_expense(amount, category, date, description)
        return redirect(url_for("dashboard"))

    return render_template("add_expense.html")

# -------------------- View Expenses --------------------

@app.route("/expenses")
def expenses():
    all_expenses = get_all_expenses()
    return render_template("expenses.html", expenses=all_expenses)

# -------------------- Delete Expense --------------------

@app.route("/delete/<int:expense_id>")
def delete(expense_id):
    delete_expense(expense_id)
    return redirect(url_for("expenses"))

# -------------------- Edit Expense --------------------

@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit(expense_id):
    expense = get_expense_by_id(expense_id)

    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        date = request.form["date"]
        description = request.form["description"]

        update_expense(expense_id, amount, category, date, description)
        return redirect(url_for("expenses"))

    return render_template("edit_expense.html", expense=expense)

# -------------------- Main --------------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
