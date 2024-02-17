from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QApplication, QFrame

class DayColumn(QWidget):
    def __init__(self, date):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.date_label = QLabel(date)
        self.date_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.date_label)
        self.setLayout(self.layout)
    def add_task(self, task_widget):
        self.layout.addWidget(task_widget)
