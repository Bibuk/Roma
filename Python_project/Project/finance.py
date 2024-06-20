import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox as tk_messagebox
from PIL import Image, ImageTk
import mysql.connector

class FinanceTracker(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Учет личных финансов")
        self.geometry("800x500")
        self.configure(bg='light blue')
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="5070",
            database="mydb"
        )
        self.c = self.conn.cursor()
        self.child_window = None
        self.create_main_window()

    def create_main_window(self):
        self.tree = ttk.Treeview(self, columns=("description", "category", "amount"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("description", text="Наименование")
        self.tree.heading("category", text="Статья дохода/расхода")
        self.tree.heading("amount", text="Сумма")
        self.tree.pack(fill="both", expand=True)
        frame_buttons = tk.Frame(self, bg='light blue')
        frame_buttons.pack(side=tk.TOP, fill=tk.X)
        self.btn_add = self.create_button("add.png", "Добавить", frame_buttons, 0, 0, self.show_child_window)
        self.btn_edit = self.create_button("update.png", "Редактировать", frame_buttons, 0, 1, self.edit_record)
        self.btn_delete = self.create_button("delete.png", "Удалить", frame_buttons, 0, 2, self.delete_record)
        self.btn_search = self.create_button("search.png", "Поиск", frame_buttons, 0, 3, self.show_search_window)
        self.btn_refresh = self.create_button("refresh.png", "Обновить", frame_buttons, 0, 4, self.view_records)
        self.view_records()

    def show_child_window(self):
        if self.child_window:
            self.child_window.destroy()
        self.child_window = ChildWindow(self, self.c)

    def edit_record(self):
        selected = self.tree.selection()
        if selected:
            self.child_window = UpdateChild(self, self.c, selected[0])

    def delete_record(self):
        selected = self.tree.selection()
        if selected:
            if tk_messagebox.askyesno("Удаление", "Вы уверены, что хотите удалить эту запись?"):
                self.c.execute("DELETE FROM transactions WHERE id = %s", (int(selected[0]),))
                self.conn.commit()
                self.tree.delete(selected[0])

    def show_search_window(self):
        search_id = simpledialog.askstring("Поиск", "Введите ID для поиска:")
        if search_id:
            self.search_records(search_id)

    def view_records(self):
        self.c.execute("SELECT * FROM transactions")
        records = self.c.fetchall()
        self.tree.delete(*self.tree.get_children())
        for record in records:
            self.tree.insert("", "end", str(record[0]), text=str(record[0]), values=(record[1], record[2], record[3]))

    def add_record(self, description, category, amount):
        self.c.execute("INSERT INTO transactions (description, category, amount) VALUES (%s, %s, %s)", (description, category, amount))
        self.conn.commit()
        self.view_records()

    def edit_existing_record(self, index, description, amount):
        self.c.execute("UPDATE transactions SET description = %s, amount = %s WHERE id = %s", (description, amount, index))
        self.conn.commit()
        self.view_records()

    def search_records(self, search_id):
        self.c.execute("SELECT * FROM transactions WHERE id = %s", (search_id,))
        records = self.c.fetchall()
        self.tree.delete(*self.tree.get_children())
        for record in records:
            self.tree.insert("", "end", str(record[0]), text=str(record[0]), values=(record[1], record[2], record[3]))

    def del_db(self):
        self.conn.close()

    def create_button(self, image_filename, text, frame, row, column, command):
        img = Image.open(image_filename)
        img = img.resize((20, 20), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        button = tk.Button(frame, image=img, text=text, compound=tk.LEFT, command=command)
        button.image = img
        button.grid(row=row, column=column, padx=10, pady=10)
        return button

class ChildWindow(tk.Toplevel):
    def __init__(self, master, cursor):
        super().__init__(master)
        self.configure(bg='light grey')
        self.cursor = cursor
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Наименование:", bg='light grey').grid(row=0, column=0, padx=10, pady=10)
        self.entry_description = tk.Entry(self)
        self.entry_description.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self, text="Статья дохода/расхода:", bg='light grey').grid(row=1, column=0, padx=10, pady=10)
        self.entry_category = tk.Entry(self)
        self.entry_category.grid(row=1, column=1, padx=10, pady=10)
        tk.Label(self, text="Сумма:", bg='light grey').grid(row=2, column=0, padx=10, pady=10)
        self.entry_amount = tk.Entry(self)
        self.entry_amount.grid(row=2, column=1, padx=10, pady=10)
        self.btn_save = tk.Button(self, text="Сохранить", bg='light grey', command=self.save_record)
        self.btn_save.grid(row=3, column=1, padx=10, pady=10)
class ChildWindow(tk.Toplevel):
    def __init__(self, master, cursor):
        super().__init__(master)
        self.c = cursor
        self.title("Новая транзакция")
        self.geometry("400x200")
        self.description = tk.StringVar()
        self.category = tk.StringVar()
        self.amount = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Наименование:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.description).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self, text="Статья дохода/расхода:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.category).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(self, text="Сумма:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.amount).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(self, text="Сохранить", command=self.save_record).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(self, text="Отмена", command=self.destroy).grid(row=3, column=1, padx=10, pady=10)

    def save_record(self):
        description = self.description.get()
        category = self.category.get()
        amount = self.amount.get()
        if amount:
            amount = float(amount)
        self.master.add_record(description, category, amount)
        self.destroy()

class UpdateChild(tk.Toplevel):
    def __init__(self, master, cursor, selected_id):
        super().__init__(master)
        self.c = cursor
        self.selected_id = selected_id
        self.title("Редактировать транзакцию")
        self.geometry("400x200")
        self.description = tk.StringVar()
        self.amount = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.c.execute("SELECT description, amount FROM transactions WHERE id = %s", (self.selected_id,))
        result = self.c.fetchone()
        self.description.set(result[0])
        self.amount.set(result[1])
        tk.Label(self, text="Наименование:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.description).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self, text="Сумма:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.amount).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self, text="Сохранить", command=self.update_record).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(self, text="Отмена", command=self.destroy).grid(row=2, column=1, padx=10, pady=10)

    def update_record(self):
        description = self.description.get()
        amount = self.amount.get()
        if amount:
            amount = float(amount)
        self.master.edit_existing_record(self.selected_id, description, amount)
        self.destroy()

def main():
    root = tk.Tk()
    app = FinanceTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
