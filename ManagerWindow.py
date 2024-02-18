from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QInputDialog, QPushButton, QHBoxLayout, \
    QTableWidgetItem, QTableWidget, QTextEdit
from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PySide6.QtWidgets import QWidget, QVBoxLayout
import matplotlib.pyplot as plt
from AddEmpWindow import AddEmpWindow
from AddTaskWindow import AddTaskWindow
from DataBaseHandler import DataBaseHandler



class ManagerWindow(QMainWindow):
    logout_signal = Signal()

    def __init__(self, user_info):
        super().__init__()
        self.setWindowTitle("Panel managera")
        self.setGeometry(400, 100, 950, 600)
        self.user_info = user_info
        self.table = None
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.buttons_layout)

        self.add_buttons()

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        headers = ["Imię", "Nazwisko", "Status", "Priorytet", "Tytuł", "Opis", "Uwagi", "Data Dodania",
                   "Deadline"]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.hide()
        self.layout.addWidget(self.table)

        self.stats_widget = QWidget()
        self.stats_layout = QVBoxLayout(self.stats_widget)
        self.stats_layout.setSpacing(0)

        self.layout.addWidget(self.stats_widget)
        self.chart_figure = Figure()
        self.chart_canvas = FigureCanvas(self.chart_figure)
        self.layout.addWidget(self.chart_canvas)
        self.add_task_button = QPushButton("Dodaj nowe zadanie")
        self.add_task_button.clicked.connect(self.open_add_task_window)

        self.add_emp_button = QPushButton("Dodaj nowego pracownika")
        self.add_emp_button.clicked.connect(self.open_add_empl_window)

        self.logout_button = QPushButton("Wyloguj")
        self.logout_button.clicked.connect(self.logout)

        self.layout.addWidget(self.add_task_button)
        self.layout.addWidget(self.add_emp_button)
        self.layout.addWidget(self.logout_button)

        # Inicjalizacja bazy danych
        self.db_handler = DataBaseHandler()

        self.tabela()

    def add_buttons(self):
        # Dodanie przycisków do layoutu
        button_texts = ["Czas pracy", "Statusy", "Tabela"]
        for text in button_texts:
            button = QPushButton(text)
            button.clicked.connect(self.show_stats)
            self.buttons_layout.addWidget(button)

    def show_stats(self):
        button = self.sender()
        stats_text = ""
        self.clear_stats_widget()
        if button.text() == "Czas pracy" or button.text() == "Statusy":
            # Ukryj tabelę jeśli istnieje i pokaż wykres
            if self.table is not None:
                self.table.hide()
                self.chart_canvas.show()

        if button.text() == "Czas pracy":
            # Pobranie pracowników z zespołu
            employees = self.db_handler.get_employees(self.user_info['stanowisko'], self.user_info['zespol'])
            if employees:
                # Obliczenie średniego czasu pracy dziennego dla każdego pracownika
                average_daily_work_time_per_employee = []
                for employee in employees:
                    emp_id = employee['id']
                    avg_daily_work_time = self.db_handler.average_daily_work_time(emp_id,self.user_info['zespol'])

                    #print(avg_daily_work_time)

                    average_daily_work_time_per_employee.append((employee['imie'], avg_daily_work_time))

                # Obliczenie średniego czasu pracy dziennego dla całego zespołu
                avg_daily_work_time_team = self.db_handler.average_daily_work_time_team(self.user_info['zespol'])

                average_daily_work_time_per_employee.append(("Zespół", avg_daily_work_time_team))
                # Przygotowanie danych do wykresu słupkowego
                names = [str(emp[0]) for emp in average_daily_work_time_per_employee]
                times = [emp[1] for emp in average_daily_work_time_per_employee]

                # Stworzenie wykresu słupkowego
                self.chart_figure.clear()
                ax = self.chart_figure.add_subplot(111)  # Add subplot to existing figure
                ax.bar(names, times)
                ax.set_ylabel('Czas pracy (minuty)')
                ax.set_title(f'Średni czas pracy dzienny pracowników w zespole "{self.user_info["zespol"]}"')

                # Wyświetl wykres w oknie podręcznym
                self.chart_canvas.draw()

                stats_text += f"Średni czas pracy dzienny pracowników w zespole '{self.user_info['zespol']}':\n"
                for emp, avg_time in average_daily_work_time_per_employee:
                    hours = int(avg_time // 60)
                    minutes = int(avg_time % 60)
                    stats_text += f"{emp}: {hours} h {minutes} min\n"

            else:
                stats_text = "Brak pracowników w zespole."

        elif button.text() == "Statusy":
            # Pobierz dane do wykresu
            self.chart_figure.clear()

            tasks_status_dict = self.db_handler.tasks_by_status(self.user_info['zespol'])
            allTask = self.db_handler.allTask(self.user_info['zespol'])
            labels = list(tasks_status_dict.keys())
            counts = list(tasks_status_dict.values())

            # Wygeneruj wykres kołowy
            ax = self.chart_figure.add_subplot(111)
            ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Ustawienie wykresu na okrąg
            ax.set_title('Procentowy udział zadań w poszczególnych statusach')

            self.chart_canvas.draw()
            stats_text += f"Zadania:\n"
            for task_id, task_details in allTask.items():
                title = task_details['tytul']
                status = task_details['status']
                stats_text += f"Tytuł: {title}, Status: {status}\n"

        elif button.text() == "Tabela":
            self.tabela()

        # Wyświetlenie statystyk
        stats_label = QLabel(stats_text)
        self.stats_layout.addWidget(stats_label)

    def clear_stats_widget(self):
        # Usunięcie wszystkich elementów z widżetu statystyk
        for i in reversed(range(self.stats_layout.count())):
            self.stats_layout.itemAt(i).widget().setParent(None)

    def tabela(self):
        self.chart_canvas.hide()  # Ukryj wykres
        self.table.show()
        self.clear_stats_widget()

        all_tasks = self.db_handler.allTask(self.user_info['zespol'])
        num_rows = len(all_tasks)
        self.table.setRowCount(num_rows)  # Ustaw liczbę wierszy

        for row, (task_id, task_details) in enumerate(all_tasks.items()):
            employee_id = task_details['osobaID']
            status = task_details['status']
            priority = task_details['piorytet']
            title = task_details['tytul']
            description = task_details['opis']
            notes = task_details['uwagi']
            date_added = str(task_details['dataDodania'])
            deadline = str(task_details['deadLine'])
            employee_details = self.db_handler.get_employee_details(employee_id)
            employee_name = employee_details['imie']
            employee_surname = employee_details['nazwisko']

            self.table.setItem(row, 0, QTableWidgetItem(employee_name))
            self.table.setItem(row, 1, QTableWidgetItem(employee_surname))
            self.table.setItem(row, 2, QTableWidgetItem(status))
            self.table.setItem(row, 3, QTableWidgetItem(priority))
            self.table.setItem(row, 4, QTableWidgetItem(title))
            self.table.setItem(row, 5, QTableWidgetItem(description))
            self.table.setItem(row, 6, QTableWidgetItem(notes))
            self.table.setItem(row, 7, QTableWidgetItem(date_added))
            self.table.setItem(row, 8, QTableWidgetItem(deadline))
    def open_add_task_window(self):
        self.add_task_window = AddTaskWindow(self.user_info)
        self.add_task_window.show()

    def open_add_empl_window(self):
        self.add_emp_window = AddEmpWindow(self.user_info)
        self.add_emp_window.show()

    def logout(self):
        self.close()
        self.logout_signal.emit()

