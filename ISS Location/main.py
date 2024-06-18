import requests
import os
from dotenv import load_dotenv
from datetime import datetime as dt
import smtplib
import time

load_dotenv()

MY_LAT = -1.292066
MY_LNG = 36.821945

EMAIL = os.getenv('MY_EMAIL')
PASS = os.getenv('PASS')

def is_overhead():
    iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss.raise_for_status()

    data = iss.json()
    longitude = float(data["iss_position"]['longitude'])
    latitude = float(data["iss_position"]['latitude'])
    location = (longitude, latitude)
    if MY_LAT - 5 <= latitude <= MY_LAT + 5 and MY_LAT - 5 <= longitude <= MY_LAT + 5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]['sunrise'].split('T')[1].split(":")[0])
    sunset = int(data["results"]['sunset'].split('T')[1].split(":")[0])

    time_now = dt.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_night() and is_overhead():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASS)
            connection.sendmail(from_addr=EMAIL, to_addrs="murigipeninah1@gmail.com", msg="Subject: ISS APPROACHING!!!\n\nThe ISS is up there. Check it out")
