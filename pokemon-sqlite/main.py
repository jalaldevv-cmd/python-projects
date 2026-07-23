import sqlite3


def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokemon (
        name TEXT PRIMARY KEY,
        height INTEGER,
        weight INTEGER,
        base_experience INTEGER,
        first_ability TEXT)    
    """)


def insert_pokemon(cursor):
    pokemon_list = [
        ("Bulbasaur", 7, 69, 70, "Overgrow"),
        ("Pikachu", 4, 60, 90, "Static"),
        ("Charizard", 17, 900, 700, "Blaze"),
    ]

    for pokemon in pokemon_list:
        cursor.execute(
            """
        INSERT OR IGNORE INTO pokemon
        VALUES (?, ?, ?, ?, ?)
        """,
            pokemon,
        )


def display_pokemon(cursor):
    cursor.execute("""
    SELECT *
    FROM pokemon
    """)

    pokemon_all = cursor.fetchall()

    for pokemon in pokemon_all:
        print(pokemon)


def main():
    print("Pokemon Database")
    print("-" * 20)

    connection = sqlite3.connect("pokemon.db")
    cursor = connection.cursor()

    create_table(cursor)
    insert_pokemon(cursor)

    connection.commit()

    display_pokemon(cursor)

    connection.close()

    print("Database updated successfully!")


if __name__ == "__main__":
    main()
