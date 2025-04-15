import bcrypt

def setup_master_password():
    password = input("Set a master password: ").encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    with open("master.hash", "wb") as f:
        f.write(hashed)

    print("Master password setup complete.")

if __name__ == "__main__":
    setup_master_password()