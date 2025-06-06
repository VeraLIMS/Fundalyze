import requests
from dotenv import load_dotenv
import os

load_dotenv()

headers = {
    "CF-Access-Client-Id": os.getenv("CF_ACCESS_CLIENT_ID"),
    "CF-Access-Client-Secret": os.getenv("CF_ACCESS_CLIENT_SECRET"),
    "Accept": "application/json",
}

resp = requests.get("https://api.veralims.com/items/portfolio", headers=headers)
print("Status:", resp.status_code)
print("Body:", resp.text)