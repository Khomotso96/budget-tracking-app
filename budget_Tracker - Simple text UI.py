# Importing necessary module
import sqlite3



def connect_to_database(database_name):
    """
    Connect to SQLite database.

    Parameters:
    - database_name (str): The name of the SQLite database.

    Returns:
    - connection (sqlite3.Connection): Connection object if successful, None otherwise.

    Raises:
    - sqlite3.Error: If there is an error connecting to the database.
    """
    try:
        connection = sqlite3.connect(database_name)
        return connection
    except sqlite3.Error as e:
        print("Error connecting to database:", e)
        return None



def create_tables(connection):
    """
    Create necessary tables if they don't exist in the database.

    Parameters:
    - connection (sqlite3.Connection): Connection object to the SQLite database.

    Returns:
    - None

    Raises:
    - sqlite3.Error: If there is an error creating tables in the database.
    """
    try:
        cursor = connection.cursor()
        # Create table for expenses
        cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY,
                        category TEXT,
                        item_name TEXT,
                        amount REAL)''')
        # Create table for income
        cursor.execute('''CREATE TABLE IF NOT EXISTS income (
                        id INTEGER PRIMARY KEY,
                        category TEXT,
                        item_name TEXT,
                        amount REAL)''')
        # Create table for budgets with a unique constraint
        cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                        category TEXT PRIMARY KEY,
                        budget REAL)''')  # Adding PRIMARY KEY constraint
        # Create table for financial goals
        cursor.execute('''CREATE TABLE IF NOT EXISTS financial_goals (
                        id INTEGER PRIMARY KEY,
                        goal_name TEXT,
                        target_amount REAL,
                        current_amount REAL)''')
        connection.commit()
    except sqlite3.Error as e:
        print("Error creating tables:", e)



def add_expense_category(connection, category, item_name, amount):
    """
    Add new expense category to the database.

    Parameters:
    - connection (sqlite3.Connection): Connection object to the SQLite database.
    - category (str): Expense category to add.
    - item_name (str): Name of the expense item.
    - amount (float): Expense amount.

    Returns:
    - None

    Raises:
    - sqlite3.Error: If there is an error adding the expense category to the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO expenses (category, item_name, amount) VALUES (?, ?, ?)", (category, item_name, amount))
        connection.commit()
        print("Expense item '{}' added successfully to category '{}'.".format(item_name, category))
    except sqlite3.Error as e:
        print("Error adding expense item:", e)



def view_expenses(connection):
    """
    View all expenses.

    Parameters:
    - connection (sqlite3.Connection): Connection object to the SQLite database.

    Returns:
    - None

    Raises:
    - sqlite3.Error: If there is an error viewing expenses in the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM expenses")
        expense_data = cursor.fetchall()
        if expense_data:
            for row in expense_data:
                print("Category: {}, Item Name: {}, Amount: {}".format(row[1], row[2], row[3]))
        else:
            print("No expense entries found.")
    except sqlite3.Error as e:
        print("Error viewing expenses:", e)



def view_expenses_by_category(connection):
    """
    View expenses by category.

    Parameters:
    - connection (sqlite3.Connection): Connection object to the SQLite database.

    Returns:
    - None

    Raises:
    - sqlite3.Error: If there is an error viewing expenses by category in the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT category FROM expenses")
        categories = cursor.fetchall()
        for category in categories:
            print("Category:", category[0])
            cursor.execute("SELECT * FROM expenses WHERE category=?", (category[0],))
            expense_data = cursor.fetchall()
            for row in expense_data:
                print("    Item Name: {}, Amount: {}".format(row[2], row[3]))
            print()  # Empty line
    except sqlite3.Error as e:
        print("Error viewing expenses by category:", e)



def add_income_category(connection, category, item_name, amount):
    """
    Add new income category to the database.

    Parameters:
    - connection (sqlite3.Connection): Connection object to the SQLite database.
    - category (str): Income category to add.
    - item_name (str): Name of the income item.
    - amount (float): Income amount.

    Returns:
    - None

    Raises:
    - sqlite3.Error: If there is an error adding the income category to the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO income (category, item_name, amount) VALUES (?, ?, ?)", (category, item_name, amount))
        connection.commit()
        print("Income item '{}' added successfully to category '{}'.".format(item_name, category))
    except sqlite3.Error as e:
        print("Error adding income item:", e)



