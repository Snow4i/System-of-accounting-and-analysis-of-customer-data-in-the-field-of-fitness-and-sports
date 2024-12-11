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

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения
    close_db_connection(conn)
    print("База данных успешно создана!")

if __name__ == "__main__":
    create_tables()