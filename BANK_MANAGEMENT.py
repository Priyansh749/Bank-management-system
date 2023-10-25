import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import pandas as pd

# Define a BankAccount class to represent individual bank accounts
class BankAccount:
    def __init__(self, owner, balance=0, account_number=""):
        self.owner = owner
        self.balance = balance
        self.account_number = account_number

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            return "Insufficient funds."

    def get_balance(self):
        return self.balance

# Initialize a list to store messages for display
messages = []

# Initialize a dictionary to store bank accounts
accounts = {}

# Function to create a new bank account
def create_account(owner, initial_balance, account_number):
    if account_number in accounts:
        return f"Account number {account_number} is already in use."

    # Create a DataFrame to store the account data and add it to the CSV file
    account_data = pd.DataFrame([[owner, initial_balance, account_number]],
                                columns=["Owner", "Balance", "Account Number"])
    try:
        df = pd.read_csv("accounts.csv", encoding='utf-8')
        df = pd.concat([df, account_data], ignore_index=True)
    except FileNotFoundError:
        df = account_data
    df.to_csv("accounts.csv", index=False)

    # Create a BankAccount object and add it to the accounts dictionary
    account = BankAccount(owner, initial_balance, account_number)
    accounts[account_number] = account

    return f"Account for {owner} created successfully!"

# Function to handle the "Add Account" button click
def create_account_button():
    owner_name_value = owner_name.get_text()
    initial_balance_value = initial_balance.get_text()

    # Validate input fields
    if not owner_name_value:
        messages.append("Owner name cannot be empty.")
        return

    try:
        initial_balance_value = float(initial_balance_value)
        if initial_balance_value <= 0:
            messages.append("Initial balance must be a positive number.")
            return
    except ValueError:
        messages.append("Initial balance must be a valid number.")
        return

    account_number_value = account_number.get_text()

    # Validate account number format
    if not account_number_value.isdigit():
        messages.append("Account number must be a numeric value.")
        return

    # Account creation logic...
    result = create_account(owner_name_value, initial_balance_value, account_number_value)
    messages.append(result)

# Function to handle the "Deposit" button click
def deposit_button():
    global messages
    messages=[]
    deposit_account_number_value = deposit_account_number.get_text()
    deposit_amount_value = deposit_amount.get_text()

    # Validate input fields
    if not deposit_account_number_value or not deposit_amount_value:
        messages.append("Account number and deposit amount cannot be empty.")
        return

    try:
        deposit_account_number_value = str(int(deposit_account_number_value))  # Ensure account number is a string
        deposit_amount_value = float(deposit_amount_value)

        if deposit_amount_value <= 0:
            messages.append("Deposit amount must be a positive number.")
            return
    except ValueError:
        messages.append("Invalid input. Please check your account number and deposit amount.")
        return

    # Deposit logic...
    if deposit_account_number_value in accounts:
        account = accounts[deposit_account_number_value]
        account.deposit(deposit_amount_value)
        messages.append(f"Deposited {deposit_amount_value} into account {deposit_account_number_value}")
        deposit_account_number.set_text("")
        deposit_amount.set_text("")
    else:
        messages.append(f"Account {deposit_account_number_value} not found")

# Similar validation and error handling can be applied to other functions as well.

# Function to display information of all accounts
# Function to display information of all accounts
def display_all_account_button():
    messages.clear()  # Clear the messages list
    # Check if there are accounts in the CSV file
    try:

        df = pd.read_csv("accounts.csv", encoding='utf-8')
        if df.empty:
            messages.append("No accounts available.")
            return
    except FileNotFoundError:
        messages.append("No accounts available.")
        return

    # Sort the DataFrame by account number
    df = df.sort_values(by=["Account Number"])

    # Display account information
    for index, row in df.iterrows():
        owner = row["Owner"]
        balance = row["Balance"]
        account_number = row["Account Number"]
        messages.append(f"Owner: {owner}, Balance: {balance}, Account Number: {account_number}")

# Function to handle the "Withdraw" button click
def withdraw_button():
    global withdraw_amount_value, withdraw_account_number_value
    account_number = withdraw_account_number.get_text()
    amount = float(withdraw_amount.get_text())
    messages.clear()
    if account_number in accounts:
        account = accounts[account_number]
        if account.balance >= amount:
            account.withdraw(amount)
            messages.append(f"Withdrew {amount} from account {account_number}")
        else:
            messages.append(f"Insufficient balance for account {account_number}")
    else:
        messages.append(f"Account {account_number} not found")
    withdraw_account_number_value = ""
    withdraw_amount_value = ""

