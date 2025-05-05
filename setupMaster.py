import bcrypt
import sqlite3
import getpass

def setup_master_password():
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            master_hash TEXT NOT NULL
        )
    """)
  
    username = input("Enter a new username: ")
    password = getpass.getpass("Set a master password: ").encode('utf-8')  # Use getpass for hidden input
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, master_hash) VALUES (?, ?)", (username, hashed))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists. Choose another.")
    
    conn.close()

if __name__ == "__main__":
    setup_master_password()
