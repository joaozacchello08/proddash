import requests
from dotenv import load_dotenv
import os
import webbrowser

load_dotenv()
key = os.getenv("SECRET_KEY")

response = requests.get(url="http://localhost:6969/",
                        headers={"X-API-KEY": key})
path = os.path.abspath(__file__) # current file
path = os.path.dirname(path) + "/"
file_name = "index.html"

with open(path + file_name, "w") as f:
    f.write(response.text)

webbrowser.open(f"file:///{path + file_name}")
