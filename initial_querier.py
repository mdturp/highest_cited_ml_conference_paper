"""Query the initial data for a paper."""

import requests
import time
from typing import Dict, Any
import json
import datetime

def query_paper_id(title:str, conference: str) -> Dict[str, Any]:
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
        paper_id: str) -> Dict[str, Any]:
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


def save(c_dir, not_found):
    with open(f"data/{c_dir}/not_found.json", "w") as f:
        json.dump(not_found, f)

if __name__ == "__main__":

    conference_dir = ["icml", "neurips"]
    conference_name = ["ICML", "NeurIPS"]
    toady_str = datetime.datetime.now().strftime('%d %b %Y')

    for c_dir, c_name in zip(conference_dir, conference_name):
        with open(f"data/{c_dir}/data.json", "r") as f:
            all_data = json.load(f)

        with open(f"data/{c_dir}/title.json", "r") as f:
            title_data = json.load(f)

        with open(f"data/{c_dir}/not_found.json", "r") as f:
            not_found = json.load(f)

        already_found_titles = [x["title"] for x in all_data]
        not_found_yet = [x["title"] for x in not_found]

        for t in title_data:
            year = t["year"]
            for title in t["title"]:
                if title in already_found_titles:
                    continue

                data = {"title": title, "year": year, "conference": c_name,
                        "last_updated": toady_str}

                result = query_paper_id(title=title, conference=c_name)
                result_data = result.json()
                if result.status_code != 200:
                    print("I am sleeping ...")
                    save(c_dir=c_dir, not_found=not_found)
                    time.sleep(360)
                    result = query_paper_id(title=title, conference=c_name)
                    result_data = result.json()
                
                if result_data["data"] == []:
                    if title in not_found_yet:
                        continue
                    else:
                        not_found.append(data)
                        not_found_yet.append(title)
                else:
                    # Assume that the first element is the correct paper.
                    paper_id = result_data["data"][0]["paperId"]

                    response = query_semantic_scholar_for_paper_details(
                        paper_id=paper_id)
                    if response.status_code != 200:
                        print("I am sleeping ...")
                        save(c_dir=c_dir, not_found=not_found)
                        time.sleep(360)
                        response = query_semantic_scholar_for_paper_details(
                            paper_id=paper_id)
                    
                    data["paperID"] = response.json()["paperId"]
                    data["citations"] = response.json()["citationCount"]
                    all_data.append(data)
                    already_found_titles.append(title)
                    
                    if title in not_found_yet:
                        not_found.pop(not_found_yet.index(title))