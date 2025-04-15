import base64
from Crypto.Cipher import AES

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
