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
    for row in rows[1:]:        
        cells = row.find_all("th")
        cells.extend(row.find_all("td"))
        
        if len(cells) != 1:
            if not same_year:
                rowspan = int(cells[0]["rowspan"]) if 'rowspan' in cells[0].attrs else 0
                same_year = rowspan > 0
                year = cells[0]
                title = cells[1]
            else:
                title = cells[0]
        else:
            year = cells[0]
            rowspan = int(cells[0]["rowspan"]) if 'rowspan' in cells[0].attrs else 0
            same_year = rowspan > 0
            continue
        
        arr = [year.text.replace("\n", ""), title.text.replace("\n", ""), rowspan]
        data.append(arr)
        
        rowspan = rowspan - 1
        same_year = rowspan > 0
    
    return data

actor_name = input("Digite o nome do ator ou da atriz: ") or "Fernanda Montenegro"

link = f"https://pt.wikipedia.org/wiki/Filmografia_de_" + actor_name.replace(" ", "_")
request = requests.get(link)
site = BeautifulSoup(request.text, "html.parser")
if site.text.find("A Wikipédia não possui um artigo com este nome exato") != -1:
    link = f"https://pt.wikipedia.org/wiki/" + actor_name.replace(" ", "_")
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

columns = ["Year", "Title", "n"]
df = pd.DataFrame(data, columns=columns)

# movies_by_year = df.groupby(["Year"]).count()
# movies_by_year.plot(kind="bar")
# plt.title(f"Movies per year of {actor_name}")
# plt.show()
print(df)