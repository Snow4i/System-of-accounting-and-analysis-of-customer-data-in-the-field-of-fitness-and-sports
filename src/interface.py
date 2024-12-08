import tkinter as tk

class FitnessSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Система учета и анализа данных о клиентах")
        self.geometry("500x300")  # Размер окна
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
        client_menu.add_command(label="Редактировать данные клиента", command=self.edit_client)
        client_menu.add_command(label="Удалить клиента", command=self.delete_client)
        menu.add_cascade(label="Клиенты", menu=client_menu)
        
        report_menu = tk.Menu(menu, tearoff=0)
        report_menu.add_command(label="Посмотреть отчеты", command=self.view_reports)
        menu.add_cascade(label="Отчеты", menu=report_menu)
        
        self.config(menu=menu)
        
        # Основной фрейм
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Приветственное сообщение
        welcome_label = tk.Label(main_frame, text="Добро пожаловать в систему учета клиентов!")
        welcome_label.pack(pady=20)
        
        # Кнопка для добавления нового клиента
        add_button = tk.Button(main_frame, text="Добавить нового клиента", command=self.add_client)
        add_button.pack(pady=10)
        
        # Кнопка для просмотра отчетов
        view_report_button = tk.Button(main_frame, text="Просмотр отчетов", command=self.view_reports)
        view_report_button.pack(pady=10)
    
    def open_database(self):
        print("Открытие базы данных...")
    
    def add_client(self):
        print("Добавление нового клиента...")
    
    def edit_client(self):
        print("Редактирование данных клиента...")
    
    def delete_client(self):
        print("Удаление клиента...")
    
    def view_reports(self):
        print("Просмотр отчетов...")

if __name__ == "__main__":
    app = FitnessSystem()
    app.mainloop()