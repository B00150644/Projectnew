import base64
from Crypto.Cipher import AES

#This script decrypts an AES-encrypted password that was previously encoded using AES in EAX mode and base64 encoded.
#The AES key is first loaded from the file named aes_key.key. This key must be the same one that was used to encrypt the password.
#The function then takes the base64 encoded string (which includes both the nonce and the ciphertext) decodes it and splits it into the nonce (first 16 bytes) and the actual ciphertext.
#""Nonce is the unique one time use number added to encryption to ensure each ciphertext is different even if they have the same input.""
#An AES cipher object is recreated in EAX mode using the same nonce and aes key which is necessary to decrypt the data.
#Finally the ciphertext is decrypted and returned as a UTF-8 string.

#Load AES key from file
def load_key():
    with open("aes_key.key", "rb") as f:
        return f.read()

AES_KEY = load_key()  #Load the aes256 key for decryption

#Decrypts a base64 encoded password string encrypted with AES EAX mode
def decrypt_password(encrypted_password):
#Decode the base64encoded string to retrieve the raw bytes
    encrypted_data = base64.b64decode(encrypted_password)
#Extract the first 16 bytes as the nonce (used during encryption) in AES EAX mode the nonce is 16 bytes
    nonce = encrypted_data[:16]
#The remainder is the ciphertext
    ciphertext = encrypted_data[16:]
#Recreates the cipher using the AES key and nonce
    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce=nonce)
#Decrypts the ciphertext and decodes from bytes to string
    decrypted_password = cipher.decrypt(ciphertext)
    return decrypted_password.decode()
