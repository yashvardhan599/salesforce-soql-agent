import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

def get_salesforce_token():
    payload = {
        "grant_type": "password",
        "client_id": os.getenv("SALESFORCE_CLIENT_ID"),
        "client_secret": os.getenv("SALESFORCE_CLIENT_SECRET"),
        "username": os.getenv("SALESFORCE_USERNAME"),
        "password": os.getenv("SALESFORCE_PASSWORD"),
    }

    login_url = os.getenv("SALESFORCE_LOGIN_URL")
    response = requests.post(
        f"{login_url}/services/oauth2/token",
        data=payload,
        timeout=30
    )
    response.raise_for_status()

    data = response.json()
    return data["access_token"], data["instance_url"]
