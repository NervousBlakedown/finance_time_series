# Imports
import os
import zipfile
import json
from kaggle.api.kaggle_api_extended import KaggleApi

# directory to store datasets
download_dir = "D:\\datasets\\github_financial_time_series_analysis"

# Load credentials 
with open("C:\\Users\\blake\\Documents\\github\\credentials\\kaggle.json", "r") as f:
    kaggle_creds = json.load(f)

# Initialize Kaggle API with manual credentials
api = KaggleApi()
api.authenticate()

# Dataset identifier from Kaggle
# full URL if needed: https://www.kaggle.com/datasets/andrewmvd/sp-500-stocks
dataset = 'andrewmvd/sp-500-stocks'

# download dataset
api.dataset_download_files(dataset, path = download_dir, unzip = True)

# Optional: List of CSV files I am specifically interested in
files_of_interest = ['sp500_companies.csv', 'sp500_index.csv', 'sp500_stocks.csv']

# Ensure files exist in the directory
for file_name in files_of_interest:
    file_path = os.path.join(download_dir, file_name)
    if os.path.exists(file_path):
        print(f'{file_name} has been downloaded successfully.')
    else:
        print(f'{file_name} is missing.')

print("Download and extraction complete.")