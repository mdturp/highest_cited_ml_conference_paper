"""Script that updates the citations for the papers in the `data.json` file."""

import json
import pandas as pd
import datetime


def load_data():
    with open("data.json", "r") as f:
        data_dict = json.load(f)
    df = pd.DataFrame(data_dict)
    return df

def update(df):
    df['datetime'] =  pd.to_datetime(df["last_updated"], format='%d %b %Y')
    df["last_updated"] = [x.strftime("%d %b %Y") for x in df["datetime"]]
    df = df.drop("datetime", axis=1)
    return df

def sort_and_save(df):
    df = df.sort_values(by=['citations'], ascending=False)
    df["rank"] = list(range(1, len(df)+1))
    with open("data.json", "w") as f:
        json.dump(df.to_dict(orient="records"), f)

if __name__ == "__main__":
    df = load_data()
    df = update(df)
    sort_and_save(df)