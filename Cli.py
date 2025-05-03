import sqlite3
from Decrypt import decrypt_password
from Hash import encrypt_password
import bcrypt

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
    
def add_password(user_id):
    account_type = input("Enter Account Type: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    encrypted_password = encrypt_password(password)

    cursor.execute("""
        INSERT INTO passwords (account_type, username, encrypted_password, user_id)
        VALUES (?, ?, ?, ?)""", (account_type, username, encrypted_password, user_id))

    conn.commit()
    print("Password stored successfully!")

def view_passwords(user_id):
    cursor.execute("SELECT id, account_type, username, encrypted_password FROM passwords WHERE user_id = ?", (user_id,))
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

def remove_password(user_id):
    view_passwords(user_id)

    try:
        entry_id = int(input("Enter the ID of the account to remove: "))
        cursor.execute("DELETE FROM passwords WHERE id = ? AND user_id = ?", (entry_id, user_id))
        conn.commit()

        if cursor.rowcount > 0:
            print("Account removed successfully.")
        else:
            print("No account found with that ID.")
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")
        
def login_user():
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()

    username = input("Username: ")
    entered_password = input("Master Password: ").encode('utf-8')

    cursor.execute("SELECT id, master_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result:
        user_id, stored_hash = result
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
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_password(user_id)
        elif choice == "2":
            view_passwords(user_id)
        elif choice == "3":
            remove_password(user_id)
        elif choice == "4":
            conn.close()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
