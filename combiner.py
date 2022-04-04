"""Script that looks for the papers on semantic scholar."""


import json
import pandas as pd
import datetime
import re

def all_data(c_dir="neurips"):

    with open(f"data/{c_dir}/data.json", "r") as f:
        all_data = json.load(f)
    with open(f"data/{c_dir}/title.json", "r") as f:
        title_data = json.load(f)

    all_titles = [d["title"] for d in all_data]

    conference_dict = {"neurips": "NeurIPS",
                       "icml": "ICML",
                       "iclr": "ICLR"}
    conference = conference_dict[c_dir]
    today_str = (datetime.datetime.now()
                 - datetime.timedelta(days=7)).strftime('%d %b %Y')
    print(len(all_data))
    for title_year in title_data:
        year = title_year["year"]
        for title in title_year["title"]:
            title = re.sub('\W+',' ', title)
            if title not in all_titles:
                all_data.append(
                    {"paperID": "-",
                    "title": title,
                    "year": year,
                    "conference": conference,
                    "citations": "-",
                    "last_updated": today_str}
                )
    
    df = pd.DataFrame(all_data)
    df["citations_"] = [x if x != "-" else 0 for x in df["citations"]]
    df = df.sort_values(by=['citations_'], ascending=False)
    df = df.drop("citations_", axis=1)
    with open(f"data/{c_dir}/all_data.json", 'w') as f:
        json.dump(df.to_dict(orient='records'), f)
    print(len(all_data))

all_data(c_dir="neurips")
all_data(c_dir="icml")
all_data(c_dir="iclr")