import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QComboBox,
    QLabel, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QCheckBox, QScrollArea)
from PyQt6.QtGui import QPalette, QColor, QPixmap
from PyQt6.QtCore import Qt
import requests
from io import BytesIO

# This is the url you would use to search for cards with the scryfall api
URL = f"https://api.scryfall.com/cards/search?"

class Filters(QWidget):
    def __init__(self):
        super().__init__()

        # This allows the user to enter their name using the Line Edit element (text box)
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("color: white;")
        self.name_input.setPlaceholderText("Enter card name...")

        # This allows the user to enter in the ability of the card they would like
        self.ability_input = QLineEdit()
        self.ability_input.setStyleSheet("color: white;")
        self.ability_input.setPlaceholderText("Enter the ability of the card (ex. draw a card)")

        # This allows the user to enter in the mana value of the card they would like
        self.mana_input = QLineEdit()
        self.mana_input.setStyleSheet("color: white;")
        self.mana_input.setPlaceholderText("Enter the amount of mana the card costs")

        # This is the full setup for a checkbox allowing the user to select which colors of card they will see
        self.color_checkboxes = {}
        color_layout = QHBoxLayout()
        colors = ["red", "white", "blue", "green", "black", "colorless"]

        # This go's through the colors in the colors list and creates a checkbox for them
        # The checkboxes get added to our layout which is the checkbox list itself
        # The checkbox also gets added to the color_checkboxes dict in order to associate it with its color
        for color in colors:
            checkbox = QCheckBox(color)
            self.color_checkboxes[color] = checkbox
            color_layout.addWidget(checkbox)

        # This is a combo box (dropdown menu) for the rarity of the card
        self.rarity = QComboBox()
        self.rarity.addItems(["Any", "Common", "Uncommon", "Rare", "Mythic Rare", "Special"])

        # This is a combo box (dropdown menu) for the type of the card
        self.card_type = QComboBox()
        self.card_type.addItems(["Any", "Creature", "Planeswalker", "Enchantment", "Sorcery", "Instant", "Artifact", "Land"])

        # This is a submit button that when pushed activates the submit function
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)

        # This creates a form layout allowing all of these widgets to be stacked on top of each other with captions
        layout = QFormLayout()
        layout.addRow("Card Name:", self.name_input)
        layout.addRow("Color:", color_layout)
        layout.addRow("Mana Cost:", self.mana_input)
        layout.addRow("Rarity:", self.rarity)
        layout.addRow("Type:", self.card_type)
        layout.addRow("Ability:", self.ability_input)

        # This creates the main layout which is a vertical layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(submit_button)

        # This creates a scrollable area in the gui that allows the cards to be displayed
        self.results_area = QScrollArea()
        self.results_widget = QWidget()

        # This makes it a vertical layout
        self.results_layout = QVBoxLayout()

        # These just make sure that the widget has a layout and that it is resizable
        self.results_widget.setLayout(self.results_layout)
        self.results_area.setWidget(self.results_widget)
        self.results_area.setWidgetResizable(True)

        # Lastly add the widget to the main layout
        main_layout.addWidget(self.results_area)

        # This just makes the widgets layout the main layout
        self.setLayout(main_layout)

    # This will go through and display all the cards based on their uri
    def displayCard(self, card):

        # First we will create the widget and give it a horizontal layout
        card_widget = QWidget()
        layout = QVBoxLayout()

        # Then we will create a label so that we can display the image of the card
        image_label = QLabel()

        # Grab the uri for the image
        image_url = card.get("image_uris", {}).get("border_crop")

        # If it exists
        if image_url:

            # Try to get the image content and put it into a pixmap which will display the data 
            try:
                img_data = requests.get(image_url).content
                pixmap = QPixmap()
                pixmap.loadFromData(img_data)
                image_label.setPixmap(pixmap.scaled(223, 310, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

            # If that fails then just display that it failed to load the image
            except Exception as e:
                image_label.setText("Image failed to load.")
        
        # If there is no image found then display that
        else:
            image_label.setText("No image was found")

        # Create the widget with all of the card information
        info_layout = QVBoxLayout()
        name = QLabel(f"<b>{card.get('name', 'Unknown')}</b>")
        colors = ", ".join(card.get("colors", [])) or "Colorless"
        rarity = card.get("rarity", "N/A")
        ctype = card.get("type_line", "N/A")
        oracle = card.get("oracle_text", "N/A")
        pt = f"{card.get('power', '')}/{card.get('toughness', '')}" if "power" in card and "toughness" in card else ""

        info_layout.addWidget(name)
        for text in [f"Colors: {colors}", f"Rarity: {rarity}", f"Type: {ctype}", f"Ability: {oracle}", f"Power/Toughness: {pt}"]:
            info_layout.addWidget(QLabel(text))

        layout.addWidget(image_label)
        layout.addLayout(info_layout)
        card_widget.setLayout(layout)
        self.results_layout.addWidget(card_widget)
        
    # This prints the query for the get request using the options selected or typed by the user
    def submit(self):

        # ✅ Clear previous results before making a new query
        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # This is the query for the get request ultimately it will go into the parameters
        question = ""

        # If the name_input isn't empty then add it to the question
        if self.name_input.text() != "":
            question += f'name:"{self.name_input.text()}" '

        # Go through the color map and make a dictionary so that we can have the input in the correct format
        color_map = {"white": "w", "blue": "u", "black": "b", "red": "r", "green": "g", "colorless": "c"}

        # Create a selected colors list that gets the proper annotation for the colors selected by the user
        selected_colors = [color_map[color] for color, checkbox in self.color_checkboxes.items() if checkbox.isChecked()]

        # ✅ Correct formatting of color query
        if selected_colors:
            question += f"c:{''.join(selected_colors)} "

        # If the mana input is not empty add it to the question
        if self.mana_input.text() != "":
            question += f"cmc={self.mana_input.text()} "

        # If the rarity input is not "Any" add it to the question
        if self.rarity.currentText() != "Any":
            question += f"rarity:{self.rarity.currentText().lower()} "

        # If the card type input is not "Any" add it to the question
        if self.card_type.currentText() != "Any":
            question += f"type:{self.card_type.currentText().lower()} "

        # If the ability input is not empty add it to the question
        if self.ability_input.text() != "":
            question += f'oracle:"{self.ability_input.text()}" '

        # This makes parameters with our query as 'q' due to that being what the API needs for a response
        parameters = {"q": question}

        # Then we make a get request to the API making sure to pass the parameters and putting the response in JSON form
        try:
            response = requests.get(url=URL, params=parameters)
            response.raise_for_status()
            data = response.json()
        
        except Exception as e:
            error_label = QLabel(f"Error: {str(e)}")
            self.results_layout.addWidget(error_label)
            return

        # Display the first 20 cards returned from the API
        for card in data.get("data", [])[:20]:
            self.displayCard(card)        

# This simply creates a main window allowing our widget to be viewed
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Widget Example")
        self.setGeometry(100, 100, 500, 100)
        self.custom_widget = Filters()
        self.setCentralWidget(self.custom_widget)

# This is simply a function that allows for a dark mode
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

# This is just the main program actually running
app = QApplication(sys.argv)
apply_dark_mode(app)
window = MainWindow()
window.show()
sys.exit(app.exec())
