import os
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd
import numpy as np
import re

load_dotenv()

# Prepare file paths for loading data.
script_path = os.getcwd()
data_path = os.path.abspath(os.path.join(script_path, "data"))
aggregate_path = os.path.join(data_path, "aggregated")

# Define regex patterns for file names.
source_csv_pattern = ".*\.csv$"

# Preload files
files = os.listdir(aggregate_path)
data_files = [file for file in files if re.match(pattern=source_csv_pattern, string=file)]

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

schema = [
    'country',
    'countryname',
    'year',
    'variable',
    'unit',
    'value',
    'value_usd',
    'value_ppp',
    'value_usd_per_capita',
    'value_pct_national_income',
    'value_pct_gdp',
    'age',
    'shortname',
    'shorttype',
    'shortpop',
    'shortage',
    'region',
    'subregion'
]

def insert_data(data):
    try:
        response = (
            supabase.table("economic_data")
            .insert(
                data
            )
            .execute()
        )
        return response

    except Exception as exception:
        return exception

my_list = []

for file in data_files:
    file_path = f"{aggregate_path}/{file}"
    data = pd.read_csv(file_path, keep_default_na=False, na_values=[''], encoding='utf-8')[schema]
    my_list.append({file: False})
    data = data.replace({np.nan: None})

    # Chunk size for each insert
    chunk_size = 1000  # Adjust based on your row size

    # Insert data in chunks
    for i in range(0, len(data), chunk_size):
        chunk = data.iloc[i:i + chunk_size].to_dict(orient="records")
        result = insert_data(chunk)
        print(f"Inserted rows {i} to {i + chunk_size}, response: {result}")
