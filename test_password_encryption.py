import sqlite3

def view_passwords():
    """Connect to the password_manager.db and display all stored passwords."""
    # Connect to the SQLite database
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    # Execute a query to retrieve all rows from the 'passwords' table
    cursor.execute('SELECT account_type, username, encrypted_password FROM passwords')

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Iterate through the rows and print the details
    for row in rows:
        account_type, username, encrypted_password = row
        print(f"Account Type: {account_type}")
        print(f"Username: {username}")
        print(f"Encrypted Password: {encrypted_password}\n")

    # Close the connection
    conn.close()

if __name__ == '__main__':
    view_passwords()
