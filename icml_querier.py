import requests
import time
from typing import Dict, Any
import json
import datetime

def query_semantic_scholar_for_paper_details(
        title: str, conference: str) -> Dict[str, Any]:
    """Query the details of a paper in the semantic scholar database.

    Args:
        title (str): The title of the paper.
        conference (str): The conference the paper was published at.

    Returns:
        Dict[str, Any]: The dictionary containing the details of the paper.
    """
    base_url = "http://api.semanticscholar.org/graph/v1/paper/"
    url = f"{base_url}search?query={title}&venue={conference}"
    response = requests.get(url)
    response_json = response.json()

    paper_id = response_json["data"][0]["paperId"]
    query_details = (f"{base_url}{paper_id}?fields=citationCount,title")
    detail_response = requests.get(query_details)

    return detail_response.json()

if __name__ == "__main__":

    with open("icml_data.json", "r") as f:
        icml_data = json.load(f)

    with open("icml_title.json", "r") as f:
        icml_title = json.load(f)

        
    already_queried_titles = [x["title"] for x in icml_data]
    toady_str = datetime.datetime.now().strftime('%d %b %Y')

    for icml_year in icml_title:
        year = icml_year["year"]
        conference = "ICML"
        
        for title in icml_year["title"]:
            if title in already_queried_titles:
                continue
            for i in range(2):
                data = {"title": title, "year": year, "conference": conference,
                        "last_updated": toady_str}
                try:
                    response = query_semantic_scholar_for_paper_details(
                        title=title, conference=conference)
            
                    data["paperID"] = response["paperId"]
                    data["citations"] = response["citationCount"]
                    icml_data.append(data)
                    already_queried_titles.append(title)
                except:
                    icml_data = sorted(icml_data,
                                       key=lambda d: -int(d['citations'])) 
                    with open("icml_data.json", "w") as f:
                        json.dump(icml_data, f)
                    print("I am sleeping ...")
                    time.sleep(360)
                    continue
                else:
                    break
