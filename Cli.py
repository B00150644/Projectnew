import sqlite3
from DecryptTest import decrypt_password
from HashTest import encrypt_password
import bcrypt

# Connect to SQLite
conn = sqlite3.connect("password_manager.db")
cursor = conn.cursor()

# Create table if it doesn’t exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_type TEXT NOT NULL,
        username TEXT NOT NULL,
        encrypted_password TEXT NOT NULL
    )""")

def check_master_password():
    try:
        with open("master.hash", "rb") as f:
            stored_hash = f.read()
    except FileNotFoundError:
        print("Master password not set. Run setupmaster.py first.")
        return False

    entered_password = input("Enter master password: ").encode('utf-8')

    if bcrypt.checkpw(entered_password, stored_hash):
        print("Access granted.")
        return True
    else:
        print("Access denied.")
        return False
    
def add_password():
    """Add a new password to the database."""
    account_type = input("Enter Account Type: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    encrypted_password = encrypt_password(password)

    cursor.execute("INSERT INTO passwords (account_type, username, encrypted_password) VALUES (?, ?, ?)", 
                   (account_type, username, encrypted_password))

    conn.commit()
    print("Password stored successfully!")

def view_passwords():
    """Retrieve and display all stored passwords."""
    cursor.execute("SELECT id, account_type, username, encrypted_password FROM passwords")
    rows = cursor.fetchall()

    if not rows:
        print("No passwords found.")
        return

    for row in rows:
        id, account_type, username, encrypted_password = row
        decrypted_password = decrypt_password(encrypted_password)
        print(f"Account Number: {id}")
        print(f"Account Type: {account_type}")
        print(f"Username: {username}")
        print(f"Password: {decrypted_password}\n")

def remove_password():
    """Remove a password entry by ID."""
    view_passwords()  # Show all entries to help user choose

    try:
        entry_id = int(input("Enter the ID of the account to remove: "))
        cursor.execute("DELETE FROM passwords WHERE id = ?", (entry_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print("Account removed successfully.")
        else:
            print("No account found with that ID.")
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")
        
def main():
    if not check_master_password():
        return  # Exit if master password check fails
     

    while True:
                print("\nPassword Manager CLI")
                print("1. Add Password")
                print("2. View Passwords")
                print("3. Remove Password")
                print("4. Exit")

                choice = input("Enter your choice: ")

                if choice == "1":
                    add_password()
                elif choice == "2":
                    view_passwords()
                elif choice == "3":
                    remove_password()
                elif choice == "4":
                    conn.close()
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
