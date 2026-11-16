
from ingestion.local_reader import load_json

file_path = "data/sample/adzuna_jobs_synthetic.json"

data = load_json(file_path)

print("Dataset loaded successfully.")
print("Total matching jobs:", data["count"])
print("Records retrieved:", len(data["results"]))

for job in data["results"]:
    print(job["id"], "-", job["title"])
