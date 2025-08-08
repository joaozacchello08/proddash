from dotenv import load_dotenv
import requests
from os import getenv
from pathlib import Path
import webbrowser

load_dotenv()

API_KEY = getenv("SECRET_KEY")

BASE_URL = "http://localhost:8080/"

response = requests.get(url=BASE_URL,
                        headers={"X-API-KEY": API_KEY})

desktop_path = Path.home() / "Desktop"
file_path = desktop_path / "index.html"

with open(file_path, "w", encoding="utf-8") as f:
    f.truncate(0)
    f.write(response.text)

webbrowser.open("file://" + file_path.resolve().as_posix())
