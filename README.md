# Third Year Project

Password Manager Project
A python project to simply and securely manage users passwords 

Motivation
===
This project was built as a third-year final year college project to help users manage their passwords securely and locally without relying on vulnerable cloud-based services.

How the system looks 
===
•Heres is the begining of setting up you master user

![image](https://github.com/user-attachments/assets/1516b8d9-2f60-48e5-bff7-16fab2563cc8)

•Here is the running of the password managers cli

![image](https://github.com/user-attachments/assets/43864a3a-5007-443f-aef3-1800e00e5212)

•An example of how the adding user function works

![image](https://github.com/user-attachments/assets/8dc5c4a3-744e-4a7d-ba14-230a2124f0c5)

•An example of the viewing passwords function

![image](https://github.com/user-attachments/assets/a7cecbd0-7122-477d-86a0-f65f9c143337)

•An example of Removing a password
 
![image](https://github.com/user-attachments/assets/e70a12b6-27ee-4888-a251-e373deeb9875)

•An example of an editing an account

![image](https://github.com/user-attachments/assets/c6400409-cd31-4160-8a43-14c2745548f8)

•An example of an error when trying to delete a user that doesnt exist

![image](https://github.com/user-attachments/assets/b6dafb7d-3f0a-490f-a770-f3d015b3960c)

•Finally exiting of the cli

![image](https://github.com/user-attachments/assets/25c454f3-eeb9-4cd2-92cb-9619b1ae9fac)

Features
===
•	Multiple Master Accounts To store different Users passwords

•	Master passwords are hashed using bcrypt.

•	User passwords are encrypted using AES-256 in EAX mode.

•	Users may remove add and view all entries

•	Stored using Sql lite

Technologies used in the Password Manager
===

•	Python 

•	Bcrypt

•	Pycryptodome

•	sqlite


Prerequisites
===

•	Python 3.10+

•	Powershell

File Structure
===
- cli.py – Main command-line interface
- encrypt.py – AES encryption functions
- decrypt.py – AES decryption functions
- setupmaster.py – Used to set the master password using bcrypt
- users.db – SQLite database storing users and encrypted passwords
- requirements.txt - To download all required libraries

How to run
===

1.	git clone https://github.com/B00150644/Projectnew.git

2.	Open Powershell - cd $HOME\Desktop

3.	cd Projectnew

5.	python -m venv venv

7.	.\venv\Scripts\activate

8.	Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process (ONLY IF ERROR)

9.	(If error run this after the policy change ) .\venv\Scripts\Activate.ps1

10.	pip install -r requirements.txt

11.	python .\Cli.py

Sources
===

https://pycryptodome.readthedocs.io/en/latest/

https://www.pycryptodome.org/src/cipher/cipher

https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/

https://geekpython.medium.com/easy-password-hashing-using-bcrypt-in-python-3a706a26e4bf

