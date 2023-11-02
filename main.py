from tkinter import *
from tkinter import messagebox  # It is not a Class, that is why it needs to be called by itself.
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]

    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)

    password = "".join(password_list)  # it joins the characters.
    password_label_input.insert(0, password)
    pyperclip.copy(password)  # It copies the password so the user avoid that step.


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_entry_input.get()
    try:
        with open("my_passwords.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message=f"No Data File Found. Save at least one website'password")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists")


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry_input.get()
    email = email_username_input.get()
    password = password_label_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,

        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo("Oops", "Please don't leave any field empty!")
    else:
        try:
            with open("my_passwords.json", "r") as my_passwords_file:
                # Reading old data
                data = json.load(my_passwords_file)
        except FileNotFoundError:
            with open("my_passwords.json", "w") as my_passwords_file:
                json.dump(new_data, my_passwords_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("my_passwords.json", "w") as my_passwords_file:
                # Saving updated data
                json.dump(data, my_passwords_file, indent=4)

        finally:
            website_entry_input.delete(0, END)
            password_label_input.delete(0, END)

    # ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)  # 100 100 arguments are half of Canvas's size 200.
canvas.grid(column=1, row=0)

# Website Label
website_label = Label(text="Website:")
website_label.grid(column=0, row=1, sticky=EW)
#  Entry for Website Label
website_entry_input = Entry(width=35)
website_entry_input.grid(column=1, row=1, columnspan=2, sticky=EW)
website_entry_input.focus()  # It converts the mouse cursor into writing mode.
#  Generate Password Button
website_search_button = Button(text="Search", command=find_password)
website_search_button.grid(column=2, row=1, sticky=EW)

# Email/Username Label
email_username = Label(text="Email/Username:")
email_username.grid(column=0, row=2, sticky=EW)
#  Entry for Email/Username Label
email_username_input = Entry(width=35)
email_username_input.grid(column=1, row=2, columnspan=2, sticky=EW)
email_username_input.insert(0, "emiliomorles@test.com")  # an example of what to write

# Password Label
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
#  Entry for Password Label
password_label_input = Entry(width=21)
password_label_input.grid(column=1, row=3, sticky=EW)
#  Generate Password Button
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3, sticky=EW)

#  Add Password Button
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky=EW)

window.mainloop()
