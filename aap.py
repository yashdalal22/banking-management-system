import tkinter as tk
from tkinter import messagebox
import random
import pymysql.cursors

# Database connection
connection = pymysql.connect(
    host="localhost",
    user='root',
    password="password",  # Replace with your MySQL password
    cursorclass=pymysql.cursors.DictCursor,
    database="user"
)
mycursor = connection.cursor()
#mycursor.execute("create database user")
# mycursor.execute("create table table1(name varchar(30), age int, pin int, state varchar(30), gender varchar(30), balance bigint, account_no bigint)")
# Functions for navigating the UI
def show_main_menu():
    new_user_frame.pack_forget()
    login_user_frame.pack_forget()
    transaction_frame.pack_forget()
    deposit_frame.pack_forget()
    withdraw_frame.pack_forget()
    main_menu_frame.pack()

def show_new_user():
    main_menu_frame.pack_forget()
    new_user_frame.pack()

def show_login_user():
    main_menu_frame.pack_forget()
    login_user_frame.pack()

def show_transaction():
    login_user_frame.pack_forget()
    transaction_frame.pack()

def show_deposit():
    transaction_frame.pack_forget()
    deposit_frame.pack()

def show_withdraw():
    transaction_frame.pack_forget()
    withdraw_frame.pack()

# Function to create a new user
def create_new_user():
    name = name_entry.get()
    age = age_entry.get()
    pin = pin_entry.get()
    state = state_entry.get()
    gender = gender_entry.get()
    account_no = random.randint(10000000000, 99999999999)

    if not (name and age and pin and state and gender):
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        mycursor.execute(
            "INSERT INTO table1 (name, age, pin, state, gender, balance, account_no) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, int(age), int(pin), state, gender, 0, account_no)
        )
        connection.commit()
        messagebox.showinfo("Success", "New user created successfully!\nAccount No: " + str(account_no))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to log in as an existing user
def login_user():
    global logged_in_user
    name = login_name_entry.get()
    pin = login_pin_entry.get()

    if not (name and pin):
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        mycursor.execute("SELECT * FROM table1 WHERE name = %s AND pin = %s", (name, int(pin)))
        user = mycursor.fetchone()

        if user:
            logged_in_user = user
            balance_label.config(text=f"Current Balance: ₹{logged_in_user['balance']}")
            show_transaction()
        else:
            messagebox.showerror("Error", "Invalid credentials.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to deposit money
def deposit_money():
    amount = deposit_entry.get()

    if not amount or not amount.isdigit() or int(amount) <= 0:
        messagebox.showerror("Error", "Please enter a valid amount.")
        return

    new_balance = logged_in_user['balance'] + int(amount)
    try:
        mycursor.execute("UPDATE table1 SET balance = %s WHERE account_no = %s", (new_balance, logged_in_user['account_no']))
        connection.commit()
        logged_in_user['balance'] = new_balance
        balance_label.config(text=f"Current Balance: ₹{new_balance}")
        messagebox.showinfo("Success", f"Deposited ₹{amount} successfully!")
        show_main_menu()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to withdraw money
def withdraw_money():
    amount = withdraw_entry.get()

    if not amount or not amount.isdigit() or int(amount) <= 0:
        messagebox.showerror("Error", "Please enter a valid amount.")
        return

    if int(amount) > logged_in_user['balance']:
        messagebox.showerror("Error", "Insufficient balance.")
        return

    new_balance = logged_in_user['balance'] - int(amount)
    try:
        mycursor.execute("UPDATE table1 SET balance = %s WHERE account_no = %s", (new_balance, logged_in_user['account_no']))
        connection.commit()
        logged_in_user['balance'] = new_balance
        balance_label.config(text=f"Current Balance: ₹{new_balance}")
        messagebox.showinfo("Success", f"Withdrawn ₹{amount} successfully!")
        show_main_menu()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tkinter setup
root = tk.Tk()
root.title("Bank Management System")
root.geometry("400x400")

logged_in_user = None

# Main Menu Frame
main_menu_frame = tk.Frame(root)
main_menu_frame.pack()

tk.Label(main_menu_frame, text="Bank Management System", font=("Arial", 16)).pack(pady=20)

tk.Button(main_menu_frame, text="New User", font=("Arial", 12), command=show_new_user).pack(pady=10)
tk.Button(main_menu_frame, text="Login User", font=("Arial", 12), command=show_login_user).pack(pady=10)
tk.Button(main_menu_frame, text="Exit", font=("Arial", 12), command=root.destroy).pack(pady=10)

# New User Frame
new_user_frame = tk.Frame(root)

name_label = tk.Label(new_user_frame, text="Name:")
name_label.pack()
name_entry = tk.Entry(new_user_frame)
name_entry.pack()

age_label = tk.Label(new_user_frame, text="Age:")
age_label.pack()
age_entry = tk.Entry(new_user_frame)
age_entry.pack()

pin_label = tk.Label(new_user_frame, text="PIN:")
pin_label.pack()
pin_entry = tk.Entry(new_user_frame, show="*")
pin_entry.pack()

state_label = tk.Label(new_user_frame, text="State:")
state_label.pack()
state_entry = tk.Entry(new_user_frame)
state_entry.pack()

gender_label = tk.Label(new_user_frame, text="Gender:")
gender_label.pack()
gender_entry = tk.Entry(new_user_frame)
gender_entry.pack()

tk.Button(new_user_frame, text="Create User", command=create_new_user).pack(pady=10)
tk.Button(new_user_frame, text="Back to Main Menu", command=show_main_menu).pack(pady=10)

# Login User Frame
login_user_frame = tk.Frame(root)

login_name_label = tk.Label(login_user_frame, text="Name:")
login_name_label.pack()
login_name_entry = tk.Entry(login_user_frame)
login_name_entry.pack()

login_pin_label = tk.Label(login_user_frame, text="PIN:")
login_pin_label.pack()
login_pin_entry = tk.Entry(login_user_frame, show="*")
login_pin_entry.pack()

tk.Button(login_user_frame, text="Login", command=login_user).pack(pady=10)
tk.Button(login_user_frame, text="Back to Main Menu", command=show_main_menu).pack(pady=10)

# Transaction Frame
transaction_frame = tk.Frame(root)

tk.Label(transaction_frame, text="Transaction Menu", font=("Arial", 16)).pack(pady=10)

balance_label = tk.Label(transaction_frame, text="", font=("Arial", 12))
balance_label.pack(pady=10)

tk.Button(transaction_frame, text="Deposit", command=show_deposit).pack(pady=5)
tk.Button(transaction_frame, text="Withdraw", command=show_withdraw).pack(pady=5)
tk.Button(transaction_frame, text="Back to Main Menu", command=show_main_menu).pack(pady=10)

# Deposit Frame
deposit_frame = tk.Frame(root)

tk.Label(deposit_frame, text="Deposit Amount:").pack()
deposit_entry = tk.Entry(deposit_frame)
deposit_entry.pack()
tk.Button(deposit_frame, text="Confirm Deposit", command=deposit_money).pack(pady=5)
tk.Button(deposit_frame, text="Back to Transaction Menu", command=show_transaction).pack(pady=10)

# Withdraw Frame
withdraw_frame = tk.Frame(root)

tk.Label(withdraw_frame, text="Withdraw Amount:").pack()
withdraw_entry = tk.Entry(withdraw_frame)
withdraw_entry.pack()
tk.Button(withdraw_frame, text="Confirm Withdraw", command=withdraw_money).pack(pady=5)
tk.Button(withdraw_frame, text="Back to Transaction Menu", command=show_transaction).pack(pady=10)

# Start the application
root.mainloop()