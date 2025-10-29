import os

import requests
from dotenv import load_dotenv


load_dotenv()

def create_course(course_name, description=None):
    url = "https://api.stripe.com/v1/products"
    api_key = os.getenv("STRIPE")
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "name": course_name,
        "description": description
    }
    response = requests.post(url=url, headers=headers, data=data)
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"Ошибка HTTP: {response.status_code}")
        return response.json()
