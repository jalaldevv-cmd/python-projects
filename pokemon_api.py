import requests
import csv

URL = "https://pokeapi.co/api/v2/pokemon/"


def get_json(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def extract_pokemon(pokemon):
    name = pokemon["name"]
    height = pokemon["height"]
    weight = pokemon["weight"]
    base_exp = pokemon["base_experience"]
    first_ability = pokemon["abilities"][0]["ability"]["name"]
    return [name, height, weight, base_exp, first_ability]


def save_to_csv(pokemon_info):
    with open("pokemon.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Height", "Weight", "Base Exp", "First Ability"])
        writer.writerow(pokemon_info)


def main():
    print("Starting Pokemon API...")
    pokemon_name = input("Which Pokemon?").strip().lower()
    url = URL + pokemon_name

    try:
        pokemon = get_json(url)
    except requests.RequestException as e:
        print(f"Could not find Pokemon '{pokemon_name}'.")
        print("Request Failed: ", e)
        return

    pokemon_info = extract_pokemon(pokemon)
    save_to_csv(pokemon_info)

    print(f"{pokemon_info[0]} saved successfully!")


if __name__ == "__main__":
    main()
