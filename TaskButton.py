from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget


class TaskButton(QWidget):
    def __init__(self, title, description, duration, parent=None):
        super().__init__(parent)

        # Main button that covers the whole TaskButton
        self.button = QPushButton(self)
        self.button.setStyleSheet("QPushButton { text-align: left; padding: 10px; }")
        self.button.clicked.connect(self.on_click)

        # Layout for the content inside the button
        content_layout = QVBoxLayout()

        # Title label
        self.titleLabel = QLabel(title)
        self.titleLabel.setStyleSheet("font-weight: bold;")

        # Description label
        self.descriptionLabel = QLabel(description)

        # Duration label
        self.durationLabel = QLabel(duration)
        self.durationLabel.setStyleSheet("color: green;")

        # Add widgets to the content layout
        content_layout.addWidget(self.titleLabel)
        content_layout.addWidget(self.descriptionLabel)
        content_layout.addWidget(self.durationLabel)

        # Set the content layout to the button
        self.button.setLayout(content_layout)

        # Main layout of the TaskButton widget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.button)
        self.setLayout(main_layout)

    def on_click(self):
        print("Button clicked! Perform an action here.")
