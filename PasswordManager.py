import os
import bcrypt
import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# File storage
DB_FILE = "passwords.json"
MASTER_PASSWORD_FILE = "master_password.json"

def load_passwords():
    """Load saved passwords from JSON."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return json.load(file)
    return {}

def save_passwords(data):
    """Save passwords to JSON."""
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

def hash_master_password(password):
    """Hash the master password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_master_password(stored_hash, password):
    """Verify entered master password against stored hash."""
    return bcrypt.checkpw(password.encode(), stored_hash)

def encrypt_password(password, key):
    """Encrypt password using AES encryption."""
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted = cipher.encrypt(pad(password.encode(), AES.block_size))
    return cipher.iv + encrypted

def decrypt_password(encrypted_data, key):
    """Decrypt AES-encrypted password."""
    iv = encrypted_data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size).decode()

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("400x300")

        self.key = None

        tk.Label(root, text="Master Password:").pack()
        self.master_entry = tk.Entry(root, show="*", width=30)
        self.master_entry.pack()
        tk.Button(root, text="Login", command=self.authenticate).pack()

    def authenticate(self):
        master_password = self.master_entry.get()
        if not os.path.exists(MASTER_PASSWORD_FILE):
            hashed_password = hash_master_password(master_password)
            with open(MASTER_PASSWORD_FILE, "w") as file:
                json.dump({"master_password": hashed_password.decode()}, file)
            messagebox.showinfo("Success", "Master password set!")
        else:
            with open(MASTER_PASSWORD_FILE, "r") as file:
                stored_hash = json.load(file)["master_password"].encode()
            if not verify_master_password(stored_hash, master_password):
                messagebox.showerror("Error", "Incorrect Master Password")
                return
        
        self.key = pad(master_password.encode(), AES.block_size)[:32]
        self.load_main_screen()

    def load_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Password Manager", font=("Arial", 14)).pack()
        tk.Button(self.root, text="Add Password", command=self.add_password).pack()
        tk.Button(self.root, text="View Passwords", command=self.view_passwords).pack()
        tk.Button(self.root, text="Search Password", command=self.search_password).pack()

    def add_password(self):
        service = simpledialog.askstring("Input", "Enter service name:")
        username = simpledialog.askstring("Input", "Enter username:")
        password = simpledialog.askstring("Input", "Enter password:")
        
        if service and username and password:
            passwords = load_passwords()
            encrypted_password = encrypt_password(password, self.key)
            passwords[service] = {"username": username, "password": encrypted_password.hex()}
            save_passwords(passwords)
            messagebox.showinfo("Success", "Password added successfully!")

    def view_passwords(self):
        passwords = load_passwords()
        result = ""
        for service, details in passwords.items():
            decrypted_password = decrypt_password(bytes.fromhex(details["password"]), self.key)
            result += f"Service: {service}\nUsername: {details['username']}\nPassword: {decrypted_password}\n\n"
        messagebox.showinfo("Stored Passwords", result)

    def search_password(self):
        service = simpledialog.askstring("Search", "Enter service name:")
        passwords = load_passwords()
        if service in passwords:
            details = passwords[service]
            decrypted_password = decrypt_password(bytes.fromhex(details["password"]), self.key)
            messagebox.showinfo("Password Found", f"Service: {service}\nUsername: {details['username']}\nPassword: {decrypted_password}")
        else:
            messagebox.showinfo("Not Found", "No password found for this service.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()