from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel


class DirectorWindow(QWidget):
    def __init__(self, user_info):
        super().__init__()
        self.setWindowTitle("Panel dyrektora")
        self.setGeometry(400, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(QLabel(f"Witaj {user_info['imie']}! Jesteś zalogowany jako dyrektor."))
