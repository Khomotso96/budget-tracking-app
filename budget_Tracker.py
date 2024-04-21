import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class BudgetTrackerApp:
    def __init__(self, master):
        """
        Initialize the BudgetTrackerApp.

        Parameters:
        - master (tk.Tk): The master tkinter window.
        """
        self.master = master
        self.master.title("Expense and Budget Tracker")

        # Connect to database
        self.database_name = "expense_tracker.db"
        self.connection = self.connect_to_database(self.database_name)
        if self.connection is None:
            messagebox.showerror("Error", "Failed to connect to the database. Exiting...")
            self.master.destroy()
            return

        # Create tables if they don't exist
        self.create_tables(self.connection)

        # Pre-added categories
        self.categories = [
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

        # Create buttons for each menu option
        self.btn_add_expense = tk.Button(master, text="1. Add expense", command=self.add_expense)
        self.btn_add_expense.pack()

        self.btn_view_expenses = tk.Button(master, text="2. View expenses", command=self.view_expenses)
        self.btn_view_expenses.pack()

        self.btn_view_expenses_by_category = tk.Button(master, text="3. View expenses by category", command=self.view_expenses_by_category)
        self.btn_view_expenses_by_category.pack()

        self.btn_add_income = tk.Button(master, text="4. Add income", command=self.add_income)
        self.btn_add_income.pack()

        self.btn_view_income = tk.Button(master, text="5. View income", command=self.view_income)
        self.btn_view_income.pack()

        self.btn_view_income_by_category = tk.Button(master, text="6. View income by category", command=self.view_income_by_category)
        self.btn_view_income_by_category.pack()

        self.btn_set_budget = tk.Button(master, text="7. Set budget for a category", command=self.set_budget)
        self.btn_set_budget.pack()

        self.btn_view_budget = tk.Button(master, text="8. View budget for a category", command=self.view_budget)
        self.btn_view_budget.pack()

        self.btn_set_financial_goals = tk.Button(master, text="9. Set financial goals", command=self.set_financial_goals)
        self.btn_set_financial_goals.pack()

        self.btn_view_edit_goals = tk.Button(master, text="10. View and edit financial goals", command=self.view_and_edit_goals)
        self.btn_view_edit_goals.pack()

        self.btn_view_progress = tk.Button(master, text="11. View progress towards financial goals", command=self.view_progress)
        self.btn_view_progress.pack()

        self.btn_quit = tk.Button(master, text="12. Quit", command=self.quit_app)
        self.btn_quit.pack()


    def connect_to_database(self, database_name):
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
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            return None


    def create_tables(self, connection):
        """
        Create tables in the database if they don't exist.

        Parameters:
        - connection (sqlite3.Connection): Connection object to the SQLite database.

        Returns:
        - None

        Raises:
        - sqlite3.Error: If there is an error creating tables in the database.
        """
        try:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                            id INTEGER PRIMARY KEY,
                            category TEXT,
                            item_name TEXT,
                            amount REAL)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS income (
                            id INTEGER PRIMARY KEY,
                            category TEXT,
                            item_name TEXT,
                            amount REAL)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                            category TEXT PRIMARY KEY,
                            budget REAL)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS financial_goals (
                            id INTEGER PRIMARY KEY,
                            goal_name TEXT,
                            target_amount REAL,
                            current_amount REAL)''')
            connection.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error creating tables: {e}")


    def add_expense(self):
        """
        Add an expense to the expenses table in the database.

        Parameters:
        - None

        Returns:
        - None

        Raises:
        - None
        """
        category = self.select_category()
        if category is None:
            return
        item_name = simpledialog.askstring("Expense", "Enter expense item name:")
        if item_name is None:
            return
        amount = simpledialog.askfloat("Expense", "Enter expense amount:")
        if amount is None:
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO expenses (category, item_name, amount) VALUES (?, ?, ?)", (category, item_name, amount))
            self.connection.commit()
            messagebox.showinfo("Expense Added", f"Expense item '{item_name}' added successfully to category '{category}'.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding expense item: {e}")


    def view_expenses(self):
        """
        View expenses from the expenses table in the database.

        Parameters:
        - None

        Returns:
        - None

        Raises:
        - sqlite3.Error: If there is an error viewing expenses in the database.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM expenses")
            expense_data = cursor.fetchall()
            if expense_data:
                expenses_str = "\n".join([f"Category: {row[1]}, Item Name: {row[2]}, Amount: {row[3]}" for row in expense_data])
                messagebox.showinfo("Expenses", expenses_str)
            else:
                messagebox.showinfo("Expenses", "No expense entries found.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error viewing expenses: {e}")


    def view_expenses_by_category(self):
        """
        View expenses grouped by category from the expenses table in the database.

        Parameters:
        - None

        Returns:
        - None

        Raises:
        - sqlite3.Error: If there is an error viewing expenses by category in the database.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT DISTINCT category FROM expenses")
            categories = cursor.fetchall()
            for category in categories:
                category_name = category[0]
                cursor.execute("SELECT * FROM expenses WHERE category=?", (category_name,))
                expense_data = cursor.fetchall()
                if expense_data:
                    expenses_str = "\n".join([f"    Item Name: {row[2]}, Amount: {row[3]}" for row in expense_data])
                    messagebox.showinfo(f"Expenses - {category_name}", expenses_str)
                else:
                    messagebox.showinfo(f"Expenses - {category_name}", "No expense entries found.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error viewing expenses by category: {e}")


    def add_income(self):
        """
        Add an income to the income table in the database.

        Parameters:
        - None

        Returns:
        - None

        Raises:
        - None
        """
        item_name = simpledialog.askstring("Income", "Enter income item name:")
        if item_name is None:
            return
        amount = simpledialog.askfloat("Income", "Enter income amount:")
        if amount is None:
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO income (category, item_name, amount) VALUES (?, ?, ?)", ("", item_name, amount))
            self.connection.commit()
            messagebox.showinfo("Income Added", f"Income item '{item_name}' added successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding income item: {e}")


    def view_income(self):
        """
        View income from the income table in the database.

        Parameters:
        - None

        Returns:
        - None

        Raises:
        - sqlite3.Error: If there is an error viewing income in the database.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM income")
            income_data = cursor.fetchall()
            if income_data:
                income_str = "\n".join([f"Category: {row[1]}, Item Name: {row[2]}, Amount: {row[3]}" for row in income_data])
                messagebox.showinfo("Income", income_str)
            else:
                messagebox.showinfo("Income", "No income entries found.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error viewing income: {e}")


    def view_income_by_category(self):
        """
        View income grouped by category from the income table in the database.

        Parameters:
        - None

        Returns:
        - None

        Raises:
        - sqlite3.Error: If there is an error viewing income by category in the database.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT DISTINCT category FROM income")
            categories = cursor.fetchall()
            for category in categories:
                category_name = category[0]
                cursor.execute("SELECT * FROM income WHERE category=?", (category_name,))
                income_data = cursor.fetchall()
                if income_data:
                    income_str = "\n".join([f"    Item Name: {row[2]}, Amount: {row[3]}" for row in income_data])
                    messagebox.showinfo(f"Income - {category_name}", income_str)
                else:
                    messagebox.showinfo(f"Income - {category_name}", "No income entries found.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error viewing income by category: {e}")


    def select_category(self):
        """
        Select a category from a list of pre-added categories or add a new category.

        Parameters:
        - None

        Returns:
        - category (str): The selected or newly added category.
        """
        category_choice = simpledialog.askinteger("Category", "Select category:\n" + "\n".join([f"{idx}. {category}" for idx, category in enumerate(self.categories, start=1)]) + "\n" + f"{len(self.categories) + 1}. Add a new Category")
        if category_choice is None:
            return None
        if category_choice == len(self.categories) + 1:
            category = simpledialog.askstring("Category", "Enter the new category:")
            if category is None:
                return None
            self.categories.append(category)
            return category
        else:
            return self.categories[category_choice - 1]


    def set_budget(self):
        """
        Set a budget for a category.

        Parameters:
        - None

        Returns:
        - None

        Raises:
        - sqlite3.Error: If there is an error setting budget in the database.
        """
        category = self.select_category()
        if category is None:
            return
        budget = simpledialog.askfloat("Budget", f"Enter budget amount for category '{category}':")
        if budget is None:
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT OR REPLACE INTO budgets (category, budget) VALUES (?, ?)", (category, budget))
            self.connection.commit()

            cursor.execute("SELECT SUM(amount) FROM expenses WHERE category = ?", (category,))
            total_expense = cursor.fetchone()[0] or 0
            difference = budget - total_expense
            if difference > 0:
                messagebox.showinfo("Budget", f"Category '{category}' is under budget by ${difference:.2f}.")
            elif difference < 0:
                messagebox.showinfo("Budget", f"Category '{category}' is over budget by ${abs(difference):.2f}.")
            else:
                messagebox.showinfo("Budget", f"Category '{category}' is exactly on budget.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error setting budget: {e}")


    def view_budget(self):
        """
        View budget for each category.

        Parameters:
        - None

        Returns:
        - None

        Raises:
        - sqlite3.Error: If there is an error viewing budget in the database.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT category, budget FROM budgets")
            budget_data = cursor.fetchall()
            if budget_data:
                budget_str = "\n".join([f"Category: {category}, Budget: {budget:.2f}" for category, budget in budget_data])
                messagebox.showinfo("Budget", budget_str)
            else:
                messagebox.showinfo("Budget", "No budget categories found.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error viewing budget: {e}")


    def set_financial_goals(self):
        """
        Set financial goals.

        Parameters:
        - None

        Returns:
        - None

        Raises:
        - sqlite3.Error: If there is an error setting financial goals in the database.
        """
        goal_name = simpledialog.askstring("Financial Goals", "Enter the name of the financial goal:")
        if goal_name is None:
            return
        target_amount = simpledialog.askfloat("Financial Goals", "Enter the target amount:")
        if target_amount is None:
            return
        current_amount = simpledialog.askfloat("Financial Goals", "Enter the current amount:")
        if current_amount is None:
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO financial_goals (goal_name, target_amount, current_amount) VALUES (?, ?, ?)", (goal_name, target_amount, current_amount))
            self.connection.commit()
            messagebox.showinfo("Financial Goals", f"Financial goal '{goal_name}' set successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error setting financial goal: {e}")


    def view_and_edit_goals(self):
        """
        View and edit financial goals.

        Parameters:
        - None

        Returns:
        - None

        Raises:
        - sqlite3.Error: If there is an error viewing or editing financial goals in the database.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM financial_goals")
            goals_data = cursor.fetchall()
            if goals_data:
                goals_str = "\n".join([f"Goal Name: {row[1]}, Target Amount: {row[2]}, Current Amount: {row[3]}" for row in goals_data])
                messagebox.showinfo("Financial Goals", goals_str)
            else:
                messagebox.showinfo("Financial Goals", "No financial goals set.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error viewing financial goals: {e}")


    def view_progress(self):
        """
        View progress towards financial goals.

        Parameters:
        - None

        Returns:
        - None

        Raises:
        - sqlite3.Error: If there is an error viewing progress towards financial goals in the database.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT SUM(current_amount) FROM financial_goals")
            total_current_amount = cursor.fetchone()[0] or 0
            cursor.execute("SELECT SUM(target_amount) FROM financial_goals")
            total_target_amount = cursor.fetchone()[0] or 0
            if total_target_amount > 0:
                progress_percentage = (total_current_amount / total_target_amount) * 100
                messagebox.showinfo("Financial Goals Progress", f"Total progress towards financial goals: {progress_percentage:.2f}%")
            else:
                messagebox.showinfo("Financial Goals Progress", "No financial goals set.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error viewing progress towards financial goals: {e}")


    def quit_app(self):
        """
        Quit the application.

        Parameters:
        - None

        Returns:
        - None
        """
        self.master.destroy()


def main():
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
