import sqlite3
# setting up gui
import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Jaynie's Banking APP")
window.config(bg="bisque")
# window.geometry(200x200)
window.geometry("200x200")
# put text onto gui
greeting = tk.Label(text="Welcome, to Jaynie Bank",bg="white",font=("Times New Roman", 16))
greeting.pack(side = "top")
# puts button onto gui
def logBtn():
  logIn = tk.Button(window, text="Log In", background="red")
  logIn.pack(side = "bottom", padx = 20,pady= 20)

logBtn()

def enterInfo():
  userTxt = tk.Label(window, text= "User name")
  userTxt.pack(padx= 10,pady = 10)
  userInput = tk.Entry(window)
  userInput.pack(padx = 5, pady=5)
enterInfo()
# Set column and row weight
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# Make the window resizable
window.resizable(True, True)
window.mainloop()
# global variables for database access
connection = sqlite3.connect('storage.sqlite')
cursor = connection.cursor()

# initial setup - create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts 
(
  account_num INTEGER PRIMARY KEY,
  pin INTEGER,
  user_name TEXT,
  current_balance REAL
);
""")

def create_new_account(user_name, pin):
  """
  Create new account with zero balance.
  Return the account number just created.
  """
  cursor.execute("""
    INSERT INTO accounts (
      pin, user_name, current_balance
      ) 
    VALUES (?, ?, 0.0);
  """, (pin, user_name))
  # always call commit when updating table
  connection.commit()
  
  # to retreive the last inserted account number
  # MySQL has equivalent function: LAST_INSERT_ID()
  cursor.execute("SELECT last_insert_rowid();")
  last_id = cursor.fetchall()[0][0]
  
  return last_id
  
def check_balance(account_num, pin):
  """
  Check balance by account number and pin. 
  Return None if account_num + pin is invalid.
  """
  cursor.execute("""
    SELECT current_balance
    FROM accounts
    WHERE account_num = ? AND pin = ?
    ;
    """, (account_num, pin)
  )
  
  results = cursor.fetchall()
  if len(results) != 1:
    return None
  return results[0][0]

# to add deposit or withdrawal functionality
# read about UPDATE statement in SQL


# sample interaction with banking app:
new_id = create_new_account('misha', 12345)
print('created account number:', new_id)
print('remember this number to access it in the future')
print()

# balance check with correct pin
balance = check_balance(new_id, 12345)
print(f'(correct pin) balance for account #{new_id} is {balance}')

# balance cehck with incorrect pin
balance = check_balance(new_id, 5678)
print(f'(wrong pin) balance for account #{new_id} is {balance}')


connection.close()