# Function to display account information
def display_account_info():
    global display_account_number_value, messages
    messages.clear()
    account_number = display_account_number.get_text()
    if account_number in accounts:
        account = accounts[account_number]
        owner = account.owner
        balance = account.balance
        messages.append(f"Account Number: {account_number}, Owner: {owner}, Balance: {balance}")
    else:
        messages.append(f"Account {account_number} not found")
    display_account_number_value = ""

# Function to handle the "Transfer" button click
def transfer_button():
    global accounts, messages
    messages.clear()
    from_account_number = transfer_from_account.get_text()
    to_account_number = transfer_to_account.get_text()
    amount = float(transfer_amount.get_text())
    if from_account_number in accounts and to_account_number in accounts:
        from_account = accounts[from_account_number]
        to_account = accounts[to_account_number]
        if from_account.balance >= amount:
            from_account.withdraw(amount)
            to_account.deposit(amount)
            messages.append(f"Transferred {amount} from account {from_account_number} to account {to_account_number}")
        else:
            messages.append(f"Insufficient balance in account {from_account_number}")
    else:
        messages.append("One or both accounts not found")
    # Clear input field values
    transfer_from_account.set_text("")
    transfer_to_account.set_text("")
    transfer_amount.set_text("")

# Function to handle the "Delete Account" button click
def delete_account_button():
    global accounts, messages
    messages.clear()
    account_number = account_to_delete.get_text()
    if account_number in accounts:
        del accounts[account_number]
        messages.append(f"Account {account_number} deleted.")
        # Remove the account from the DataFrame and save
        df = pd.read_csv("accounts.csv", encoding='utf-8')
        df = df[df["Account Number"] != account_number]
        df.to_csv("accounts.csv", index=False)
    else:
        messages.append(f"Account {account_number} not found")
    # Clear input field value
    account_to_delete.set_text("")

# Function to handle the "Delete All Accounts" button click
def delete_all_accounts_button():
    global accounts, messages
    messages.clear()
    accounts.clear()  # Clear the accounts dictionary
    messages.append("All accounts deleted.")
    df = pd.DataFrame(columns=["Owner", "Balance", "Account Number"])
    df.to_csv("accounts.csv", index=False)  # Overwrite the CSV file with an empty DataFrame

# Function to draw messages on the GUI
def draw_handler(canvas):
    canvas.draw_text("Bank Management System", (20, 30), 40, "white")
    y = 80
    for message in messages:
        canvas.draw_text(message, (20, y), 30, "Red")
        y += 50  # Adjust the vertical spacing for better readability

# Create a GUI frame
frame = simplegui.create_frame("Frame", 800, 700, 400)

# Add input fields and buttons to the frame
owner_name = frame.add_input("Owner Name:", create_account, 200)
initial_balance = frame.add_input("Initial Balance:", create_account, 200)
account_number = frame.add_input("Account Number:", create_account, 200)
frame.add_button("Add Account", create_account_button)

deposit_account_number = frame.add_input("Account Number:", deposit_button, 200)
deposit_amount = frame.add_input("Deposit Amount:", deposit_button, 200)
frame.add_button("Deposit", deposit_button)

withdraw_account_number = frame.add_input("Account Number:", withdraw_button, 200)
withdraw_amount = frame.add_input("Withdraw Amount:", withdraw_button, 200)
frame.add_button("Withdraw", withdraw_button)

display_account_number = frame.add_input("Account Number:", display_account_info, 200)
frame.add_button("Display Account Info", display_account_info)

transfer_from_account = frame.add_input("From Account:", transfer_button, 200)
transfer_to_account = frame.add_input("To Account:", transfer_button, 200)
transfer_amount = frame.add_input("Transfer Amount:", transfer_button, 200)
frame.add_button("Transfer", transfer_button)

account_to_delete = frame.add_input("Account Number:", delete_account_button, 200)
frame.add_button("Delete Account", delete_account_button)

display_all_account = frame.add_button("Display All Account", display_all_account_button)
frame.add_button("Delete All Accounts", delete_all_accounts_button)

# Set the draw handler for the frame
frame.set_draw_handler(draw_handler)

# Start the GUI frame
frame.start()
