import requests
from datetime import datetime
import os

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["SHEET_ENDPOINT"]


GENDER = "male"
AGE = 25
HEIGHT = 187.96
WEIGHT = 70

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

bearer_headers = {
    "Authorization": f"Bearer {os.environ['TOKEN']}"
}

type_of_exercise = input("What exercise did you do today? ")

exercise_params = {
 "query": type_of_exercise,
 "gender": GENDER,
 "weight_kg": WEIGHT,
 "height_cm": HEIGHT,
 "age": AGE,
}

response = requests.post(url=exercise_endpoint, json=exercise_params, headers=headers)
result = response.json()
# print(response.text)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    add_row = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    sheet_response = requests.post(url=sheet_endpoint, json=add_row, headers=bearer_headers)
    print(sheet_response.text)
    # print(result["exercises"][0]["duration_min"])