def view_income(connection):
    """
    View all income entries.

    Parameters:
    - connection (sqlite3.Connection): Connection object to the SQLite database.

    Returns:
    - None

    Raises:
    - sqlite3.Error: If there is an error viewing income in the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM income")
        income_data = cursor.fetchall()
        if income_data:
            for row in income_data:
                print("Category: {}, Item Name: {}, Amount: {}".format(row[1], row[2], row[3]))
        else:
            print("No income entries found.")
    except sqlite3.Error as e:
        print("Error viewing income:", e)



def view_income_by_category(connection):
    """
    View income by category.

    Parameters:
    - connection (sqlite3.Connection): Connection object to the SQLite database.

    Returns:
    - None

    Raises:
    - sqlite3.Error: If there is an error viewing income by category in the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT category FROM income")
        categories = cursor.fetchall()
        for category in categories:
            print("Category:", category[0])
            cursor.execute("SELECT * FROM income WHERE category=?", (category[0],))
            income_data = cursor.fetchall()
            for row in income_data:
                print("    Item Name: {}, Amount: {}".format(row[2], row[3]))
            print()  # Empty line
    except sqlite3.Error as e:
        print("Error viewing income by category:", e)



def set_budget(connection, category, budget):
    """
    Set budget for a category.

    Parameters:
    - connection (sqlite3.Connection): Connection object to the SQLite database.
    - category (str): Category for which budget is set.
    - budget (float): Budget amount to set.

    Returns:
    - None

    Raises:
    - sqlite3.Error: If there is an error setting the budget in the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT OR REPLACE INTO budgets (category, budget) VALUES (?, ?)", (category, budget))
        connection.commit()
        print("Budget for category '{}' set successfully.".format(category))
    except sqlite3.Error as e:
        print("Error setting budget:", e)



def view_budget(connection):
    """
    View budget for each category and compare with actual expenses.

    Parameters:
    - connection (sqlite3.Connection): Connection object to the SQLite database.

    Returns:
    - None

    Raises:
    - sqlite3.Error: If there is an error viewing the budget in the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT category, budget FROM budgets")
        budget_data = cursor.fetchall()
        if budget_data:
            for category, budget in budget_data:
                cursor.execute("SELECT SUM(amount) FROM expenses WHERE category = ?", (category,))
                total_expense = cursor.fetchone()[0] or 0
                difference = budget - total_expense
                print(f"Category: {category}, Budget: {budget:.2f}, Actual Expense: {total_expense:.2f}, Difference: {difference:.2f}")
        else:
            print("No budget categories found.")
    except sqlite3.Error as e:
        print("Error viewing budget:", e)



def set_financial_goals(connection):
    """
    Set financial goals.

    Parameters:
    - connection (sqlite3.Connection): Connection object to the SQLite database.

    Returns:
    - None

    Raises:
    - sqlite3.Error: If there is an error setting financial goals in the database.
    """
    try:
        cursor = connection.cursor()
        goal_name = input("Enter the name of the financial goal: ")
        target_amount = float(input("Enter the target amount: "))
        current_amount = float(input("Enter the current amount: "))
        cursor.execute("INSERT INTO financial_goals (goal_name, target_amount, current_amount) VALUES (?, ?, ?)", (goal_name, target_amount, current_amount))
        connection.commit()
        print("Financial goal '{}' set successfully.".format(goal_name))
    except sqlite3.Error as e:
        print("Error setting financial goal:", e)



def view_and_edit_goals(connection):
    """
    View and edit financial goals.

    Parameters:
    - connection (sqlite3.Connection): Connection object to the SQLite database.

    Returns:
    - None

    Raises:
    - sqlite3.Error: If there is an error viewing financial goals in the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM financial_goals")
        goals_data = cursor.fetchall()
        if goals_data:
            for goal in goals_data:
                print("Goal Name: {}, Target Amount: {}, Current Amount: {}".format(goal[1], goal[2], goal[3]))
            goal_id = int(input("Enter the ID of the goal you want to edit: "))
            new_target_amount = float(input("Enter the new target amount: "))
            cursor.execute("UPDATE financial_goals SET target_amount = ? WHERE id = ?", (new_target_amount, goal_id))
            connection.commit()
            print("Financial goal updated successfully.")
        else:
            print("No financial goals found.")
    except sqlite3.Error as e:
        print("Error viewing and editing financial goals:", e)



def view_progress(connection):
    """
    View progress towards financial goals.

    Parameters:
    - connection (sqlite3.Connection): Connection object to the SQLite database.

    Returns:
    - None

    Raises:
    - sqlite3.Error: If there is an error viewing progress towards financial goals in the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM financial_goals")
        goals_data = cursor.fetchall()
        if goals_data:
            for goal in goals_data:
                progress = (goal[3] / goal[2]) * 100
                print("Goal Name: {}, Target Amount: {}, Current Amount: {}, Progress: {:.2f}%".format(goal[1], goal[2], goal[3], progress))
        else:
            print("No financial goals found.")
    except sqlite3.Error as e:
        print("Error viewing progress towards financial goals:", e)



