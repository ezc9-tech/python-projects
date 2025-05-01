import requests

def card_lookup(name):
    URL = f"https://api.scryfall.com/cards/named?"
    paramaters = {'exact':name}
    data = requests.get(URL, paramaters).json()
    print(name)
    print(f"Colors: {data["colors"][0]}")
    print(f"Rarity: {data["rarity"]}")
    print(f"Type: {data["type_line"]}")
    print(f"Skill: {data["oracle_text"]}")
    print(f"Power/Toughness: {data["power"]}/{data["toughness"]}")

card_lookup("Zada, Hedron Grinder")