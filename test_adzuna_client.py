from ingestion.adzuna_client import AdzunaClient

import json
from pathlib import Path

client = AdzunaClient()

print("Adzuna client initialised successfully.")
print("App ID available:", bool(client.app_id))
print("App Key available:", bool(client.app_key))

jobs = client.get_jobs()

if jobs is not None:
    print("\nAPI request successful!")

    print("Total matching jobs:", jobs["count"])
    print("Listings returned:", len(jobs["results"]))

    if jobs["results"]:
        print("First job fields:", jobs["results"][0].keys())

    raw_data_path = Path("data/raw/adzuna_jobs.json")

    with open(raw_data_path, "w", encoding="utf-8") as file:
        json.dump(jobs, file, indent=4, ensure_ascii=False)

    print("Raw API response saved successfully.")

else:
    print("API request failed.")