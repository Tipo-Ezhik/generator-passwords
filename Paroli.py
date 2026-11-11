import tkinter as tk
import random
import string
import json
import os
from tkinter import messagebox
from key import KEY

KEY = KEY

def xor_encrypt(text, key):
    return "".join(chr(ord(text[i]) ^ ord(key[i % len (key)])) for i in range (len(text)))# если xаковы то 0 аor цифры один если разные то 1

def xor_decrypt(text, key):
    return xor_encrypt(text, key)

FILE = 'vault.json'

if not os.path.exists(FILE):
    with open(FILE, 'w') as f:
        json.dump([], f)

def load():
    with open(FILE, "r") as f:
        return json.load(f)
    
def save(data):
    with open(FILE, 'w')as f:
        json.dump(data, f, indent = 2)

data = load()
LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = '!@#$%^&*()-_+=[]{}:;,.?/'

def generate_password(lenght = 12):
    pool = LOWER + UPPER + DIGITS + SYMBOLS

    pwd = [
        random.choice(LOWER),
        random.choice(UPPER),
        random.choice(DIGITS),
        random.choice(SYMBOLS),
    ]

    for _ in range(lenght - 4):
        pwd.append(random.choice(pool))

    random.shuffle(pwd)
    return "".join(pwd)

def refresh_list(filtered = None):
    listbox.delete(0, tk.END)

    show = filtered if filtered is not None else data

    for item in show:
            pwd = xor_decrypt(item['password'],KEY)
            listbox.insert(
                tk.END,
                f"{item['service']} | {item['login']}"
            )

def add_entry():
    service = entry_service.get()
    login = entry_login.get()
    lenght = int(entry_length.get())

    pwd = generate_password(lenght)
    enc = xor_encrypt(pwd,KEY)

    data.append({
        'service':service,
        'login': login,
        'password': enc
    })

    save(data)
    refresh_list()

    entry_service.delete(0, tk.END)
    entry_login.delete(0, tk.END)

def delete_entry():
    sel = listbox.curselection()
    if not sel:
        return
    del data[sel[0]]
    save(data)
    refresh_list()

def copy_password():
    sel = listbox.curselection()
    if not sel:
        return
    
    item = data[sel[0]]
    pwd = xor_decrypt(item["password"], KEY)

    root.clipboard_clear()
    root.clipboard_append(pwd)

def copy_password():
    sel = listbox.curselection()
    if not sel:
        return
    item = data[sel[0]]
    pwd = xor_decrypt(item["password"], KEY)
    root.clipboard_clear()
    root.clipboard_append(pwd)
    strength = password_strength(pwd)
    messagebox.showinfo('Пароль', f"{pwd}\n\nНадежность: {strength}\n\nПароль скопирован в буфер обмена!")

    
def copy_login():
    sel = listbox.curselection()
    if not sel:
        return
    item = data[sel[0]]
    login = item['login']
    root.clipboard_clear()
    root.clipboard_append(login)

def search():
    q = entry_search.get().lower()
    filtered = [
        i for i in data
        if q in i['service'].lower()
    ]
    refresh_list(filtered)

root = tk.Tk()
root.title('Password Manager Pro')
root.geometry('720x520')
root.configure(bg = '#1e1e1e')

def password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c in LOWER for c in password):
        score += 1 
    if any(c in UPPER for c in password):
        score += 1
    if any(c in DIGITS for c in password):
        score += 1
    if any(c in SYMBOLS for c in password):
        score += 1
    if score <= 2:
        return 'Слабый'
    elif score <= 4:
        return 'Средний'
    return 'Сильный'
filtered_data = data.copy()
     

top_frame = tk.Frame(root, bg = '#2b2b2b', padx = 10, pady = 10)
top_frame.pack(fill = 'x')

tk.Label(top_frame, text="Сервис:", bg="#2b2b2b", fg="white").grid(row = 0, column = 0)
entry_service = tk.Entry(top_frame, width = 20)
entry_service.grid(row = 0, column = 1, padx = 5)

tk.Label(top_frame, text = "Логин:", bg = "#2b2b2b", fg = "white").grid(row = 0, column = 2)
entry_login = tk.Entry(top_frame, width = 20)
entry_login.grid(row = 0, column = 3, padx = 5)

tk.Label(top_frame, text = "Пароль:", bg = "#2b2b2b", fg = "white").grid(row = 0, column = 4)
entry_length = tk.Entry(top_frame, width = 5)
entry_length.insert(0, "12")
entry_length.grid(row = 0, column = 5)

tk.Button(top_frame, text = "Добавить", command = add_entry).grid(row = 0, column = 6 , padx = 10)

search_frame = tk.Frame(root, bg = "#1e1e1e")
search_frame.pack(fill = "x", pady = 5)

entry_search = tk.Entry(search_frame, width=40)
entry_search.pack(side = "left", padx = 10)

tk.Button(search_frame, text="Поиск", command=search).pack(side = "left")

listbox = tk.Listbox(
    root,
    width=90,
    height=18,
    bg="#111111",
    fg="white",
    selectbackground="#4444aa"
)
listbox.pack(pady = 10)

btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack()

tk.Button(btn_frame, text="Удалить", command = delete_entry).grid(row = 0, column = 0, padx = 10)
tk.Button(btn_frame, text="Скопировать логин", command = copy_login).grid(row = 0, column = 2, padx = 10)
tk.Button(btn_frame, text="Скопировать пароль", command = copy_password).grid(row = 0, column = 1, padx = 10)

refresh_list()
root.mainloop()

