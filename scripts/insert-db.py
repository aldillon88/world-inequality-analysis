import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

response = (
    supabase.table("country_data")
    .insert(
        {
            "alpha2": "DE",
            "name": "Germany"
        }
    )
    .execute()
)

print(response)
