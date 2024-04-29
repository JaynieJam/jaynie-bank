import sqlite3
# setting up gui
import tkinter as tk


connection = sqlite3.connect('storage.sqlite')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts 
(
  account_num INTEGER PRIMARY KEY,
  pin INTEGER,
  user_name TEXT,
  current_balance REAL
); 
""")

# print("line 54")

connection.commit()
# connection.close()
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
# new_id = create_new_account('misha', 12345)
# print('created account number:', new_id)
# print('remember this number to access it in the future')
# print()

# # balance check with correct pin
# balance = check_balance(new_id, 12345)
# print(f'(correct pin) balance for account #{new_id} is {balance}')

# # balance check with incorrect pin
# balance = check_balance(new_id, 5678)
# print(f'(wrong pin) balance for account #{new_id} is {balance}')

# print("it reaches line 113")
# cursor.execute('SELECT * FROM accounts')
# print(cursor.fetchall())


def deposit(account_num, pin, amount):
  # use 'update' feature on sql lite
  balance = check_balance(account_num,pin)
  print(f'balance: {balance}')
  if balance != None:
    newBalance = balance + amount
    cursor.execute(
      """ 
      UPDATE accounts
      SET current_balance = @newBalance
      WHERE account_num = ? AND pin = ?
      ;
      """, (newBalance,account_num, pin)
  )
  return newBalance

def withdraw(account_num,pin, amount):
  newBalance = 0;
  balance = check_balance(account_num,pin)
  if balance != None:
    if amount > balance:
      print("insufficient funds")
    else:
      newBalance = balance - amount
      cursor.execute(
        """ 
        UPDATE accounts
        SET current_balance = @newBalance
        WHERE account_num = ? AND pin = ?
        ;
        """, (newBalance,account_num, pin)
  )
  return newBalance
# withdraw
# has funds?
# current funds 50 > 0
# proposed new balance
def changeUserName(user_name,pin,account_num):
  action = input("would you like to change your user_name or pin?")
  if action[:1] == 'u' or 'n':
    newUsername = input("Enter your NEW username: ")
    cursor.execute(
      """ 
      UPDATE accounts
      SET user_name = @newUsername
      WHERE account_num = ? AND pin = ?
      ;
      """, (newUsername,account_num, pin)
    )
  
  return newUsername
def changePin(account_num,pin):
  if action[:1] == 'p':  
    newPin = input("Enter your NEW pin: ")
    cursor.execute(
          """ 
          UPDATE accounts
          SET user_name = @newPin
          WHERE account_num = ? AND pin = ?
          ;
          """, (account_num, newPin, pin)
    )
    return newPin
  
def accountDeletion(account_num,pin):
  dblcheck = input("Are you sure you would like to delete your account? ")
  if dblcheck[:1] == "y":
    cursor.execute(
          """ 
          DELETE FROM accounts
          WHERE account_num = ? AND pin = ?
          ;
          """, (account_num,pin)
    )
    return "You're account is now deleted"
  elif dblcheck[:1] == "n":
    exit()
  else:
    accountDeletion(account_num,pin)
    
  
  

# print(f' accountNum = {account_num}')
# print(f' pin = {pin}')
stillUsing = True
# put it in a function like Parks & Rec? and use recursion to work around edge cases
# def options():
while True:
  action = input("""
  ---------------------------------------------------------
  1. Withdraw
  2. Deposit
  3. Change Name
  4. Change Pin
  5. Remove Account
  6. Quit? 
  (enter the number associated with your desired action)
  ---------------------------------------------------------
  """)
  
   
  if action == '1':
    amount = float(input("Enter the amount you would like to withdraw: "))
    balance = withdraw(account_num, pin, amount)
  elif action == '2':
    amount = float(input("Enter the amount you would like to deposit: "))
    balance = deposit(account_num, pin, amount)
  elif action == '3':
    # returns new user_name
    newUser = changeUserName(userName,account_num, pin)
  elif action == '4':
    newPin = changePin(account_num,pin)
    print(newPin)
  elif action == '5':
    # cursor.execute('SELECT * FROM accounts')
    # print(cursor.fetchall())
    accountDeletion(account_num,pin)
    # cursor.execute('SELECT * FROM accounts')
    # print(cursor.fetchall())
  elif action == '6':
    exit()
  else: 
    print("Try Again")
  
  if balance > 0:
    print(f'{balance}')
  

# cursor.execute("""DELETE FROM accounts
# WHERE user_name = 'misha';""")
# cursor.execute('SELECT * FROM accounts')
# print(cursor.fetchall())
if __name__ == '__main__':
  accountType = input("Are you a new or existing member? ")
  if accountType[:1] == "n":
    print("they're new")
  elif accountType[:1] == "e":
    print("they're a member")
  userName = input("what is your userName: ")
  pin = input("what is your pin number: ")

  account_num = create_new_account(userName,pin)
  options()

# connection.close()