def display_categories(categories):
    """
    Display pre-added categories with numbers.

    Parameters:
    - categories (list): List of categories.

    Returns:
    - None
    """
    print("Existing categories:")
    for idx, category in enumerate(categories, start=1):
        print(f"{idx}. {category}")
    print(f"{len(categories) + 1}. Add a new Category")



def add_new_category():
    """
    Add a new category.

    Returns:
    - new_category (str): The newly added category.
    """
    new_category = input("Enter the new category: ")
    return new_category



def display_menu():
    """
    Display the menu.

    Returns:
    - None
    """
    print("Expense and Budget Tracker:")
    print()  # Empty line
    print("1. Add expense")
    print("2. View expenses")
    print("3. View expenses by category")
    print("4. Add income")
    print("5. View income")
    print("6. View income by category")
    print("7. Set budget for a category")
    print("8. View budget for a category")
    print("9. Set financial goals")
    print("10. View and edit financial goals")
    print("11. View progress towards financial goals")
    print("12. Quit")
    print()  # Empty line



def main():
    """
    Main function to run the expense and budget tracker app.
    """
    # Connect to database
    database_name = "expense_tracker.db"
    connection = connect_to_database(database_name)
    if connection is None:
        return

    # Create tables if they don't exist
    create_tables(connection)

    # Pre-added categories
    categories = [
        "Housing",
        "Transportation",
        "Food and Dining",
        "Utilities",
        "Personal Care",
        "Health and Fitness",
        "Entertainment",
        "Education",
        "Debt Payments",
        "Savings and Investments"
    ]

    # Main menu
    while True:
        display_menu()
        choice = input("Enter your choice: ")


        if choice == "1":
            # Add expense
            display_categories(categories)
            category_choice = int(input("Enter expense category number or add a new one: "))
            if category_choice == len(categories) + 1:
                category = add_new_category()
                categories.append(category)
            else:
                category = categories[category_choice - 1]
            item_name = input("Enter expense item name: ")
            amount = float(input("Enter expense amount: "))
            add_expense_category(connection, category, item_name, amount)
            print()  # Empty line


        elif choice == "2":
            # View expenses
            view_expenses(connection)
            print()  # Empty line


        elif choice == "3":
            # View expenses by category
            view_expenses_by_category(connection)
            print()  # Empty line


        elif choice == "4":
            # Add income
            item_name = input("Enter income item name: ")
            amount = float(input("Enter income amount: "))
            add_income_category(connection, "", item_name, amount)
            print()  # Empty line


        elif choice == "5":
            # View income
            view_income(connection)
            print()  # Empty line


        elif choice == "6":
            # View income by category
            view_income_by_category(connection)
            print()  # Empty line


        elif choice == "7":
            # Set budget for a category
            display_categories(categories)
            category_choice = int(input("Enter category number to set budget: "))
            if category_choice == len(categories) + 1:
                category = add_new_category()
                categories.append(category)
            else:
                category = categories[category_choice - 1]
            budget = float(input("Enter Budget Amount: "))
            set_budget(connection, category, budget)
            
            # Calculate total expenses for the chosen category
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT SUM(amount) FROM expenses WHERE category = ?", (category,))
                total_expense = cursor.fetchone()[0] or 0
                difference = budget - total_expense
                if difference > 0:
                    print(f"Category '{category}' is under budget by ${difference:.2f}.")
                elif difference < 0:
                    print(f"Category '{category}' is over budget by ${abs(difference):.2f}.")
                else:
                    print(f"Category '{category}' is exactly on budget.")
            except sqlite3.Error as e:
                print("Error calculating budget difference:", e)
            print()  # Empty line


        elif choice == "8":
            # View budget for each category
            view_budget(connection)
            print()  # Empty line


        elif choice == "9":
            # Set financial goals
            set_financial_goals(connection)
            print()  # Empty line


        elif choice == "10":
            # View and edit financial goals
            view_and_edit_goals(connection)
            print()  # Empty line


        elif choice == "11":
            # View progress towards financial goals
            view_progress(connection)
            print()  # Empty line


        elif choice == "12":
            # Exit the program
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 12.")
            print()  # Empty line


    # Close the database connection when done
    connection.close()


if __name__ == "__main__":
    main()
