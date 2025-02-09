import os
from tkinter import messagebox
from cryptography.fernet import Fernet

# In this file, some smaller functions are defined for usage in the main python file

# Generate a secret key.
def generate_key():
   return Fernet.generate_key()

# Initialize Fernet cipher with the provided key.
def initialize_cipher(key):
   return Fernet(key)

# Function to encrypt a password.
def encrypt_password(cipher, password):
   return cipher.encrypt(password.encode()).decode()

# Function to decrypt a password.
def decrypt_password(cipher, encrypted_password):
   return cipher.decrypt(encrypted_password.encode()).decode()


def check_input(*args):
    r'''This function checks the text boxes and makes sure there are no
            empty text boxes.
    '''
    # Boolean variable to track conditions
    value = True

    # Both username and password inputted
    if len(args) == 2:
        if not args[0].get().replace(' ','') or not args[1].get().replace(' ',''):
            messagebox.showerror(title="Error", message="Empty username and/or password")
            value = False
    # Only the username inputted
    else:
        if not args[0].get().replace(' ',''):
            messagebox.showerror(title="Error", message="Empty username")
            value = False

    # Return the boolean variable
    return value


def read_key(location: str):
    r'''This function loads or generates the encryption key, while
            also retrieving the key
    '''
     # Load or generate the encryption key.
    key_filename = 'encryption_key.key'
    # Check if file exists
    if os.path.exists(os.path.join(location, key_filename)):
        with open(os.path.join(location, key_filename), 'rb') as key_file:
            key = key_file.read()
    else:
        key = generate_key()
        with open(os.path.join(location, key_filename), 'wb') as key_file:
            key_file.write(key)

    # Initialize cipher for password encryption and return it
    return initialize_cipher(key)


