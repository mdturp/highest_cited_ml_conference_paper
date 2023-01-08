"""Convert the list of titles to the all data file structure."""


import json
import re
import pandas as pd



conference_dirs  = ['iclr', 'icml', "neurips"]

def load_data(conference_dir, data_file_name):
    path = f'./data/{conference_dir}/{data_file_name}'
    with open(path, 'r') as f:
        title_data = json.load(f)
    return title_data

def save_data(conference_dir, data_file_name, data):
    path = f'./data/{conference_dir}/{data_file_name}'
    with open(path, 'w') as f:
        json.dump(data, f)



for c_dir in conference_dirs:
    title_data_json = load_data(
        conference_dir=c_dir, data_file_name="title.json")
    all_data_json = load_data(
        conference_dir=c_dir, data_file_name="all_data.json")
    
    df_all_data = pd.DataFrame(all_data_json)
    all_titles = list(df_all_data["title"].values)
    
    filtered_all_data_json = []
    for year_title_data in title_data_json:
        for title in year_title_data["title"]:
            title_cleaned = re.sub('\W+',' ', title)
            index = all_titles.index(title_cleaned)
            filtered_all_data_json.append(all_data_json[index])
    save_data(conference_dir=c_dir, data_file_name="all_data.json",
              data=filtered_all_data_json)