from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QInputDialog, QPushButton

from AddTaskWindow import AddTaskWindow


class ManagerWindow(QMainWindow):
    def __init__(self, user_info):
        super().__init__()
        self.setWindowTitle("Panel managera")
        self.setGeometry(400, 100, 800, 600)
        self.user_info = user_info
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(QLabel(f"Witaj {user_info['imie']}! Jesteś zalogowany jako manager."))

        self.add_task_button = QPushButton("Dodaj nowe zadanie")
        self.add_task_button.clicked.connect(self.open_add_task_window)
        self.layout.addWidget(self.add_task_button)

    def open_add_task_window(self):
        # Otwórz nowe okno do dodawania zadania
        self.add_task_window = AddTaskWindow(self.user_info)
        self.add_task_window.show()