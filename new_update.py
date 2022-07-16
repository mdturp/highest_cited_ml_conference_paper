"""Script that updates the citations for the papers in the `data.json` file."""

import datetime
import json
import pandas as pd
import requests

SEMANTIC_SCHOLAR_PATH = 'http://api.semanticscholar.org/graph/v1/paper/'
QUERY_DETAILS = '?fields=citationCount'

def load_failure_json():
    with open('data/failure_cases.json', "r") as f:
        failure_cases = json.load(f)
    return failure_cases

def save_failure_json(data):
    with open('data/failure_cases.json', "w") as f:
        json.dump(data, f)

def load_data():
    with open('data/neurips/all_data.json', 'r') as f:
        data_dict_neurips = json.load(f)
    df_neurips = pd.DataFrame(data_dict_neurips)
    with open('data/icml/all_data.json', 'r') as f:
        data_dict_icml = json.load(f)
    df_icml = pd.DataFrame(data_dict_icml)
    with open('data/iclr/all_data.json', 'r') as f:
        data_dict_iclr = json.load(f)
    df_iclr = pd.DataFrame(data_dict_iclr)

    df = pd.concat([df_neurips, df_icml, df_iclr])
    df = df.reset_index().drop("index", axis=1)
    return df


def query_paper_id(title: str, conference: str) -> requests.Response:
    """Query the id of the paper based on the title.

    Args:
        title (str): The title of the paper.
        conference (str): The conference the paper was published at.

    Returns:
        Dict[str, Any]: Dictionary containing the paper.
    """
    base_url = "http://api.semanticscholar.org/graph/v1/paper/"
    url = f"{base_url}search?query={title}&venue={conference}"
    response = requests.get(url)
    return response


def query_semantic_scholar_for_paper_details(
        paper_id: str) -> requests.Response:
    """Query the details of a paper in the semantic scholar database.

    Args:
        paper_id (str): The semantic scholar paper_id

    Returns:
        Dict[str, Any]: The dictionary containing the details of the paper.
    """
    base_url = "http://api.semanticscholar.org/graph/v1/paper/"
    query_details = (f"{base_url}{paper_id}?fields=citationCount,title")
    detail_response = requests.get(query_details)
    return detail_response


def update(df):
    df['datetime'] = pd.to_datetime(df['last_updated'], format='%d %b %Y')
    df['last_updated'] = [x.strftime('%d %b %Y') for x in df['datetime']]
    df = df.sort_values(by=["datetime"])
    failure_cases = load_failure_json()
    toady_str = datetime.datetime.now().strftime('%d %b %Y')
    print("Updating")
    for idx, row in df.iterrows():
        paper_id = row["paperID"]
        conference = row["conference"]
        title = row["title"]
        print(f"`{title}`")
        if paper_id == "-":
            response = query_paper_id(
                title=title, conference=conference)
            if response.status_code == 429 or response.status_code == 403:
                break
            if response.json()["data"] == []:
                df.loc[idx, ["last_updated"]] = [toady_str]
            else:
                # Assume that the first element is the correct paper.
                paper_id = response.json()["data"][0]["paperId"]
                response_details = query_semantic_scholar_for_paper_details(
                    paper_id=paper_id)
                if (response_details.status_code == 429
                    or response_details.status_code == 403):
                    break

                updated_citation = response_details.json()["citationCount"]
                df.loc[idx, ["paperID", "citations", "last_updated"]] = \
                    [paper_id, updated_citation, toady_str]
        else:
            response_details = query_semantic_scholar_for_paper_details(
                paper_id=paper_id)

            if response_details.status_code == 429 or response_details.status_code == 403:
                break
            try:
                updated_citation = response_details.json()["citationCount"]
            except Exception as e:
                entry = failure_cases.get(title, {"err_msg": [],
                                                    "err_time": [],
                                                    "paper_id": []})
                entry["err_msg"].append(response_details.json())
                entry["err_time"].append(toady_str)
                entry["paper_id"].append(paper_id)

                failure_cases["title"] = entry
                
                continue 

            df.loc[idx, ["citations", "last_updated"]] = \
                [updated_citation, toady_str]
        
    save_failure_json(failure_cases)
    df = df.drop('datetime', axis=1)
    return df


def sort_and_save(df):
    df["citations_"] = [x if x != "-" else 0 for x in df["citations"]]
    df = df.sort_values(by=['citations_'], ascending=False)
    df = df.drop("citations_", axis=1)

    df_icml = df[df["conference"] == "ICML"]
    with open('data/icml/all_data.json', 'w') as f:
        json.dump(df_icml.to_dict(orient='records'), f)
    with open('data/icml/1000_data.json', 'w') as f:
        json.dump(df_icml[:1000].to_dict(orient='records'), f)

    df_neurips = df[df["conference"] == "NeurIPS"]
    with open('data/neurips/all_data.json', 'w') as f:
        json.dump(df_neurips.to_dict(orient='records'), f)
    with open('data/neurips/1000_data.json', 'w') as f:
        json.dump(df_neurips[:1000].to_dict(orient='records'), f)
    
    df_iclr = df[df["conference"] == "ICLR"]
    with open('data/iclr/all_data.json', 'w') as f:
        json.dump(df_iclr.to_dict(orient='records'), f)
    with open('data/iclr/1000_data.json', 'w') as f:
        json.dump(df_iclr[:1000].to_dict(orient='records'), f)


if __name__ == '__main__':
    df = load_data()
    df = update(df)
    sort_and_save(df)
