import requests
import json

url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/emprise-batie-et-non-batie/records?limit=20&refine=l_src%3A%22Fiche%20parcellaire%20et%20terrain%20certifi%C3%A9%22"

response = requests.get(url)

file_name = "emprise-batie-et-non-batie"

if response.status_code == 200:
    data = response.json()
    with open("Data/" + file_name +".txt", "w") as f: 
        f.write(json.dumps(data))
else:
    print("Erreur :", response.status_code)

