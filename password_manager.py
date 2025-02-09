import os
import json
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from helper_funcs import check_input, read_key, encrypt_password, decrypt_password

# Simple password manager, only to store passwords and usernames, not passwords for certain websites.
# Implementation of cryptography, GUI and data manipulation.

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
json_file_path = os.path.join(__location__, 'users_passwords.json')

# Function to hide/show the password.
def show_pass():
    if var.get() == 1:
        password_text.configure(show="")
    elif var.get() == 0:
        password_text.configure(show="*")


def save_pass():
    r'''This function checks the text boxes and makes sure the
            following conditions are met:
        
        - No empty text boxes;
        - Username cannot be the same as one previously entered.

        If all conditions above are met, username and password will be saved
            and the password will be encrypted.
    '''
    # Variables
    username = username_text.get().replace(' ','')
    password = password_text.get().replace(' ','')

    # Empty text boxes errors
    if check_input(username_text, password_text):
        # Load the JSON file with the usernames and passwords
        # If the file has no content, we'll provide an empty dictionary
        try: 
            with open(json_file_path, 'r') as f:
                data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = {}

        # Initialize cipher for password encryption
        cipher = read_key(__location__)

        # Check if the username exists in the JSON file
        if username in data:
            messagebox.showerror(title="Error", message="Username already in file!")
        else:
            # Password has to be encrypted
            data[username] = encrypt_password(cipher, password)
            # Save the content
            with open(json_file_path, 'w') as f: 
                json.dump(data, f, indent=4)
                
            # Message to show that the data was saved
            messagebox.showinfo(title="Completed", message="Password saved!")


def get_password():
    r'''This function checks the username text box and makes sure the
            username is inputted.
        Also, the username has to be inside of the JSON file, otherwise
            no password can be retrieved.

        Returns:
            Password inputted into the text box
    '''
    if check_input(username_text):
        # Try to retrieve password from JSON file
        try: 
            with open(json_file_path, 'r') as f:
                data = json.load(f)
            
            # Retrieve password
            cipher = read_key(location=__location__)

            # Check if username is saved
            username = username_text.get().replace(' ','')
            if username in data.keys():
                decrypted_password = decrypt_password(cipher, data[username])
                password_text.delete(0, tk.END)
                password_text.insert(index=0, string=decrypted_password)
            else:
                messagebox.showerror(title="Error", message="Username not saved!")

        except json.decoder.JSONDecodeError:
            messagebox.showerror(title="Error", message="No password for inputted username!")



def list_elements():
    r'''This function returns all the usernames on the JSON file.
        To then get the password for a username, the get password
            button should be pressed.
    '''
    try: 
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        # Gather all the usernames
        users = [user.strip('"\'') for user in data.keys()]
        messagebox.showinfo(title="Usernames Saved", message=users)
    except json.decoder.JSONDecodeError:
        messagebox.showerror(title="Error", message="Empty file!")


if __name__ == "__main__":
    # Create the GUI
    gui = tk.Tk(className=' Password Manager')
    # Set Window Size
    gui.geometry('500x300')
    
    # Create the username and password text boxes
    username_text = tk.Entry(gui, bg='white', font=("Helvetica", 14))
    password_text = tk.Entry(gui, bg='white', font=("Helvetica", 14), show='*')

    # Initialize Integer Manager
    var = tk.IntVar()
    
    # Create the labels for the text boxes
    username_label = tk.Label(gui, text='Username:', font=("Helvetica", 14, "bold"))
    password_label = tk.Label(gui, text='Password:', font=("Helvetica", 14, "bold"))

    # Place the content on the GUI
    username_label.grid(column=0, row=0, pady=15), password_label.grid(column=0, row=1, padx=20, pady=15)
    username_text.grid(column=1, row=0, pady=15), password_text.grid(column=1, row=1, padx=20, pady=15)

    # Create buttons (Save, Exit, Show Password, Get Password, Get List of Usernames and Passwords)
    save_btn = tk.Button(master=gui, text='Save Password', command=save_pass, font=("Helvetica", 10, "bold"), width=15)
    exit_btn = tk.Button(master=gui, text='Exit', command=gui.quit, font=("Helvetica", 10, "bold"), width=10)
    show_btn = tk.Checkbutton(master=gui, command=show_pass, offvalue=0, onvalue=1, variable=var)
    get_password_btn = tk.Button(master=gui, text='Get Password', command=get_password, font=("Helvetica", 10, "bold"), width=15)
    list_btn = tk.Button(master=gui, text='List', command=list_elements, font=("Helvetica", 10, "bold"), width=10)

    # Place the buttons on the GUI
    save_btn.place(x=100, y=200)
    exit_btn.place(x=300, y=200)
    show_btn.grid(column=2, row=1)
    get_password_btn.place(x=100, y=250)
    list_btn.place(x=300, y= 250)

    # Make sure the enter key has a purpose -> Save Password
    gui.bind('<Return>', lambda event: save_btn.invoke())

    gui.mainloop()