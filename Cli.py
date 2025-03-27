import sqlite3
from HashTest import encrypt_password
from DecryptTest import decrypt_password

# Connect to SQLite
conn = sqlite3.connect("password_manager.db")
cursor = conn.cursor()

# Create table if it doesn’t exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Account_type TEXT NOT NULL,
        username TEXT NOT NULL,
        encrypted_password TEXT NOT NULL
    )
""")

def add_password():
    """Add a new password to the database."""
    account_type = input("Enter Account Type: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    encrypted_password = encrypt_password(password)

    cursor.execute("INSERT INTO passwords (Account_type, username, encrypted_password) VALUES (?, ?, ?)", 
                   (account_type, username, encrypted_password))

    conn.commit()
    print("Password stored successfully!")

def view_passwords():
    """Retrieve and display all stored passwords."""
    cursor.execute("SELECT Account_type, username, encrypted_password FROM passwords")
    rows = cursor.fetchall()

    if not rows:
        print("No passwords found.")
        return

    for row in rows:
        account_type, username, encrypted_password = row
        decrypted_password = decrypt_password(encrypted_password)
        print(f"Account Type: {account_type}")
        print(f"Username: {username}")
        print(f"Password: {decrypted_password}\n")

def main():
    while True:
        print("\nPassword Manager CLI")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            conn.close()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
