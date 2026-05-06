import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")

        # Данные для генерации
        self.history = []
        self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # Ползунок длины пароля
        ttk.Label(self.root, text="Длина пароля:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.length_scale = ttk.Scale(self.root, from_=4, to=32, orient="horizontal")
        self.length_scale.set(12)
        self.length_scale.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.length_label = ttk.Label(self.root, text="12")
        self.length_label.grid(row=0, column=2, padx=10, pady=5)

        # Чекбоксы для символов
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)

        ttk.Checkbutton(self.root, text="Цифры (0-9)", variable=self.use_digits).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Checkbutton(self.root, text="Буквы (a-z, A-Z)", variable=self.use_letters).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ttk.Checkbutton(self.root, text="Спецсимволы (!@#$%&*)", variable=self.use_special).grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Кнопка генерации
        self.generate_btn = ttk.Button(self.root, text="Сгенерировать пароль", command=self.generate_password)
        self.generate_btn.grid(row=4, column=0, columnspan=3, pady=15)

        # Поле вывода пароля
        ttk.Label(self.root, text="Сгенерированный пароль:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = ttk.Entry(self.root, width=40, font=("Courier", 10))
        self.password_entry.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        # Таблица истории
        ttk.Label(self.root, text="История паролей:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        columns = ("ID", "Пароль", "Длина", "Символы", "Дата")
        self.history_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        self.history_tree.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        # Прокрутка для таблицы
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.history_tree.yview)
        scrollbar.grid(row=7, column=3, sticky="ns")
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        # Обновление метки длины при движении ползунка
        self.length_scale.config(command=self.update_length_label)

        # Растягивание элементов
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(7, weight=1)

    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))

    def generate_password(self):
        length = int(self.length_scale.get())
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля — 4 символа.")
            return
        if length > 32:
            messagebox.showerror("Ошибка", "Максимальная длина пароля — 32 символа.")
            return

        chars = ""
        if self.use_digits.get():
            chars += "0123456789"
        if self.use_letters.get():
            chars += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.use_special.get():
            chars += "!@#$%&*"

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов.")
            return

        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        # Добавление в историю
        used_chars = ""
        if self.use_digits.get(): used_chars += "Цифры "
        if self.use_letters.get(): used_chars += "Буквы "
        if self.use_special.get(): used_chars += "Спецсимволы"

        record = {
            "id": len(self.history) + 1,
            "password": password,
            "length": length,
            "characters": used_chars.strip(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(record)
        self.save_history()
        self.update_history_table()

    def update_history_table(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        for record in self.history:
            self.history_tree.insert("", "end", values=(
                record["id"], record["password"], record["length"],
                record["characters"], record["timestamp"]
            ))

    def load_history(self):
        if os.path.exists("password_history.json"):
            try:
                with open("password_history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.history = []

    def save_history(self):
        try:
            with open("password_history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=4, ensure_ascii=False)
        except IOError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
