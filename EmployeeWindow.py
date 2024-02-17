import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame, \
    QHBoxLayout, QPushButton, QGridLayout, QSizePolicy

from DataBaseHandler import DataBaseHandler
from TaskButton import TaskButton


class EmployeeWindow(QMainWindow):
    def __init__(self, account_info):
        super().__init__()
        self.db_handler = DataBaseHandler()
        self.account_info = account_info
        self.current_week_start = datetime.datetime.now().date() - datetime.timedelta(
            days=datetime.datetime.now().weekday())

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Panel pracownika")
        self.setGeometry(400, 100, 800, 300)

        self.prev_week_button = QPushButton('<-', self)
        self.prev_week_button.clicked.connect(self.prev_week)
        self.next_week_button = QPushButton('->', self)
        self.next_week_button.clicked.connect(self.next_week)

        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        sunday = monday + datetime.timedelta(days=6)
        przepracowane_godziny = self.db_handler.sumaCzasuPracyWTygodniu(monday)
        h = int(przepracowane_godziny / 60)
        min = int(przepracowane_godziny % 60)
        self.week_label = QLabel(f"{monday.strftime('%Y-%m-%d')} - {sunday.strftime('%Y-%m-%d')}          {h} h {min} min /40h ")
        self.week_label.setAlignment(Qt.AlignCenter)

            # strzalki i tydzien
        navigation_layout = QHBoxLayout()
        #navigation_layout.setContentsMargins(0, 0, 0, 0)
        navigation_layout.addWidget(self.prev_week_button)
        navigation_layout.addStretch()
        navigation_layout.addWidget(self.week_label)
        navigation_layout.addStretch()
        navigation_layout.addWidget(self.next_week_button)

        weekdays_widget = QWidget()
        weekdays_layout = QGridLayout()

        weekdays_layout.setVerticalSpacing(0)
        weekdays_layout.setHorizontalSpacing(0)
        weekdays_layout.setContentsMargins(0, 0, 0, 0)

        weekdays_widget.setLayout(weekdays_layout)

     #dzien i nazwa
        self.week_labels = []
        for i, day in enumerate(['Pon', 'Wt', 'Śr', 'Czw', 'Pt']):
            czasPracyDzien = self.db_handler.czasPracyNaDzien(day)
            h = int(czasPracyDzien / 60)
            min = int(czasPracyDzien % 60)

            label_text = f"{day}  {(self.current_week_start + datetime.timedelta(days=i)).strftime('%Y-%m-%d')} \n {h} h {min} min / 8h"
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
            weekdays_layout.addWidget(label, 0, i * 2, 1, 1, Qt.AlignTop)
            self.week_labels.append(label)

            if i > 0:
                line = QFrame()
                line.setFrameShape(QFrame.VLine)
                line.setFrameShadow(QFrame.Sunken)
                weekdays_layout.addWidget(line, 0, i * 2 - 1, -1, 1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(navigation_layout) # strzalki i tydzien
        main_layout.addWidget(weekdays_widget) # kolumny

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.day_columns_layouts = []
        for i in range(5):
            day_layout = QVBoxLayout()
            weekdays_layout.addLayout(day_layout, 1, i * 2, Qt.AlignTop)
            weekdays_layout.setAlignment(Qt.AlignTop)
            self.day_columns_layouts.append(day_layout)

        self.display_weekly_tasks()

    def display_weekly_tasks(self):
        for day_layout in self.day_columns_layouts:
            for i in reversed(range(day_layout.count())):
                widget_to_remove = day_layout.itemAt(i).widget()
                day_layout.removeWidget(widget_to_remove)
                widget_to_remove.setParent(None)


        for i, day_layout in enumerate(self.day_columns_layouts):
            day_date = self.current_week_start + datetime.timedelta(days=i)
            tasks = self.db_handler.get_active_tasks_for_day(day_date, self.account_info['id'])

            for task in tasks:
                czasPracyDzien = self.db_handler.czasPracyNaDzienNaTask(day_date,task['id'])  # w minutach
                task_widget = TaskButton(
                                        task_id=task['id'],
                                        title=task['tytul'],
                                        duration=czasPracyDzien,
                                        status= task['status'],
                                        workday=day_date
                                        )
                task_widget.status_changed.connect(self.handle_status_change)  # Podłączanie sygnału

                day_layout.addWidget(task_widget)
        self.update_layouts()


    def prev_week(self):
        self.change_week(-1)
        self.clear_tasks()
        self.display_weekly_tasks()
    def update_layouts(self):
        for layout in self.day_columns_layouts:
            layout.update()
    def next_week(self):
        self.change_week(1)
        self.clear_tasks()
        self.display_weekly_tasks()
    def change_week(self, offset):
        self.weekdays = ['Pon', 'Wt', 'Śr', 'Czw', 'Pt']  # Definicja weekdays poza pętlą
        self.current_week_start += datetime.timedelta(weeks=offset)
        monday = self.current_week_start - datetime.timedelta(days=self.current_week_start.weekday())
        sunday = monday + datetime.timedelta(days=6)
        przepracowane_godziny = self.db_handler.sumaCzasuPracyWTygodniu(monday)
        h = int(przepracowane_godziny/60)
        min = int(przepracowane_godziny%60)
        week_text = f"{monday.strftime('%Y-%m-%d')} - {sunday.strftime('%Y-%m-%d')}         {h} h {min} min /40h "
        self.week_label.setText(week_text)

        for i, label in enumerate(self.week_labels):
            dzien = (monday + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            czasPracyDzien = self.db_handler.czasPracyNaDzien(dzien)
            h = int(czasPracyDzien/60)
            min = int(czasPracyDzien % 60)
            label_text = f"{self.weekdays[i]}  {dzien} \n {h} h {min} min / 8h"
            label.setText(label_text)

    def clear_tasks(self):
        for day_layout in self.day_columns_layouts:
            while day_layout.count():
                item = day_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

    def handle_status_change(self, status):  # Nowa metoda do obsługi zmiany statusu
        print("Status changed:", status)
        self.clear_tasks()  # Wyczyść zadania
        # Aktualizacja etykiety z godzinami przepracowanymi w tygodniu
        self.przepracowane_godziny = self.db_handler.sumaCzasuPracyWTygodniu(self.current_week_start)
        h, min = self.calculate_worked_hours_in_week()
        self.week_label.setText(
            f"{self.current_week_start} - {self.current_week_start + datetime.timedelta(days=6)} {h} h {min} min /40h")

        # Aktualizacja etykiety z godzinami przepracowanymi w dniu
        for i, label in enumerate(self.week_labels):
            dzien = (self.current_week_start + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            czasPracyDzien = self.db_handler.czasPracyNaDzien(dzien)
            h = int(czasPracyDzien / 60)
            min = int(czasPracyDzien % 60)
            label_text = f"{self.weekdays[i]}  {dzien} \n {h} h {min} min / 8h"
            label.setText(label_text)
        self.display_weekly_tasks()  # Wyświetl zadania ponownie

    def calculate_worked_hours_in_week(self):
        total_minutes = self.db_handler.sumaCzasuPracyWTygodniu(self.current_week_start)
        h, m = divmod(total_minutes, 60)
        return h, m