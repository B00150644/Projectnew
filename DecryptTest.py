import sqlite3
from Crypto.Cipher import AES
import base64

# Load AES key from file
def load_key():
    with open("aes_key.key", "rb") as f:
        return f.read()

AES_KEY = load_key()  # Load the key

def decrypt_password(encrypted_password):
    """Decrypts the password using AES."""
    encrypted_data = base64.b64decode(encrypted_password)
    nonce = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce=nonce)
    decrypted_password = cipher.decrypt(ciphertext)
    return decrypted_password.decode()

# Connect to SQLite
conn = sqlite3.connect("password_manager.db")
cursor = conn.cursor()

# Fetch the latest stored password
cursor.execute("SELECT Account_type, username, encrypted_password FROM passwords ORDER BY id DESC LIMIT 1")
row = cursor.fetchone()

if row:
    Account_type, username, encrypted_password = row
    decrypted_password = decrypt_password(encrypted_password)
    print(f"Account_type: {Account_type}")
    print(f"Username: {username}")
    print(f"Decrypted Password: {decrypted_password}")
else:
    print("No passwords found in the database.")

conn.close()
