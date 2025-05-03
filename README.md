# Third Year Project

Password Manager Project
A python project to simply and securely manage users passwords 

Motivation
This project was built as a third-year final year college project to help users manage their passwords securely and locally without relying on vulnerable cloud-based services.

How the system looks 

![image](https://github.com/user-attachments/assets/bdd515a7-135f-4b4f-9f7d-f6a06ed9227a)

![image](https://github.com/user-attachments/assets/a80b566b-284c-4e39-bddf-5ed83b8b9605)

![image](https://github.com/user-attachments/assets/24122ff4-63ba-451e-b281-c77ac52d789d)

![image](https://github.com/user-attachments/assets/332a08e7-8a68-4bee-bf1f-de36fdf390cd)

![image](https://github.com/user-attachments/assets/984eb048-7588-4787-92f9-f66369a8939e)

![image](https://github.com/user-attachments/assets/53df9e58-c747-4a6e-8062-d252f10bda20)

![image](https://github.com/user-attachments/assets/90d689f0-14c2-434c-a1a8-98928a90ff32)

Features

•	Master passwords are hashed using bcrypt.

•	Multiple Master Users

•	User passwords are encrypted using AES-256 in EAX mode.

•	Users may remove add and view all entries

Technologies used in the Password Manager

•	Python 

•	Bcrypt

•	Pycryptodome

•	sqlite


Prerequisites

•	Python 3.10+

•	Powershell

File Structure
- cli.py – Main command-line interface
- encrypt.py – AES encryption functions
- decrypt.py – AES decryption functions
- setupmaster.py – Used to set the master password
- users.db – SQLite database storing users and encrypted passwords
- requirements.txt - To download all required libraries

How to run

1.	git clone https://github.com/B00150644/Projectnew.git

2.	Open Powershell - cd $HOME\Desktop

3.	cd Projectnew

4.	python -m venv venv

5.	.\venv\Scripts\activate

6.	pip install -r requirements.txt

7.	python .\Cli.py

Sources 
https://pycryptodome.readthedocs.io/en/latest/
https://www.pycryptodome.org/src/cipher/cipher
https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/
https://geekpython.medium.com/easy-password-hashing-using-bcrypt-in-python-3a706a26e4bf
