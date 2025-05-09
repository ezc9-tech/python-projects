import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QComboBox,
    QLabel, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QCheckBox)
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
import requests
from rich.console import Console
from rich.table import Table


URL = f"https://api.scryfall.com/cards/search?"

# URL = "https://cards.scryfall.io/border_crop/front/4/5/4520cdcc-a10f-4b39-9c6f-ba86f6aa2c87.jpg?1689998306"

# imageLabel = QLabel()
        # response = requests.get(URL).content
        # pixmap = QPixmap()
        # pixmap.loadFromData(response)
        # imageLabel.setPixmap(pixmap)

class Filters(QWidget):
    def __init__(self):
        super().__init__()

        #This allows the user to enter their name using the Line Edit element (text box)
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("color: white;")
        self.name_input.setPlaceholderText("Enter card name...")

        #This allows the user to enter in the ability of the card they would like
        self.ability_input = QLineEdit()
        self.ability_input.setStyleSheet("color: white;")
        self.ability_input.setPlaceholderText("Enter the ability of the card (ex. draw a card)")

        #This allows the user to enter in the mana value of the card they would like
        self.mana_input = QLineEdit()
        self.mana_input.setStyleSheet("color: white;")
        self.mana_input.setPlaceholderText("Enter the amount of mana the card costs")

        #This is the full setup for a checkbox allowing the user to select which colors of card they will see
        self.color_checkboxes = {}
        color_layout = QHBoxLayout()
        colors = ["red", "white", "blue", "green", "black", "colorless"]

        #This go's through the colors in the colors list and creates a checkbox for them
        #The checkboxes get added to our layout which is the checkbox list itself
        #The checkbox also gets added to the color_checkboxes dict in order to associate it with its color
        for color in colors:
            checkbox = QCheckBox(color)
            self.color_checkboxes[color] = checkbox
            color_layout.addWidget(checkbox)

        #This is a combo box (dropdown menu) for the rarity of the card
        self.rarity = QComboBox()
        self.rarity.addItems(["Any", "Common", "Uncommon", "Rare", "Mythic Rare", "Special"])

        #This is a combo box (dropdown menu) for the type of the card
        self.card_type = QComboBox()
        self.card_type.addItems(["Any", "Creature", "Planeswalker", "Enchantment", "Sorcery", "Instant", "Artifact", "Land"])

        #This is a submit button that when pushed activates the submit function
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)

        #This creates a form layout allowing all of these widgets to be stacked on top of each other with captions
        layout = QFormLayout()
        layout.addRow("Card Name:", self.name_input)
        layout.addRow("Color:", color_layout)
        layout.addRow("Mana Cost:", self.mana_input)
        layout.addRow("Rarity:", self.rarity)
        layout.addRow("Type:", self.card_type)
        layout.addRow("Ability:", self.ability_input)

        #This creates the main layout which is a vertical layout it adds the 
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(submit_button)

        #This just makes the widgets layout the main layout
        self.setLayout(main_layout)

    #This prints the query for the get request the options selected or typed by the user
    def submit(self):
        question = ""
        if self.name_input.text() != "":
            question += f"name={self.name_input.text()} "

        color_map = {"white": "w", "blue": "u", "black": "b", "red": "r", "green": "g", "colorless": "c"}
        selected_colors = [color_map[color] for color, checkbox in self.color_checkboxes.items() if checkbox.isChecked()]
        if selected_colors != []:
            question += f"c={selected_colors} "

        if self.mana_input.text() != "":
            question += f"cmc={self.mana_input.text()} "

        if self.rarity.currentText() != "Any":
            question += f"rarity={self.rarity.currentText()} "

        if self.card_type.currentText() != "Any":
            question += f"type={self.card_type.currentText()} "

        if self.ability_input.text() != "":
            question += f"oracle={self.ability_input.text()} "
        
        parameters = {"q": question}
        response = requests.get(url=URL, params=parameters).json()
        console = Console()
        count = 0

        for card in response["data"]:
            count += 1
            console.print(f"\n[bold green]Card {count}: {card['name']}[/bold green]")

            table = Table(title=f"Information about {card['name']}")
            table.add_column("Field", justify="left", style="cyan", no_wrap=True)
            table.add_column("Value", justify="left", style="magenta")

            # Safely add each field, using .get() to avoid KeyError
            table.add_row("Name", card.get("name", "N/A"))

            colors = card.get("colors", [])
            table.add_row("Colors", ", ".join(colors) if colors else "Colorless")

            table.add_row("Rarity", card.get("rarity", "N/A"))
            table.add_row("Type", card.get("type_line", "N/A"))
            table.add_row("Skill", card.get("oracle_text", "N/A"))

            if "power" in card and "toughness" in card:
                table.add_row("Power/Toughness", f"{card['power']}/{card['toughness']}")

            image_url = card.get("image_uris", {}).get("border_crop")
            if image_url:
                table.add_row("Image", image_url)

            console.print(table)

        

#This simply creates a main window allowing our widget to be viewed
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Widget Example")
        self.setGeometry(100, 100, 500, 100)
        self.custom_widget = Filters()
        self.setCentralWidget(self.custom_widget)

#This is simply a function that allows for a dark mode
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

#This is just the main program actually running
app = QApplication(sys.argv)
apply_dark_mode(app)
window = MainWindow()
window.show()
sys.exit(app.exec())