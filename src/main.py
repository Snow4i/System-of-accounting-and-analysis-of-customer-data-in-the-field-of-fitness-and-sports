import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

DB_FILE = "database.db"

# Данные для авторизации
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(conn, query, params=None):
    cur = conn.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    conn.commit()
    cur.close()

def create_tables():
    conn = get_db_connection()

    create_table_queries = [
        """
        CREATE TABLE IF NOT EXISTS Clients (
            Client_id INTEGER PRIMARY KEY,
            First_name VARCHAR(50),
            Last_name VARCHAR(50),
            Date_of_birth DATE,
            Gender VARCHAR(50),
            Phone_number VARCHAR(50),
            Email VARCHAR(50),
            Address VARCHAR(50),
            Membership_type VARCHAR(50),
            Membership_start_date DATE,
            Membership_end_date DATE,
            Subscription_status VARCHAR(50)
        );
        """
    ]

    for query in create_table_queries:
        execute_query(conn, query)

    conn.close()
    print("База данных успешно создана!")

class FitnessSystem(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Система учета и анализа данных о клиентах")
        self.geometry("500x300")
        self.resizable(False, False)

        # Меню
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Открыть базу данных", command=self.open_database)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.destroy)
        menu.add_cascade(label="Файл", menu=file_menu)

        client_menu = tk.Menu(menu, tearoff=0)
        client_menu.add_command(label="Добавить нового клиента", command=self.add_client)
        client_menu.add_command(label="Редактировать клиента", command=self.edit_client)
        client_menu.add_command(label="Удалить клиента", command=self.delete_client)
        menu.add_cascade(label="Клиенты", menu=client_menu)

        self.config(menu=menu)

        # Основной фрейм
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Приветственное сообщение
        welcome_label = tk.Label(main_frame, text="Добро пожаловать в систему учета клиентов!")
        welcome_label.pack(pady=20)

        # Кнопки для операций
        add_button = tk.Button(main_frame, text="Добавить нового клиента", command=self.add_client)
        add_button.pack(pady=5)

        edit_button = tk.Button(main_frame, text="Редактировать клиента", command=self.edit_client)
        edit_button.pack(pady=5)

        delete_button = tk.Button(main_frame, text="Удалить клиента", command=self.delete_client)
        delete_button.pack(pady=5)

    # Окно авторизации
    @staticmethod
    def show_login():
        login_window = tk.Tk()
        login_window.title("Авторизация")
        login_window.geometry("300x150")
        login_window.resizable(False, False)

        tk.Label(login_window, text="Логин:").pack(pady=5)
        entry_username = tk.Entry(login_window)
        entry_username.pack()

        tk.Label(login_window, text="Пароль:").pack(pady=5)
        entry_password = tk.Entry(login_window, show="*")
        entry_password.pack()

        def attempt_login():
            username = entry_username.get()
            password = entry_password.get()
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                login_window.destroy()
                app = FitnessSystem()
                app.mainloop()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль!")

        login_button = tk.Button(login_window, text="Войти", command=attempt_login)
        login_button.pack(pady=10)

        login_window.mainloop()

    def open_database(self):
        try:
            conn = get_db_connection()
            conn.close()
            messagebox.showinfo("Успех", "База данных успешно открыта!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть базу данных: {e}")

    def add_client(self):
        def save_client():
            first_name = entry_first_name.get().strip()
            last_name = entry_last_name.get().strip()
            dob = entry_dob.get().strip()
            gender = entry_gender.get().strip()
            phone_number = entry_phone_number.get().strip()
            email = entry_email.get().strip()
            address = entry_address.get().strip()
            membership_type = entry_membership_type.get().strip()
            membership_start_date = entry_membership_start_date.get().strip()
            membership_end_date = entry_membership_end_date.get().strip()
            subscription_status = entry_subscription_status.get().strip()

            if not first_name or not last_name:
                messagebox.showwarning("Предупреждение", "Пожалуйста, заполните имя и фамилию.")
                return

            try:
                conn = get_db_connection()
                query = """
                INSERT INTO Clients (
                    First_name, Last_name, Date_of_birth, Gender,
                    Phone_number, Email, Address, Membership_type,
                    Membership_start_date, Membership_end_date, Subscription_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """
                execute_query(conn, query, [
                    first_name, last_name, dob, gender, phone_number, email, address,
                    membership_type, membership_start_date, membership_end_date, subscription_status
                ])
                conn.close()
                messagebox.showinfo("Успех", "Клиент успешно добавлен!")
                top_level.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить клиента: {e}")

        top_level = tk.Toplevel(self)
        top_level.geometry("400x400")
        top_level.title("Добавить клиента")

        tk.Label(top_level, text="Имя").pack()
        entry_first_name = tk.Entry(top_level)
        entry_first_name.pack()

        tk.Label(top_level, text="Фамилия").pack()
        entry_last_name = tk.Entry(top_level)
        entry_last_name.pack()

        tk.Label(top_level, text="Дата рождения").pack()
        entry_dob = tk.Entry(top_level)
        entry_dob.pack()

        tk.Label(top_level, text="Пол").pack()
        entry_gender = tk.Entry(top_level)
        entry_gender.pack()

        tk.Label(top_level, text="Телефон").pack()
        entry_phone_number = tk.Entry(top_level)
        entry_phone_number.pack()

        tk.Label(top_level, text="Электронная почта").pack()
        entry_email = tk.Entry(top_level)
        entry_email.pack()

        tk.Label(top_level, text="Адрес").pack()
        entry_address = tk.Entry(top_level)
        entry_address.pack()

        tk.Label(top_level, text="Тип членства").pack()
        entry_membership_type = tk.Entry(top_level)
        entry_membership_type.pack()

        tk.Label(top_level, text="Дата начала членства").pack()
        entry_membership_start_date = tk.Entry(top_level)
        entry_membership_start_date.pack()

        tk.Label(top_level, text="Дата окончания членства").pack()
        entry_membership_end_date = tk.Entry(top_level)
        entry_membership_end_date.pack()

        tk.Label(top_level, text="Статус подписки").pack()
        entry_subscription_status = tk.Entry(top_level)
        entry_subscription_status.pack()

        save_button = tk.Button(top_level, text="Сохранить", command=save_client)
        save_button.pack(pady=10)
        
    def edit_client(self):
        client_id = simpledialog.askinteger("Редактировать клиента", "Введите ID клиента для редактирования:")
        if not client_id:
            return
        
        conn = get_db_connection()
        query = "SELECT * FROM Clients WHERE Client_id = ?;"
        cur = conn.cursor()
        cur.execute(query, (client_id,))
        client = cur.fetchone()
        conn.close()

        if not client:
            messagebox.showerror("Ошибка", "Клиент с таким ID не найден.") 
            return

        def save_changes():
            new_first_name = entry_first_name.get().strip()
            new_last_name = entry_last_name.get().strip()
            new_phone_number = entry_phone_number.get().strip()

            if not new_first_name or not new_last_name:
                messagebox.showwarning("Предупреждение", "Имя и фамилия обязательны.")
                return

            try:
                conn = get_db_connection()
                query = """
                    UPDATE Clients
                    SET First_name = ?, Last_name = ?, Phone_number = ?
                    WHERE Client_id = ?;
                """
                execute_query(conn, query, (new_first_name, new_last_name, new_phone_number, client_id))
                conn.close()
                messagebox.showinfo("Успех", "Данные клиента обновлены!")
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить клиента: {e}")

        edit_window = tk.Toplevel(self)
        edit_window.geometry("400x300")
        edit_window.title("Редактировать клиента")

        tk.Label(edit_window, text="Имя").pack()
        entry_first_name = tk.Entry(edit_window)
        entry_first_name.insert(0, client["First_name"])
        entry_first_name.pack()

        tk.Label(edit_window, text="Фамилия").pack()
        entry_last_name = tk.Entry(edit_window)
        entry_last_name.insert(0, client["Last_name"])
        entry_last_name.pack()

        tk.Label(edit_window, text="Телефон").pack()
        entry_phone_number = tk.Entry(edit_window)
        entry_phone_number.insert(0, client["Phone_number"])
        entry_phone_number.pack()

        save_button = tk.Button(edit_window, text="Сохранить изменения", command=save_changes)
        save_button.pack(pady=10)

    def delete_client(self):
        client_id = simpledialog.askinteger("Удалить клиента", "Введите ID клиента для удаления:")
        if not client_id:
            return

        try:
            conn = get_db_connection()
            query = "DELETE FROM Clients WHERE Client_id = ?;"
            execute_query(conn, query, (client_id,))
            conn.close()
            messagebox.showinfo("Успех", "Клиент удален!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить клиента: {e}")

if __name__ == "__main__":
    create_tables()
    FitnessSystem.show_login()