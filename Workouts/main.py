import os
import openai
from dotenv import load_dotenv
import requests
from datetime import datetime as dt

load_dotenv()

NUT_KEY = os.getenv("NUTRITION_KEY")
NUT_ID = os.getenv("NUTRITION_ID")
OPEN_AI = os.getenv("OPENAI_KEY")
USERNAME = os.getenv("SHEETY_KEY")
TOKEN = os.getenv("TOKEN")
PROJECT_NAME = "myWorkouts"
SHEET_NAME = "workouts"

weight = float(input("How much do you weigh?: "))
height = float(input("How tall are you?: "))
age = int(input("How old are you?: "))
lifts = input("What exercises have you done?: ")


headers = {
    "x-app-id": NUT_ID,
    "x-app-key": NUT_KEY,
    # "x-remote-user-id": 0,
}

data = {
    "query": lifts,
    "gender": "male",
    "weight_kg":weight,
    "height_cm":height,
    "age": age
}

bearer_headers = {
    "Authorization": TOKEN
}

NUTRITION_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = f"https://api.sheety.co/{USERNAME}/{PROJECT_NAME}/{SHEET_NAME}"

response = requests.post(url=NUTRITION_ENDPOINT, json=data, headers=headers)
exercises = response.json()["exercises"]

date = dt.now().strftime("%d%m%Y")
now_time = dt.now().strftime("%X")

for i in exercises:
    sheet_inputs = {
       "workout": {
           "date": date,
           "time": now_time,
           "exercise": i['name'].title(),
           "duration": i['duration_min'],
           "calories": i['nf_calories']
        }
    }

    end = requests.post(url=SHEETY_ENDPOINT, json=sheet_inputs, headers=bearer_headers)
    print(end.text)