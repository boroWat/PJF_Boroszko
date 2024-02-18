from PySide6.QtCore import Qt, QTime, Signal
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout, QDialog, QFormLayout, QTimeEdit, \
    QComboBox, QTextEdit

from DataBaseHandler import DataBaseHandler


class TaskButton(QWidget):
    status_changed = Signal(str)
    def __init__(self,task_id, title, duration,status,workday,empID, parent=None):
        super().__init__(parent)
        self.empID = empID
        self.db_handler = DataBaseHandler()
        self.task_id = task_id
        self.work_day = workday
        self.status = status
        self.button = QPushButton(self)
        self.button.setStyleSheet("QPushButton { padding: 25px; }")
        self.button.clicked.connect(self.edit_task_dialog)

        content_layout = QHBoxLayout()
        if len(title) > 12:
            display_title = title[:12] + "..."
            self.setToolTip(title)
        else:
            display_title = title

        self.titleLabel = QLabel(display_title)
        self.titleLabel.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.titleLabel.setWordWrap(True)

        if duration is not None:
            hours, minutes = divmod(int(duration), 60)
            duration_formatted = f"{hours} h {minutes} min"
        else:
            duration_formatted = f"0 h 0 min"

        self.durationLabel = QLabel(duration_formatted)
        self.durationLabel.setStyleSheet("color: white;font-size: 12px;")
        self.durationLabel.setAlignment(Qt.AlignRight)

        content_layout.addWidget(self.titleLabel)
        content_layout.addWidget(self.durationLabel)

        self.button.setLayout(content_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.button)
        self.setLayout(main_layout)
        self.set_button_color()

    def set_button_color(self):
        if self.status == "Nowe":  # Nowe
            self.button.setStyleSheet(" QPushButton { padding: 25px;background-color: #8A2BE2; }") #BlueViolet
        elif self.status == "Odroczone":  # Odroczone
            self.button.setStyleSheet(" QPushButton { padding: 25px;background-color: #6495ED; }") #CornflowerBlue
        elif self.status == "Zakończone":  # Zakonczone
            self.button.setStyleSheet(" QPushButton { padding: 25px;background-color: #696969; }") #DimGray
        elif self.status == "W trakcie": # W trakcie
            self.button.setStyleSheet(" QPushButton { padding: 25px;background-color: #F08080; }") #LightCoral

    def edit_task_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edytuj Zadanie")

        # Tworzy layout formularza z polami czasu, wyboru statusu, i uwag
        form_layout = QFormLayout(dialog)

        # Pobieranie danych zadania z bazy danych

        task_data = self.db_handler.get_task_by_id(self.task_id)

        # Ustawianie etykiet z danymi zadania
        title_label = QLabel(f"<b>Tytuł: </b>{task_data['tytul']}")
        title_label.setStyleSheet("font-size: 15px;")

        description_label = QLabel(f"<b>Opis: </b> {task_data['opis']}")
        description_label.setStyleSheet("font-size: 14px;")

        piorytet_label = QLabel(f"<b>Piorytet: </b> {task_data['piorytet']}")
        piorytet_label.setStyleSheet("font-size: 14px;")

        comments_label = QLabel("<b>Uwagi:</b>")
        comments_edit = QTextEdit(dialog)
        comments_edit.setPlainText(task_data['uwagi'])

        # Dodawanie etykiet i pola uwag do layoutu
        form_layout.addRow(title_label)
        form_layout.addRow(description_label)
        form_layout.addRow(piorytet_label)
        form_layout.addRow(comments_label, comments_edit)

        # Dodanie pól wyboru czasu i statusu do layoutu
        dayData = self.db_handler.dayInfo(task_data['id'],self.work_day)
        print(dayData)
        start_time_default = QTime.fromString(dayData['zaczecie'], "hh:mm:ss")
        end_time_default = QTime.fromString(dayData['zakonczenie'], "hh:mm:ss")
        start_time_edit = QTimeEdit(start_time_default, dialog)
        end_time_edit = QTimeEdit(end_time_default, dialog)

        form_layout.addRow("<b>Czas rozpoczęcia:</b>", start_time_edit)
        form_layout.addRow("<b>Czas zakończenia:</b>", end_time_edit)

        status_combo = QComboBox(dialog)
        status_combo.addItems(["Nowe", "W trakcie", "Zakończone", "Odroczone"])
        status_combo.setCurrentText(task_data['status'])  # Ustawienie aktualnego statusu
        form_layout.addRow("<b>Status:</b>", status_combo)

        # Dodawanie przycisków do zapisu i anulowania
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Zapisz", dialog)
        cancel_button = QPushButton("Anuluj", dialog)


        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        form_layout.addRow(buttons_layout)

        # Łączenie przycisków z funkcjami
        save_button.clicked.connect(lambda: self.save_task_changes(
            start_time_edit.time(), end_time_edit.time(), status_combo.currentText(), comments_edit.toPlainText(),self.work_day,self.empID))
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(form_layout)
        dialog.setFixedSize(400, 300)
        dialog.exec()

    def save_task_changes(self, start_time, end_time, status,comments,work_day,empID):
        print(f"Czas rozpoczęcia: {start_time.toString()}, Czas zakończenia: {end_time.toString()}, Status: {status}")
        self.db_handler.update_task(self.task_id, start_time, end_time, status, comments,work_day,empID)
        self.status_changed.emit(status)
        dialog = self.findChild(QDialog)  # Znajdź okno dialogowe, którego dotyczy przycisk "Zapisz"
        if dialog:
            dialog.accept()  # Zamknij okno dialogowe z akceptacją zmian
