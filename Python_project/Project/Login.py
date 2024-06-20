from tkinter import *
from tkinter import messagebox as ns
import mysql.connector
import finance

class Main:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg='lightblue')  # Изменение цвета фона окна
        self.username = StringVar()
        self.password = StringVar()

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="5070",
            database="mydb"
        )
        self.cursor = self.db.cursor()

        self.head = Label(self.master, text='Авторизация', font=('Arial', 35, 'bold'), pady=20, bg='lightblue')
        self.head.pack()

        self.logf = Frame(self.master, padx=30, pady=20, bg='white', relief='raised', borderwidth=3)
        self.widgets()

    def widgets(self):
        Label(self.logf, text='Username:', font=('Arial', 20), pady=10, padx=10, bg='white').grid(sticky=W)
        Entry(self.logf, textvariable=self.username, bd=5, font=('Arial', 15)).grid(row=0, column=1)

        Label(self.logf, text='Password:', font=('Arial', 20), pady=10, padx=10, bg='white').grid(sticky=W)
        Entry(self.logf, textvariable=self.password, bd=5, font=('Arial', 15), show='*').grid(row=1, column=1)

        Button(self.logf, text='Login', bd=3, font=('Arial', 15), padx=10, pady=10, command=self.login).grid(row=2, column=0)
        Button(self.logf, text='Create Account', bd=3, font=('Arial', 15), padx=10, pady=10, command=self.new_user).grid(row=2, column=1)

        self.logf.pack()

    def login(self):
        username = self.username.get()
        password = self.password.get()

        self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = self.cursor.fetchone()

        if result:
            ns.showinfo("Успех", "Вы успешно авторизовались!")
            self.master.withdraw()
            self.finance_window = finance.FinanceTracker(self.master)
        else:
            ns.showerror("Ошибка", "Неверное имя пользователя или пароль.")

    def new_user(self):
        username = self.username.get()
        password = self.password.get()

        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            self.db.commit()
            ns.showinfo("Успех", "Пользователь успешно создан!")
        except mysql.connector.Error as err:
            ns.showerror("Ошибка", f"Произошла ошибка при создании пользователя: {err}")

    def del_db(self):
        self.db.close()

if __name__ == "__main__":
    try:
        root = Tk()
        root.title("Authentication System")
        app = Main(root)
        root.mainloop()
    except KeyboardInterrupt:
        app.del_db()
        print("Приложение отключено")
