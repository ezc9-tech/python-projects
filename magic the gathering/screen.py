import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QComboBox,
    QLabel, QFormLayout, QLineEdit, QPushButton, QVBoxLayout
)
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

URL = "https://cards.scryfall.io/border_crop/front/4/5/4520cdcc-a10f-4b39-9c6f-ba86f6aa2c87.jpg?1689998306"

# imageLabel = QLabel()
        # response = requests.get(URL).content
        # pixmap = QPixmap()
        # pixmap.loadFromData(response)
        # imageLabel.setPixmap(pixmap)

class Filters(QWidget):
    def __init__(self):
        super().__init__()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter card name...")

        self.color = QComboBox()
        self.color.addItems(["Any", "Red", "White", "Blue", "Green", "Black"])

        self.rarity = QComboBox()
        self.rarity.addItems(["Any", "Common", "Uncommon", "Rare", "Mythic Rare", "Special"])

        self.card_type = QComboBox()
        self.card_type.addItems(["Any", "Creature", "Planeswalker", "Enchantment", "Sorcery", "Instant", "Artifact", "Land"])

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)

        layout = QFormLayout()
        layout.addRow("Card Name:", self.name_input)
        layout.addRow("Color:", self.color)
        layout.addRow("Rarity:", self.rarity)
        layout.addRow("Type:", self.card_type)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(submit_button)

        self.setLayout(main_layout)

    def submit(self, text):
        print(self.name_input.text())
        print(self.color.currentText())
        print(self.rarity.currentText())
        print(self.card_type.currentText())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Widget Example")
        self.setGeometry(100, 100, 500, 100)
        self.custom_widget = Filters()
        self.setCentralWidget(self.custom_widget)

def apply_dark_mode(app):
    dark_palette = QPalette()

    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(142, 45, 197).lighter())
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)

    app.setPalette(dark_palette)


app = QApplication(sys.argv)
apply_dark_mode(app)
window = MainWindow()
window.show()

sys.exit(app.exec())