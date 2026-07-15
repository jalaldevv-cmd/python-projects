import requests
import csv

URL = "https://api.open-meteo.com/v1/forecast?latitude=14.5995&longitude=120.9842&current=temperature_2m,relative_humidity_2m,wind_speed_10m"


def get_json(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def extract_weather(weather):
    temp = weather["current"]["temperature_2m"]
    humidity = weather["current"]["relative_humidity_2m"]
    wind_speed = weather["current"]["wind_speed_10m"]

    return [temp, humidity, wind_speed]

def save_to_csv(weather_data):
    with open("weather.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Temperature", "Humidity", "Wind Speed"])
        writer.writerow(weather_data)

def main():
    print("Starting Weather API...")
    try:
        weather = get_json(URL)
    except requests.RequestException as e:
        print("Request Failed: ", e)
        return
        
    weather_data = extract_weather(weather)
    save_to_csv(weather_data)

    print("Weather saved successfully!")

if __name__ == "__main__":
    main()
