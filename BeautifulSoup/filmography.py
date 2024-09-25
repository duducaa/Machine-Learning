import requests
from bs4 import BeautifulSoup

link = "https://en.wikipedia.org/wiki/Robert_Downey_Jr._filmography"
request = requests.get(link)

site = BeautifulSoup(request.text, "html.parser")
platforms = site.find_all("div", {"class": "mw-heading2"})
tables = site.find_all("table")
for platform, table in zip(platforms[:-2], tables):
    name = platform.find("h2").text
    print(f"======== {name} ========")
    rows = table.find("tbody").find_all("tr")
    for row in rows:
        movie = row
        print(f"-- {movie}")