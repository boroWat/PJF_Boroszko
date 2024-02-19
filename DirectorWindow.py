from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget, \
    QTableWidgetItem
from PySide6.QtCore import Signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from AddEmpWindow import AddEmpWindow
from AddTaskWindow import AddTaskWindow
from DataBaseHandler import DataBaseHandler


class DirectorWindow(QMainWindow):
    logout_signal = Signal()
    def __init__(self, user_info):
        super().__init__()
        self.db_handler = DataBaseHandler()
        self.setWindowTitle("Panel dyrektora")
        self.setGeometry(200, 100, 1150, 600)
        self.user_info = user_info
        self.table = None
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet("""
                            QPushButton {
                                background-color: #4CAF50;
                                border: none;
                                color: white;
                                padding: 3px 18px;
                                text-align: center;
                                text-decoration: none;
                                font-size: 14px;
                                margin: 4px 2px;
                                cursor: pointer;
                                border-radius: 8px;
                            }

                            QPushButton:hover {
                                background-color: #45a049;
                            }

                            QPushButton:pressed {
                                background-color: #3e8e41;
                            }
                        """)
        self.layout = QVBoxLayout(self.central_widget)
        self.upperButtons_layout = QHBoxLayout()
        self.add_task_button = QPushButton("Dodaj nowe zadanie")
        self.add_task_button.clicked.connect(self.open_add_task_window)
        self.upperButtons_layout.addWidget(self.add_task_button)

        self.add_emp_button = QPushButton("Dodaj nowego managera")
        self.add_emp_button.clicked.connect(self.open_add_empl_window)
        self.upperButtons_layout.addWidget(self.add_emp_button)

        self.logout_button = QPushButton("Wyloguj")
        self.logout_button.clicked.connect(self.logout)
        self.upperButtons_layout.addWidget(self.logout_button)

        self.layout.addLayout(self.upperButtons_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(11)
        headers = ["Imię", "Nazwisko", "Stanowisko", "Zespół", "Status", "Priorytet", "Tytuł", "Opis", "Uwagi", "Data Dodania",
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

        self.buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.buttons_layout)
        self.add_buttons()

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
            teams = self.db_handler.get_teams( self.user_info['jednostka'])
            print(teams)
            if teams:
                # Obliczenie średniego czasu pracy dziennego dla każdego pracownika
                average_daily_work_time = []
                for team in teams:
                    avg_daily_work_time = self.db_handler.average_daily_work_time_team(team)  # nazwa

                    average_daily_work_time.append((team, avg_daily_work_time))

                # Przygotowanie danych do wykresu słupkowego
                names = [str(emp[0]) for emp in average_daily_work_time]
                times = [emp[1] for emp in average_daily_work_time]

                # Stworzenie wykresu słupkowego
                self.chart_figure.clear()
                ax = self.chart_figure.add_subplot(111)  # Add subplot to existing figure
                ax.bar(names, times)
                ax.set_ylabel('Czas pracy (minuty)')
                ax.set_title(f'Średni czas pracy dzienny zespołów w jednosce "{self.user_info["jednostka"]}"')

                # Wyświetl wykres w oknie podręcznym
                self.chart_canvas.draw()

                stats_text += f"<b><big>Średni czas pracy dzienny zespołów w jednosce '{self.user_info['jednostka']}':</big><b/>"
                for emp, avg_time in average_daily_work_time:
                    hours = int(avg_time // 60)
                    minutes = int(avg_time % 60)
                    stats_text += f"<br>{emp}: {hours} h {minutes} min"

            else:
                stats_text = "Brak pracowników w zespole."

        elif button.text() == "Statusy":
            # Pobierz dane do wykresu
            self.chart_figure.clear()

            tasks_status_dict = self.db_handler.tasks_by_statusDyr()
            allTask = self.db_handler.allTaskDyr()
            labels = list(tasks_status_dict.keys())
            counts = list(tasks_status_dict.values())

            # Wygeneruj wykres kołowy
            ax = self.chart_figure.add_subplot(111)
            ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Ustawienie wykresu na okrąg
            ax.set_title('Procentowy udział wszystkich zadań w poszczególnych statusach')

            self.chart_canvas.draw()
            stats_text += "<b><big>Zadania:</big></b>"
            for task_id, task_details in allTask.items():
                title = task_details['tytul']
                status = task_details['status']
                stats_text += f"<br><b>Tytuł: {title}, Status: {status}</b>"  # Dodanie pogrubienia

        elif button.text() == "Tabela":
            self.tabela()

        # Wyświetlenie statystyk
        stats_label = QLabel(stats_text)
        self.stats_layout.addWidget(stats_label)
    def tabela(self):
        self.chart_canvas.hide()  # Ukryj wykres
        self.table.show()
        self.clear_stats_widget()

        all_tasks = self.db_handler.allTaskDyr()
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
            employee_stanowisko = employee_details['stanowisko']
            employee_zespol = employee_details['zespol']

            self.table.setItem(row, 0, QTableWidgetItem(employee_name))
            self.table.setItem(row, 1, QTableWidgetItem(employee_surname))
            self.table.setItem(row, 2, QTableWidgetItem(employee_stanowisko))
            self.table.setItem(row, 3, QTableWidgetItem(employee_zespol))
            self.table.setItem(row, 4, QTableWidgetItem(status))
            self.table.setItem(row, 5, QTableWidgetItem(priority))
            self.table.setItem(row, 6, QTableWidgetItem(title))
            self.table.setItem(row, 7, QTableWidgetItem(description))
            self.table.setItem(row, 8, QTableWidgetItem(notes))
            self.table.setItem(row, 9, QTableWidgetItem(date_added))
            self.table.setItem(row, 10, QTableWidgetItem(deadline))

    def open_add_task_window(self):
            # Otwórz nowe okno do dodawania zadania
        self.add_task_window = AddTaskWindow(self.user_info)
        self.add_task_window.show()
    def clear_stats_widget(self):
        # Usunięcie wszystkich elementów z widżetu statystyk
        for i in reversed(range(self.stats_layout.count())):
            self.stats_layout.itemAt(i).widget().setParent(None)
    def open_add_empl_window(self):
        self.add_emp_window = AddEmpWindow(self.user_info)
        self.add_emp_window.show()

    def logout(self):  # Dodane
        self.close()  # Zamknij bieżące okno
        self.logout_signal.emit()