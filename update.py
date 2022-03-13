"""Script that updates the citations for the papers in the `data.json` file."""

import datetime
import json
import pandas as pd
import requests

SEMANTIC_SCHOLAR_PATH = 'http://api.semanticscholar.org/graph/v1/paper/'
QUERY_DETAILS = '?fields=citationCount'


def load_data():
    with open('data.json', 'r') as f:
        data_dict = json.load(f)
    df = pd.DataFrame(data_dict)
    return df

def update(df):
    df['datetime'] =  pd.to_datetime(df['last_updated'], format='%d %b %Y')
    df['last_updated'] = [x.strftime('%d %b %Y') for x in df['datetime']]
    df = df.sort_values(by=["datetime"])
    toady_str = datetime.datetime.now().strftime('%d %b %Y')
    for idx, row in df.iterrows():
            paper_id = row["paperID"]
            query_path = f"{SEMANTIC_SCHOLAR_PATH}{paper_id}{QUERY_DETAILS}"
            response = requests.get(query_path)

            if response.status_code == 429 or response.status_code == 403:
                break
            try:
                updated_citation = requests.get(
                    query_path).json()["citationCount"]
                df.loc[idx,["citations", "last_updated"]] = \
                    [updated_citation, toady_str]
            except Exception:
                print(f"Failed to update: {paper_id}")
                continue

    df = df.drop('datetime', axis=1)
    return df

def sort_and_save(df):
    df = df.sort_values(by=['citations'], ascending=False)
    df['rank'] = list(range(1, len(df)+1))
    with open('data.json', 'w') as f:
        json.dump(df.to_dict(orient='records'), f)

if __name__ == '__main__':
    df = load_data()
    df = update(df)
    sort_and_save(df)