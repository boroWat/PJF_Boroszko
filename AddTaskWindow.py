from datetime import datetime

from PySide6.QtCore import QDate, QTime, QDateTime
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, \
    QCalendarWidget, QTimeEdit, QMessageBox

from DataBaseHandler import DataBaseHandler


class AddTaskWindow(QDialog):
    def __init__(self,user_info):
        super().__init__()
        self.setWindowTitle("Dodaj nowe zadanie")
        layout = QVBoxLayout(self)
        self.user_info =user_info
        print(user_info)
        self.employee_combo_box = QComboBox()
        layout.addWidget(QLabel("Wybierz pracownika:"))
        layout.addWidget(self.employee_combo_box)
        self.dataBaseHandler = DataBaseHandler()
        employees = self.dataBaseHandler.get_employees()
        for emp in employees:
            self.employee_combo_box.addItem(f"{emp['imie']} {emp['nazwisko']}", emp['id'])

        self.title_label = QLabel("Tytuł:")
        self.title_input = QLineEdit()

        self.description_label = QLabel("Opis:")
        self.description_input = QLineEdit()

        self.comments_label = QLabel("Uwagi:")
        self.comments_input = QLineEdit()

        self.deadline_label = QLabel("Termin wykonania:")
        self.deadline_input = QCalendarWidget()
        self.deadline_input.setSelectedDate(QDate.currentDate())

        self.deadlinetime_label = QLabel("Godzina wykonania:")
        self.deadlinetime_input = QTimeEdit()
        self.deadlinetime_input.setTime(QTime.currentTime())

        self.priority_label = QLabel("Priorytet:")
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Niski", "Średni", "Wysoki"])

        self.status_label = QLabel("Status:")
        self.status_input = QComboBox()
        self.status_input.addItems(["Nowe", "W trakcie", "Zakończone"])

        self.add_button = QPushButton("Dodaj zadanie")
        self.add_button.clicked.connect(self.add_task_to_db)

        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)
        layout.addWidget(self.comments_label)
        layout.addWidget(self.comments_input)
        layout.addWidget(self.deadline_label)
        layout.addWidget(self.deadline_input)
        layout.addWidget(self.deadlinetime_label)
        layout.addWidget(self.deadlinetime_input)
        layout.addWidget(self.priority_label)
        layout.addWidget(self.priority_input)
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_input)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_task_to_db(self):
        title = self.title_input.text()
        description = self.description_input.text()
        comments = self.comments_input.text()
        deadline_date = self.deadline_input.selectedDate().toString("yyyy-MM-dd")
        deadline_time = self.deadlinetime_input.time().toString("HH:mm")
        priority = self.priority_input.currentText()
        status = self.status_input.currentText()

        if not title:
            QMessageBox.warning(self, "Błąd", "Tytuł zadania jest wymagany.")
            return

        employee_id = self.employee_combo_box.currentData()
        deadline_datetime = QDateTime.fromString(deadline_date + " " + deadline_time, "yyyy-MM-dd HH:mm").toPython()
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Dodaj zadanie do bazy danych
        db_handler = DataBaseHandler()
        db_handler.add_task(employee_id, self.user_info['id'], status, priority, title, description, comments,
                            current_datetime, deadline_datetime)
        QMessageBox.information(self, "Sukces", "Zadanie zostało dodane do bazy danych.")
        self.close()
