import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame, \
    QHBoxLayout, QPushButton, QApplication, QGridLayout

from DataBaseHandler import DataBaseHandler
from TaskButton import TaskButton


class EmployeeWindow(QMainWindow):
    def __init__(self, account_info):
        super().__init__()

        self.account_info = account_info
        self.current_week_start = datetime.datetime.now().date() - datetime.timedelta(
            days=datetime.datetime.now().weekday())

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Panel pracownika")
        self.setGeometry(400, 100, 800, 600)

        self.prev_week_button = QPushButton('<-', self)
        self.prev_week_button.clicked.connect(self.prev_week)

        self.next_week_button = QPushButton('->', self)
        self.next_week_button.clicked.connect(self.next_week)

        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        sunday = monday + datetime.timedelta(days=6)

        self.week_label = QLabel(f"{monday.strftime('%Y-%m-%d')} - {sunday.strftime('%Y-%m-%d')}")
        self.week_label.setAlignment(Qt.AlignCenter)

        navigation_layout = QHBoxLayout()
        navigation_layout.addWidget(self.prev_week_button)
        navigation_layout.addStretch()
        navigation_layout.addWidget(self.week_label)
        navigation_layout.addStretch()
        navigation_layout.addWidget(self.next_week_button)

        weekdays_widget = QWidget()
        weekdays_layout = QGridLayout()  # Use QGridLayout for arranging labels and lines
        weekdays_widget.setLayout(weekdays_layout)

        weekdays_layout.setVerticalSpacing(0)
        weekdays_layout.setContentsMargins(0, 0, 0, 0)

        self.week_labels = []
        for i, day in enumerate(['Pon', 'Wt', 'Śr', 'Czw', 'Pt']):
            label_text = f"{day}\n{(self.current_week_start + datetime.timedelta(days=i)).strftime('%Y-%m-%d')}"
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter | Qt.AlignTop)  # Align to center and top
            weekdays_layout.addWidget(label, 0, i * 2, 1, 1, Qt.AlignTop)  # Align to top within the grid cell
            self.week_labels.append(label)

            if i > 0:
                vline = QFrame()
                vline.setFrameShape(QFrame.VLine)
                vline.setFrameShadow(QFrame.Sunken)
                weekdays_layout.addWidget(vline, 0, i * 2 - 1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(navigation_layout)
        main_layout.addWidget(weekdays_widget)


        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.day_columns_layouts = []
        for i in range(5):
            day_layout = QVBoxLayout()
            day_layout.setAlignment(Qt.AlignTop)
            weekdays_layout.addLayout(day_layout, 2, i * 2)  # Add the layout below the date labels
            self.day_columns_layouts.append(day_layout)

        self.display_weekly_tasks()

    def display_weekly_tasks(self):
        for day_layout in self.day_columns_layouts:
            for i in reversed(range(day_layout.count())):
                widget_to_remove = day_layout.itemAt(i).widget()
                day_layout.removeWidget(widget_to_remove)
                widget_to_remove.setParent(None)

        db_handler = DataBaseHandler()
        for i, day_layout in enumerate(self.day_columns_layouts):
            day_date = self.current_week_start + datetime.timedelta(days=i)
            tasks = db_handler.get_active_tasks_for_day(day_date, self.account_info['id'])
            print(tasks)
            for task in tasks:
                duration_str = str(task['czas'])
                task_widget = TaskButton(title=task['tytul'],
                                         description=task['opis'],
                                         duration=duration_str)
                day_layout.addWidget(task_widget)
        self.update_layouts()


    def add_task_to_day(self, day_index, task_name, duration):
        task_widget = TaskButton(task_name, duration)
        self.day_columns[day_index].add_task(task_widget)
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
        weekdays = ['Pon', 'Wt', 'Śr', 'Czw', 'Pt']  # Definicja weekdays poza pętlą
        self.current_week_start += datetime.timedelta(weeks=offset)
        monday = self.current_week_start - datetime.timedelta(days=self.current_week_start.weekday())
        sunday = monday + datetime.timedelta(days=6)
        week_text = f"{monday.strftime('%Y-%m-%d')} - {sunday.strftime('%Y-%m-%d')}"
        self.week_label.setText(week_text)

        for i, label in enumerate(self.week_labels):
            label_text = f"{weekdays[i]}\n{(monday + datetime.timedelta(days=i)).strftime('%Y-%m-%d')}"
            label.setText(label_text)

    def clear_tasks(self):
        for day_layout in self.day_columns_layouts:
            while day_layout.count():
                item = day_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()