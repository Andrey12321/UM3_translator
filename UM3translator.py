import tkinter as tk
from tkinter import filedialog
from functools import partial
from PascalToUM3 import main

def save_text():
    text = text_entry.get("1.0", "end-1c")
    with open("in_file.txt", "w") as file:
        file.write(text)

def run_main_func():
    save_text()
    main("in_file.txt", "out_file.txt")
    with open("out_file.txt", "r") as file:
        result_text = file.read()
        result_entry.delete("1.0", "end")
        result_entry.insert("1.0", result_text)

# Создание главного окна
root = tk.Tk()
root.title("Графический интерфейс")

# Создание левой части интерфейса для ввода текста
text_entry = tk.Text(root, height=30, width=60)
text_entry.grid(row=0, column=0, padx=5, pady=5)

# Создание кнопки "ТРАНСЛИРОВАТЬ"
run_button = tk.Button(root, text="ТРАНСЛИРОВАТЬ", command=run_main_func)
run_button.grid(row=0, column=1, padx=5, pady=5)

# Создание правой части интерфейса для вывода результата
result_entry = tk.Text(root, height=30, width=60)
result_entry.grid(row=0, column=2, padx=5, pady=5)

root.mainloop()