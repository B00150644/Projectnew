import sqlite3
from Decrypt import decrypt_password
from Hash import encrypt_password
import bcrypt
import getpass

# Connect to SQLite
conn = sqlite3.connect("password_manager.db")
cursor = conn.cursor()

# Create users tabl database if dont exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        master_hash BLOB NOT NULL
    )
""")

# Create table passwords if it doesnt exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_type TEXT NOT NULL,
        username TEXT NOT NULL,
        encrypted_password TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
""")
# Checks the master password by comparing input to stored bcrypt hash.
def check_master_password():
    try:
        #Trys to open master.hash file
        with open("master.hash", "rb") as f:
            stored_hash = f.read()
    except FileNotFoundError:
        # If master password not set inform user
        print("Master password not set. Run setupmaster.py first.")
        return False
    #asks users for password
    entered_password = input("Enter master password: ").encode('utf-8')
    # Verify the entered password against the stored bcrypt hash
    if bcrypt.checkpw(entered_password, stored_hash):
        print("Access granted.")
        return True
    else:
        print("Access denied.")
        return False
# Prompts user for account credentials and stores them encrypted in the database.    
def add_password(user_id):
    account_type = input("Enter Account Type: ")
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")
    #Encrypts the plaintext password using AES encryption
    encrypted_password = encrypt_password(password)
    # Inserts the account credentials and aes encrypted password into the database
    cursor.execute("""
        INSERT INTO passwords (account_type, username, encrypted_password, user_id)
        VALUES (?, ?, ?, ?)""", (account_type, username, encrypted_password, user_id))
    #commits the transaction and if succesful prints messsage
    conn.commit()
    print("Password stored successfully!")

#fetches and displays all passwords for the logged-in user decrypting each one.    
def view_passwords(user_id):
    # Retrieves all saved passwords for the given user ID
    cursor.execute("SELECT id, account_type, username, encrypted_password FROM passwords WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    #if no entries found error handle
    if not rows:
        print("No passwords found.")
        return
    #Loops through each saved entry and decrypt the password for each until entire database is displayed
    for row in rows:
        id, account_type, username, encrypted_password = row
        decrypted_password = decrypt_password(encrypted_password)
        print(f"Account Number: {id}")
        print(f"Account Type: {account_type}")
        print(f"Username: {username}")
        print(f"Password: {decrypted_password}\n")
#Deletes a password entry from the database by account id not master user id also checks which master user account is being delted from
def remove_password(user_id):
    view_passwords(user_id)

    try:
        #asks user for id of account to be removed and then commits remval to database
        entry_id = int(input("Enter the ID of the account to remove: "))
        cursor.execute("DELETE FROM passwords WHERE id = ? AND user_id = ?", (entry_id, user_id))
        conn.commit()
        #Tells user whether the deletion was successful
        if cursor.rowcount > 0:
            print("Account removed successfully.")
        else:
            print("No account found with that ID.")
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")
#Edit password option reuses add password and deletes account profile from user id
def edit_password(user_id):
    view_passwords(user_id)

    try:
        entry_id = int(input("Enter the Account number of the account to edit: "))
        #Check if the entry exists for this user
        cursor.execute("SELECT * FROM passwords WHERE id = ? AND user_id = ?", (entry_id, user_id))
        if cursor.fetchone() is None:
            print("No account found with that ID.")
            return
        
        #Delete the selected entry
        cursor.execute("DELETE FROM passwords WHERE id = ? AND user_id = ?", (entry_id, user_id))
        conn.commit()
        print("Old account entry removed. Please enter new details:")
        
        #Add a new password which just reuses the old function
        add_password(user_id)

    except ValueError:
        print("Invalid input. Please enter a numeric ID.")

#Authenticates a user by checking their username and master password against the database.     
def login_user():
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()

    username = input("Username: ")
    entered_password = getpass.getpass("Master Password: ").encode('utf-8')

    cursor.execute("SELECT id, master_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result:
        user_id, stored_hash = result
        # Verify entered password using bcrypt
        if bcrypt.checkpw(entered_password, stored_hash):
            print("Login successful.")
            return user_id
        else:
            print("Incorrect password.")
    else:
        print("User not found.")
    
    return None


def main():
    print("Welcome To The Password Manager")
    user_id = login_user()
    if not user_id:
        return

    while True:
        print("\nPassword Manager CLI")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Remove Password")
        print("4. Edit Password")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_password(user_id)
        elif choice == "2":
            view_passwords(user_id)
        elif choice == "3":
            remove_password(user_id)
        elif choice == "4":
            edit_password(user_id)
        elif choice == "5":
            conn.close()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
