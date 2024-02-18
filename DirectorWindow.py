from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal

from AddEmpWindow import AddEmpWindow
from AddTaskWindow import AddTaskWindow


class DirectorWindow(QMainWindow):
    logout_signal = Signal()
    def __init__(self, user_info):
        super().__init__()
        self.setWindowTitle("Panel dyrektora")
        self.setGeometry(400, 100, 800, 600)
        self.user_info = user_info

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(QLabel(f"Witaj {user_info['imie']}! Jesteś zalogowany jako dyrektor."))

        self.add_task_button = QPushButton("Dodaj nowe zadanie")
        self.add_task_button.clicked.connect(self.open_add_task_window)
        self.add_emp = QPushButton("Dodaj nowego managera")
        self.add_emp.clicked.connect(self.open_add_empl_window)

        self.logout_button = QPushButton("Wyloguj")
        self.logout_button.clicked.connect(self.logout)

        self.layout.addWidget(self.add_task_button)
        self.layout.addWidget(self.add_emp)
        self.layout.addWidget(self.logout_button)

    def open_add_task_window(self):
            # Otwórz nowe okno do dodawania zadania
        self.add_task_window = AddTaskWindow(self.user_info)
        self.add_task_window.show()

    def open_add_empl_window(self):
        self.add_emp_window = AddEmpWindow(self.user_info)
        self.add_emp_window.show()

    def logout(self):  # Dodane
        self.close()  # Zamknij bieżące okno
        self.logout_signal.emit()