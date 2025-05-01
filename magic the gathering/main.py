import requests
from PIL import Image
from io import BytesIO
from rich.console import Console
from rich.table import Table


#This allows you to see information about the card if you look it up by name
def card_lookup(name):
    URL = f"https://api.scryfall.com/cards/named?"
    paramaters = {'exact':name}
    data = requests.get(URL, paramaters).json()

    table = Table(title=f"Information about {name}")
    
    table.add_column("Field", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", justify="left", style="magenta")

    table.add_row("Name", name)
    table.add_row("Colors", data["colors"][0])
    table.add_row("Rarity", data["rarity"])
    table.add_row("Type", data["type_line"])
    table.add_row("Skill", data["oracle_text"])
    table.add_row("Power/Toughness", f"{data["power"]}/{data["toughness"]}")
    table.add_row("Image", data["image_uris"]["border_crop"])

    console = Console()
    console.print(table)

    # You can do this if you wanted to currently see the image
    # picture = requests.get(data["image_uris"]["border_crop"], stream=True)
    # image = Image.open(BytesIO(picture.content))
    # image.show()


    #This will allow you to find cards based on certain factors like mana cost etc.
    def find_cards():
        pass

def main():
    print("Welcome to the Magic the Gathering Card Finder")
    print("\tBy Zane Chapman")
    running = True
    while(running):
        card = input("Enter the card you would like to learn about (Leave blank to close program): ")
        if card != "":
            try:
                card_lookup(card)
            except:
                print("The card was not found, make sure you spelled it correctly.")
        else:
            print("Thank you for using, goodbye!")
            running = False




if __name__ == "__main__":
    main()
