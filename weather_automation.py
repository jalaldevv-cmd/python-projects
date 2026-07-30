import requests
import sqlite3
from datetime import datetime

URL = "https://api.open-meteo.com/v1/forecast?latitude=14.5995&longitude=120.9842&current=temperature_2m,relative_humidity_2m"


def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather (   
        id INTEGER PRIMARY KEY,
        date TEXT,
        city TEXT,
        temperature REAL,
        humidity INTEGER
    )
    """)


def get_weather(url):
    response = requests.get(url)
    response.raise_for_status()
    weather = response.json()

    date = datetime.now().strftime("%Y-%m-%d")
    city = "Manila"
    temperature = weather["current"]["temperature_2m"]
    humidity = weather["current"]["relative_humidity_2m"]

    weather_data = (date, city, temperature, humidity)
    return weather_data


def save_weather(cursor, weather_data):
    cursor.execute(
        """
    INSERT INTO weather (date, city, temperature, humidity)
    VALUES (?, ?, ?, ?)""",
        weather_data,
    )


def display_weather(cursor):
    print("Weather Logger")
    print("-" * 20)

    cursor.execute("""
    SELECT *
    FROM weather
    """)

    weathers = cursor.fetchall()

    for weather in weathers:
        print(weather)


def main():
    connection = sqlite3.connect("weather_logger.db")
    cursor = connection.cursor()

    create_table(cursor)
    weather_data = get_weather(URL)
    save_weather(cursor, weather_data)
    connection.commit()
    display_weather(cursor)
    connection.close()


if __name__ == "__main__":
    main()
