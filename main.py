import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QLabel, QPushButton, QLineEdit, QWidget, \
    QMessageBox

from DataBaseHandler import DataBaseHandler
from DirectorWindow import DirectorWindow
from EmployeeWindow import EmployeeWindow
from ManagerWindow import ManagerWindow


class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Logowanie")
        self.setGeometry(600, 200, 300, 200)
        self.dataBaseHandler = DataBaseHandler()
        self.layout = QVBoxLayout(self)
        self.setStyleSheet("""
                                   QPushButton {
                                       background-color: #4CAF50;
                                       border: none;
                                       color: white;
                                       padding: 3px 10px;
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
        self.username_label = QLabel("<b>Nazwa użytkownika:</b>")
        self.username_input = QLineEdit()
        self.password_label = QLabel("<b>Hasło:</b>")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # jako kropki tekst

        self.login_button = QPushButton("Zaloguj się")
        self.login_button.clicked.connect(self.login)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        authenticated = self.dataBaseHandler.authenticate_user(username, password)
        if authenticated:
            self.close()
            if authenticated['stanowisko'] == 'Pracownik':
                self.main_window = EmployeeWindow(authenticated)
                self.main_window.logout_signal.connect(self.show_login_window)
            elif authenticated['stanowisko'] == 'Manager':
                self.main_window = ManagerWindow(authenticated)
                self.main_window.logout_signal.connect(self.show_login_window)
            elif authenticated['stanowisko'] == 'Dyrektor':
                self.main_window = DirectorWindow(authenticated)
                self.main_window.logout_signal.connect(self.show_login_window)
            self.main_window.show()
        else:
            QMessageBox.warning(self, "Błąd logowania", "Nieprawidłowa nazwa użytkownika lub hasło")

    def show_login_window(self):
        # Wyświetlenie okna logowania po wylogowaniu
        self.main_window.close()
        self.username_input.clear()
        self.password_input.clear()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
