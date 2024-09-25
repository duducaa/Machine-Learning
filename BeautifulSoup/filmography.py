import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def verify_table(table):
    return len(table.find_all("tr")) > 1

def extract(table):
    data = []
    rows = table.find("tbody").find_all("tr")
    year = ""
    same_year = False
    rowspan = 0
    for row in rows:
        td = row.find_all("td")
        if len(td) == 0: 
            continue
        
        title = td[1].text.replace("\n", "")
        
        if not same_year:
            rowspan = int(td[0]["rowspan"]) if 'rowspan' in td[0].attrs else 0
            same_year = rowspan is not None
            year = td[0].text.replace("\n", "")
        else:
            title = td[0].text.replace("\n", "")
        
        data.append((year, title))
        rowspan = rowspan - 1
        
        same_year = rowspan > 0
    
    return data

actor_name = input("Digite o nome do ator ou da atriz: ").replace(" ", "_")

link = f"https://pt.wikipedia.org/wiki/Filmografia_de_{actor_name}"
request = requests.get(link)
site = BeautifulSoup(request.text, "html.parser")
if site.text.find("A Wikipédia não possui um artigo com este nome exato") != -1:
    link = f"https://pt.wikipedia.org/wiki/{actor_name}"
    request = requests.get(link)
    site = BeautifulSoup(request.text, "html.parser")
    
ids = ["Filmografia", "Cinema", "Filmes", "Filme"]
for id in ids:
    try:
        heading = site.find("h2", id=id).findParent()
    except:
        pass
    else:
        break

table = heading.findNextSibling()

while table.name != "table":
    table = table.findNextSibling()

data = extract(table)

columns = ["Year", "Title"]
df = pd.DataFrame(data, columns=columns)

movies_by_year = df.groupby(["Year"]).count()
movies_by_year.plot(kind="bar")
plt.show()
print(df)