from dotenv import load_dotenv
import requests
from os import getenv, path
import webbrowser

load_dotenv()

API_KEY = getenv("SECRET_KEY")

response = requests.get(url="http://127.0.0.1:8000/",
                        headers={"X-API-KEY": API_KEY})

file_path = "./test/root.html"

with open(file_path, "w", encoding="utf-8") as f:
    f.truncate(0)
    f.write(response.text)

webbrowser.open("file://" + path.abspath(file_path))
