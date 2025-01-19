import os
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd
import numpy as np

load_dotenv()

# Prepare file paths for loading data.
script_path = os.getcwd()
data_path = os.path.abspath(os.path.join(script_path, "data"))
reference_path = os.path.join(data_path, "reference")

# Load data.
df = pd.read_csv(f"{reference_path}/variable_descriptions.csv")

# Convert df to list of dictionaries
list_of_dicts = df.replace({np.nan: None}).to_dict(orient='records')

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def insert_descriptions(data):
    try:
        response = (
            supabase.table("variable_descriptions")
            .insert(
                data
            )
            .execute()
        )
        return response

    except Exception as exception:
        return exception

result = insert_descriptions(list_of_dicts)
print(result)