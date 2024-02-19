from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from DataBaseHandler import DataBaseHandler


class AddEmpWindow(QDialog):
    def __init__(self, user_info):
        super().__init__()
        self.setWindowTitle("Dodaj nowego pracownika")
        layout = QVBoxLayout(self)
        self.user_info = user_info
        self.db_handler = DataBaseHandler()
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
        self.name_label = QLabel("<b>Imie:</b>")
        self.name_input = QLineEdit()
        self.surname_label = QLabel("<b>Nazwisko:</b>")
        self.surname_input = QLineEdit()
        self.login_label = QLabel("<b>Login:</b>")
        self.login_input = QLineEdit()
        self.haslo_label = QLabel("<b>Hasło:</b>")
        self.haslo_input = QLineEdit()

        self.add_button = QPushButton("Dodaj pracownika")
        self.add_button.clicked.connect(self.add_emp_to_db)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.surname_label)
        layout.addWidget(self.surname_input)
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.haslo_label)
        layout.addWidget(self.haslo_input)

        if self.user_info['stanowisko'] == 'Dyrektor':
            self.team_label = QLabel("Zespół:")
            self.team_input = QLineEdit()
            layout.addWidget(self.team_label)
            layout.addWidget(self.team_input)



        layout.addWidget(self.add_button)


    def add_emp_to_db(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        login = self.login_input.text()
        haslo = self.haslo_input.text()


        if not (name or surname or login or haslo):
            QMessageBox.warning(self, "Błąd", "Nie podano informacji.")
            return

        if self.user_info['stanowisko'] == 'Manager': #dodawanie pracownika
            jednostka = self.user_info['jednostka']
            team = self.user_info['zespol']
            stanowisko = "Pracownik"
        else: # dodawanie menago
            jednostka = self.user_info['jednostka']
            team = self.team_input.text()
            stanowisko = "Manager"


        self.db_handler.addEmp(name,surname,login,haslo,jednostka,team,stanowisko)
        self.close()