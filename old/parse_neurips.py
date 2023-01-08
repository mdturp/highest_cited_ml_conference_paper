"""Parse the html pages and obtain a list of all neurips paper titles.
"""
from bs4 import BeautifulSoup
import requests
import json


neurips_conferences = [
    {"url": "https://papers.nips.cc/paper/2021",
     "year": 2021,
     "title": []},
     {"url": "https://papers.nips.cc/paper/2020",
     "year": 2020,
     "title": []},
     {"url": "https://papers.nips.cc/paper/2019",
     "year": 2019,
     "title": []},
     {"url": "https://papers.nips.cc/paper/2018",
     "year": 2018,
     "title": []},
     {"url": "https://papers.nips.cc/paper/2017",
     "year": 2017,
     "title": []},
]


for conference in neurips_conferences:
    url = conference["url"]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    for li in soup.find_all("ul")[1].children:
        if li != "\n":
            paper_title = str(li.contents[0].text)
            conference["title"].append(paper_title)

with open("neurips_title.json", "w") as f:
    json.dump(neurips_conferences, f)