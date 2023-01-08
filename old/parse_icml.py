"""Parse the html pages and obtain a list of all ICML paper titles.
"""
from bs4 import BeautifulSoup
import requests
import json


icml_conferences = [
    {"url": "https://proceedings.mlr.press/v139/",
     "year": 2021,
     "title": []},
     {"url": "https://proceedings.mlr.press/v119/",
     "year": 2020,
     "title": []},
     {"url": "https://proceedings.mlr.press/v97/",
     "year": 2019,
     "title": []},
     {"url": "https://proceedings.mlr.press/v80/",
     "year": 2018,
     "title": []},
     {"url": "https://proceedings.mlr.press/v70/",
     "year": 2017,
     "title": []},
]


for conference in icml_conferences:
    url = conference["url"]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    for p in soup.find_all("p", class_="title"):
        conference["title"].append(p.getText())

with open("icml_title.json", "w") as f:
    json.dump(icml_conferences, f)