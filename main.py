from tkinter import *
from tkinter import messagebox
import pyperclip
import json

DEFAULT_MAIL = "example@email.com"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():

    from random import randint, choice, shuffle


    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    password_list += [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)

    password_input.delete(0, END)
    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Don't leave any fields empty!")
    else:
        try:
            with open("passwords.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            with open("passwords.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            data.update(new_data)
            with open("passwords.json", "w") as f:
                json.dump(data, f, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)

            messagebox.showinfo(title="Success!", message="Your password has been successfully added!")


def search_password():
    website_searched = website_input.get()
    try:
        with open("passwords.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Sorry, the library of Password Manager is currently empty.")
    else:
        if website_searched in data:
            email = data[website_searched]["email"]
            password = data[website_searched]["password"]
            messagebox.showinfo(title=website_searched, message=f"Email: {email} \nPassword: {password}")
        else:
            messagebox.showinfo(title="Website not found", message=f"Sorry, there's no password found for {website_searched}.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Paassword:")
password_label.grid(column=0, row=3)

website_input = Entry(width=21)
website_input.grid(column=1, row=1, columnspan=1)
website_input.focus()

email_input = Entry(width=40)
email_input.grid(column=1, row=2, columnspan=2)
email_input.insert(0, DEFAULT_MAIL)

password_input = Entry(width=21)
password_input.grid(column=1, row=3)

search_button = Button(text="Search", command=search_password, width=15)
search_button.grid(column=2, row=1, columnspan=1)

generate_button = Button(text="Generate Password", command=generate_password, width=15)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", command=save_password, width=36)
add_button.grid(column=1, row=4, columnspan=2)


window.mainloop()