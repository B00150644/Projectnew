import sqlite3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

# Function to load or generate AES key
def load_or_generate_key():
    key_file = "aes_key.key"
    
    # If key file exists, load it
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read()
    
    # Otherwise, generate a new key and save it
    new_key = get_random_bytes(32)  # AES-256 key
    with open(key_file, "wb") as f:
        f.write(new_key)
    return new_key

AES_KEY = load_or_generate_key()  # Load existing or create a new key

def encrypt_password(plain_password):
    """Encrypts the password using AES."""
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plain_password.encode())
    return base64.b64encode(nonce + ciphertext).decode()

# Hardcoded password
password = "SuperSecure123!"
encrypted_password = encrypt_password(password)

# Print encrypted password
print(f"Encrypted Password (AES): {encrypted_password}")

# Connect to SQLite
conn = sqlite3.connect("password_manager.db")
cursor = conn.cursor()

# Create table if it doesn’t exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        encrypted_password TEXT NOT NULL
    )
""")

# Insert encrypted password
cursor.execute("INSERT INTO passwords (website, username, encrypted_password) VALUES (?, ?, ?)", 
               ("example.com", "user123", encrypted_password))

# Commit & close
conn.commit()
conn.close()

print("Encrypted password has been stored in the database successfully!")
