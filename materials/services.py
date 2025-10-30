import os

import requests
from dotenv import load_dotenv

load_dotenv()


STRIPE_API_KEY = os.getenv("STRIPE")
STRIPE_URL = "https://api.stripe.com/v1"
HEADERS = {"Authorization": f"Bearer {STRIPE_API_KEY}"}


def stripe_api_request(method, endpoint, data=None):
    """Общая функция для выполнения запросов к API Stripe."""
    url = f"{STRIPE_URL}/{endpoint}"

    if method == "POST":
        response = requests.post(url=url, headers=HEADERS, data=data)
    elif method == "GET":
        response = requests.get(url=url, headers=HEADERS)
    else:
        raise ValueError(f"Метод {method} не поддерживается")

    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(
            f"Ошибка Stripe (код {response.status_code}): {response.json().get('error', 'Неизвестная ошибка')}"
        )
        return response.json()


def create_course(course_name, description=None):
    """Создает Продукт в Stripe."""
    data = {"name": course_name, "description": description}
    return stripe_api_request("POST", "products", data=data)


def create_price(amount, product_id):
    """Создает Цену (Price) для Продукта в Stripe."""
    data = {
        "unit_amount": int(amount * 100),
        "currency": "rub",
        "product": product_id,
        "recurring[interval]": "month",
    }
    return stripe_api_request("POST", "prices", data=data)


def create_session(price_id, success_url, cancel_url):
    """Создает сессию оплаты Checkout Session в Stripe."""
    data = {
        "line_items[0][price]": price_id,
        "line_items[0][quantity]": 1,
        "mode": "payment",
        "success_url": success_url,
        "cancel_url": cancel_url,
    }
    return stripe_api_request("POST", "checkout/sessions", data=data)


def retrieve_session(session_id):
    """Получает информацию о сессии Stripe по ее ID."""
    endpoint = f"checkout/sessions/{session_id}"
    return stripe_api_request("GET", endpoint)
