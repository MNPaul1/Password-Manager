from email.policy import EmailPolicy
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = []
    password_symbols = []
    password_numbers = []

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]

    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)
    password_entry.delete(0,END)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website = web_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website:{
            "email" : email,
            "password" : password
        }
    }
    if len(website) != 0 and len(email)!=0 and len(password) != 0:
        is_ok = messagebox.askokcancel(title = website, message=f"These are the details entered: \nEmail: {email} \nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                with open("day_29/data.json", "r") as file:
                    data = json.load(file)
                    
            except FileNotFoundError:
                with open("day_29/data.json", "w") as file:
                    json.dump(new_data, file, indent=4)

            else:
                data.update(new_data)
                with open("day_29/data.json", "w") as file:
                    json.dump(data, file, indent=4)

            finally:
                web_entry.delete(0, END)
                password_entry.delete(0, END)
    else:
        messagebox.showinfo(title = "Oops", message = "Please don't leave any field empty!")


def search():
    website = web_entry.get().capitalize()
    try:
         with open("day_29/data.json", "r") as file:
            data = json.load(file)
            messagebox.showinfo(title=website, message=f"Email: {data[website]['email']} \n Password: {data[website]['password']}")
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
    except KeyError:
        messagebox.showerror(title="Error", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx = 50, pady = 50)

canvas = Canvas(width = 200, height = 200)

lock_img = PhotoImage(file = "day_29/logo.png")
canvas.create_image(100, 100, image = lock_img)
canvas.grid(column=1, row=0)

website_label = Label(text = "Website:")
website_label.grid(column = 0, row = 1)

email_label = Label(text = "Email/Username:")
email_label.grid(column = 0, row = 2)

password_label = Label(text = "Password:")
password_label.grid(column = 0, row = 3)

web_entry = Entry(width = 17)
web_entry.grid(column = 1, row = 1, columnspan = 1)
web_entry.focus()

email_entry = Entry(width = 35)
email_entry.insert(0, "mnpaul@example.com")
email_entry.grid(column = 1, row = 2, columnspan = 2)

password_entry = Entry(width = 17, highlightthickness=0)
password_entry.grid(column = 1, row = 3, padx=0)

generate_password_btn = Button(text = "Generate Password", highlightthickness=0, command = generate_password)
generate_password_btn.grid(column = 2, row = 3, sticky = 'w', padx=0)

add_btn = Button(text = "Add", width = 30, command = add_password)
add_btn.grid(column = 1, row = 4, columnspan = 2)

search_btn = Button(text = "Search", command = search)
search_btn.grid(column=2, row = 1)
window.mainloop()