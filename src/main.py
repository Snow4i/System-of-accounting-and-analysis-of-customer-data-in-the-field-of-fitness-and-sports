import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_FILE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def close_db_connection(conn):
    conn.close()

def execute_query(conn, query, params=None):
    cur = conn.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows

def insert_into_table(conn, table, columns, values):
    query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join(['?'] * len(values))})"
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    return cur.lastrowid

def update_table(conn, table, set_values, where_clause):
    query = f"UPDATE {table} SET {','.join([f'{key}=?' for key in set_values.keys()])} WHERE {where_clause}"
    cur = conn.cursor()
    cur.execute(query, list(set_values.values()))
    conn.commit()

def delete_from_table(conn, table, where_clause):
    query = f"DELETE FROM {table} WHERE {where_clause}"
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

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
        """,
        
        """
        CREATE TABLE IF NOT EXISTS Abonements (
            Abonement_id INTEGER PRIMARY KEY,
            Client_id INTEGER REFERENCES Clients(Client_id),
            Type VARCHAR(50),
            Start_date DATE,
            End_date DATE,
            Price FLOAT,
            Paid BOOLEAN,
            Frozen BOOLEAN,
            Frozen_until DATE
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS Sessions (
            Session_id INTEGER PRIMARY KEY,
            Name VARCHAR(50),
            Duration TIME,
            Date_of_session DATE,
            Instruktor_id INTEGER REFERENCES Trainers(Instruktor_id),
            Time_of_session TIME
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS Trainers (
            Instruktor_id INTEGER PRIMARY KEY,
            First_name VARCHAR(50),
            Last_name VARCHAR(50),
            Specialization VARCHAR(50),
            Experience_years INT,
            Rating FLOAT,
            Availability VARCHAR(50)
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS Attendances (
            Attendance_id INTEGER PRIMARY KEY,
            Session_id INTEGER REFERENCES Sessions(Session_id),
            Client_id INTEGER REFERENCES Clients(Client_id),
            Check_in_time DATETIME,
            Check_out_time DATETIME
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS Payments (
            Payment_id INTEGER PRIMARY KEY,
            Client_id INTEGER REFERENCES Clients(Client_id),
            Amount FLOAT,
            Payment_method TEXT CHECK(Payment_method IN ('Bank card', 'Electronic wallet')),
            Transaction_date DATE,
            Receipt_number FLOAT
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS Reports (
            Report_id INTEGER PRIMARY KEY,
            Report_type VARCHAR(50),
            Generation_date DATE,
            Data TEXT,
            User_id INTEGER REFERENCES SystemUsers(User_id)
        );
        """,
        
        """
        CREATE TABLE IF NOT EXISTS SystemUsers (
            User_id INTEGER PRIMARY KEY,
            Username VARCHAR(50),
            Password_hash VARCHAR(50),
            Role TEXT CHECK(Role IN ('Administrator', 'Manager', 'Trainer')),
            First_name VARCHAR(50),
            Last_name VARCHAR(50),
            Email VARCHAR(50)
        );
        """
    ]

    for query in create_table_queries:
        execute_query(conn, query)

    conn.commit()
    close_db_connection(conn)
    print("База данных успешно создана!")

class FitnessSystem(tk.Tk):
    def init(self):  # Fixed init method name
        super().init()

        self.title("Система учета и анализа данных о клиентах")
        self.geometry("800x600")
        self.resizable(False, False)

        # Menu setup
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Создать новую базу данных", command=self.create_new_database)
        file_menu.add_command(label="Открыть существующую базу данных", command=self.open_existing_database)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.destroy)
        menu.add_cascade(label="Файл", menu=file_menu)

        client_menu = tk.Menu(menu, tearoff=0)
        client_menu.add_command(label="Добавить нового клиента", command=self.add_client)
        client_menu.add_command(label="Редактировать данные клиента", command=self.edit_client)
        client_menu.add_command(label="Удалить клиента", command=self.delete_client)
        menu.add_cascade(label="Клиенты", menu=client_menu)

        session_menu = tk.Menu(menu, tearoff=0)
        session_menu.add_command(label="Добавить новое занятие", command=self.add_session)
        session_menu.add_command(label="Редактировать занятие", command=self.edit_session)
        session_menu.add_command(label="Удалить занятие", command=self.delete_session)
        menu.add_cascade(label="Занятия", menu=session_menu)

        report_menu = tk.Menu(menu, tearoff=0)
        report_menu.add_command(label="Посмотреть отчеты", command=self.view_reports)
        menu.add_cascade(label="Отчеты", menu=report_menu)

        self.config(menu=menu)

        # Main frame
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Welcome message
        welcome_label = tk.Label(main_frame, text="Добро пожаловать в систему учета клиентов!")
        welcome_label.pack(pady=20)

        # Text output area
        self.text_output = tk.Text(main_frame, width=80, height=30)
        self.text_output.pack(padx=10, pady=10)

        # Buttons
        add_button = tk.Button(main_frame, text="Добавить нового клиента", command=self.add_client)
        add_button.pack(pady=10)

        view_report_button = tk.Button(main_frame, text="Просмотр отчетов", command=self.view_reports)
        view_report_button.pack(pady=10)

    def create_new_database(self):
        try:
            create_tables()
            messagebox.showinfo("Успех", "Новая база данных успешно создана.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при создании новой базы данных: {e}")

    def open_existing_database(self):
        try:
            conn = get_db_connection()
            clients = execute_query(conn, "SELECT * FROM Clients")

            self.text_output.delete('1.0', tk.END)
            for client in clients:
                self.text_output.insert(tk.END, f"{client['Client_id']} | {client['First_name']} {client['Last_name']}\n")

            close_db_connection(conn)
            messagebox.showinfo("Успех", "База данных открыта. Список клиентов отображен ниже.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при открытии базы данных: {e}")

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

            if not all((first_name, last_name)):
                messagebox.showwarning("Предупреждение", "Пожалуйста, введите имя и фамилию.")
                return

            try:
                conn = get_db_connection()
                insert_into_table(
                    conn,
                    "Clients",
                    ["First_name", "Last_name", "Date_of_birth", "Gender", "Phone_number", "Email", "Address", "Membership_type", "Membership_start_date", "Membership_end_date", "Subscription_status"],
                    [first_name, last_name, dob, gender, phone_number, email, address, membership_type, membership_start_date, membership_end_date, subscription_status]
                )
                close_db_connection(conn)
                messagebox.showinfo("Успех", "Новый клиент был успешно добавлен.")
                top_level.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка при добавлении клиента: {e}")

        top_level = tk.Toplevel(self)
        top_level.geometry("400x400")

        # Create labels and entries for each field
        tk.Label(top_level, text="Имя:").pack(pady=5)
        entry_first_name = tk.Entry(top_level)
        entry_first_name.pack(pady=5)

        tk.Label(top_level, text="Фамилия:").pack(pady=5)
        entry_last_name = tk.Entry(top_level)
        entry_last_name.pack(pady=5)

        tk.Label(top_level, text="Дата рождения (YYYY-MM-DD):").pack(pady=5)
        entry_dob = tk.Entry(top_level)
        entry_dob.pack(pady=5)

        tk.Label(top_level, text="Пол:").pack(pady=5)
        entry_gender = tk.Entry(top_level)
        entry_gender.pack(pady=5)

        tk.Label(top_level, text="Телефон:").pack(pady=5)
        entry_phone_number = tk.Entry(top_level)
        entry_phone_number.pack(pady=5)

        tk.Label(top_level, text="Email:").pack(pady=5)
        entry_email = tk.Entry(top_level)
        entry_email.pack(pady=5)

        tk.Label(top_level, text="Адрес:").pack(pady=5)
        entry_address = tk.Entry(top_level)
        entry_address.pack(pady=5)

        tk.Label(top_level, text="Тип членства:").pack(pady=5)
        entry_membership_type = tk.Entry(top_level)
        entry_membership_type.pack(pady=5)

        tk.Label(top_level, text="Дата начала членства (YYYY-MM-DD):").pack(pady=5)
        entry_membership_start_date = tk.Entry(top_level)
        entry_membership_start_date.pack(pady=5)

        tk.Label(top_level, text="Дата окончания членства (YYYY-MM-DD):").pack(pady=5)
        entry_membership_end_date = tk.Entry(top_level)
        entry_membership_end_date.pack(pady=5)

        tk.Label(top_level, text="Статус подписки:").pack(pady=5)
        entry_subscription_status = tk.Entry(top_level)
        entry_subscription_status.pack(pady=5)

        # Save button
        save_button = tk.Button(top_level, text="Сохранить", command=save_client)
        save_button.pack(pady=20)
        # Main execution
if __name__ == "__main__":
    create_tables()  # Ensure tables are created before running the app
    app = FitnessSystem()
    app.mainloop()
