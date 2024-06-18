import os
import requests
from dotenv import load_dotenv

load_dotenv()

SHEETY_KEY = os.getenv("SHEETY_KEY")
SHEETY_TOKEN = os.getenv("TOKEN")

PROJECT_NAME = "flightDeals"
SHEET_NAME = "prices"

bearer_headers = {
    "Authorization": SHEETY_TOKEN
}

SHEETY_URL = f"https://api.sheety.co/{SHEETY_KEY}/{PROJECT_NAME}/{SHEET_NAME}"

class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_URL).json()['prices']
        self.destination_data = response
        return self.destination_data

    def update_data(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_URL}/{city['id']}",json=new_data)
            print(response.text)
