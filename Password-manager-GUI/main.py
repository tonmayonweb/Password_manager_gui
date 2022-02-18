from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(6, 8)
    nr_symbols = random.randint(2, 3)
    nr_numbers = random.randint(2, 3)

    random_letter = random.sample(letters, nr_letters)
    random_symboll = random.sample(symbols, nr_symbols)
    random_number = random.sample(numbers, nr_numbers)
    password = random_letter + random_symboll + random_number
    random.shuffle(password)
    Generated_password = "".join(password)
    pass_entry.insert(0, Generated_password)
    pyperclip.copy(Generated_password)


# ---------------------- Search ---------------------- #
def search_data():
    search_item = website_entry.get()
    with open("Password_data.json", "r") as data:
        data_file = json.load(data)
    try:
        if data_file[search_item]:
            messagebox.showinfo(title=search_item,
                                message=f"Email:{data_file[search_item]['email']}\nPassword:{data_file[search_item]['password']}")
            pyperclip.copy(f"{data_file[search_item]['password']}")
            messagebox.showinfo(title="Password Manager", message="Password copied to the clip-board")

    except KeyError:
        messagebox.showerror(title=search_item, message="data not fount")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    user_website = website_entry.get()
    user_email = email_entry.get()
    user_password = pass_entry.get()
    new_data = {
        user_website: {
            "email": user_email,
            "password": user_password,
        }
    }
    if len(user_website) > 0 and len(user_email) > 0 and len(user_password) > 0:
        is_ok = messagebox.askokcancel(title="Password Manager",
                                       message=f"Data you entered is ok ?\nWebsite: {user_website}\nEmail: {user_email}\nPassword: {user_password} ")
        if is_ok:
            try:
                with open("Password_data.json", "r") as data:
                    datafile = json.load(data)
                    datafile.update(new_data)
                with open("Password_data.json", "w") as data:
                    json.dump(datafile, data, indent=4)
            except:
                with open("Password_data.json", "w") as data:
                    json.dump(new_data, data, indent=4)

            website_entry.delete(0, END)
            email_entry.delete(0, END)
            pass_entry.delete(0, END)
            pyperclip.copy(user_password)
            messagebox.showinfo(title=user_website, message="Password saved and copied to the clip-board successfully")
    else:
        messagebox.showerror(title="Password Manager", message="Pls fill all the field")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=YELLOW)

#  -------- Canvas-Setting ---------#

canvas = Canvas(width=200, height=200, bg=YELLOW, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# --------- Labels --------- #

website = Label(text="Website:", font=(FONT_NAME, 12, "bold"), bg=YELLOW)
website.grid(row=1, column=0)

Email_user_name = Label(text="Email/Username:", font=(FONT_NAME, 12, "bold"), bg=YELLOW)
Email_user_name.grid(row=2, column=0)

password = Label(text="Password:", font=(FONT_NAME, 12, "bold"), bg=YELLOW)
password.grid(row=3, column=0)

# --------- Entry -------- #

website_entry = Entry(width=22)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=32)
email_entry.insert(0, "abcd@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2)

pass_entry = Entry(width=22)
pass_entry.grid(row=3, column=1, )

# -------- Buttons -------- #

generate = Button(text="Generate", bg=PINK, command=generate_password)
generate.grid(row=3, column=2)

search = Button(text="Search", bg=GREEN, command=search_data)
search.grid(row=1, column=2)

add = Button(width=27, text="Add", bg=GREEN, command=save_password)
add.grid(row=4, column=1, columnspan=2)
window.mainloop()
