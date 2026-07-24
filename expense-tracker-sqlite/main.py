import sqlite3


def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        description TEXT,
        amount INTEGER
    )
    """)


def add_expense(cursor):
    description = input("What item? ")
    amount = int(input("How much? "))

    expense_data = (description, amount)

    cursor.execute(
        """
    INSERT INTO expenses (description, amount)
    VALUES (?, ?)""",
        expense_data,
    )


def display_expenses(cursor):
    print("All Expenses:")
    print("-" * 20)

    cursor.execute("""
    SELECT *
    FROM expenses
    """)

    expenses = cursor.fetchall()

    for expense in expenses:
        print(expense)


def main():
    print("Expense Tracker")
    print("-" * 20)

    connection = sqlite3.connect("expense_tracker.db")
    cursor = connection.cursor()

    create_table(cursor)
    add_expense(cursor)
    connection.commit()
    display_expenses(cursor)
    connection.close()


if __name__ == "__main__":
    main()
