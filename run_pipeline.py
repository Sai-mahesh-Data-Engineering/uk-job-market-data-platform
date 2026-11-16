
import json
from pathlib import Path

from ingestion.local_reader import load_json

from processing.normalizer import normalize_adzuna_response
from processing.reed_normalizer import normalize_reed_response
from processing.validator import validate_jobs


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

ADZUNA_FILE = PROJECT_ROOT / "data/sample/adzuna_jobs_synthetic.json"
REED_FILE = PROJECT_ROOT / "data/sample/reed_jobs_synthetic.json"

OUTPUT_DIR = PROJECT_ROOT / "data/processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOAD SOURCE DATA
# --------------------------------------------------

print("\nLoading source datasets...")

adzuna_data = load_json(ADZUNA_FILE)
reed_data = load_json(REED_FILE)

print("Adzuna records:", len(adzuna_data["results"]))
print("Reed records:", len(reed_data))


# --------------------------------------------------
# 3. NORMALISE SOURCE DATA
# --------------------------------------------------

print("\nNormalising records...")

adzuna_jobs = normalize_adzuna_response(adzuna_data)
reed_jobs = normalize_reed_response(reed_data)

# Combine both sources
all_jobs = adzuna_jobs + reed_jobs

print("Total normalised records:", len(all_jobs))


# --------------------------------------------------
# 4. VALIDATE COMBINED DATA
# --------------------------------------------------

print("\nValidating records...")

validation_results = validate_jobs(all_jobs)

valid_jobs = [
    result["job"]
    for result in validation_results
    if result["is_valid"]
]

rejected_jobs = [
    {
        "job": result["job"],
        "errors": result["errors"]
    }
    for result in validation_results
    if not result["is_valid"]
]


# --------------------------------------------------
# 5. SAVE OUTPUT DATA
# --------------------------------------------------

valid_output = OUTPUT_DIR / "validated_jobs.json"
rejected_output = OUTPUT_DIR / "rejected_jobs.json"

with open(valid_output, "w", encoding="utf-8") as file:
    json.dump(valid_jobs, file, indent=4, ensure_ascii=False)

with open(rejected_output, "w", encoding="utf-8") as file:
    json.dump(rejected_jobs, file, indent=4, ensure_ascii=False)


# --------------------------------------------------
# 6. PIPELINE SUMMARY
# --------------------------------------------------

print("\n========== PIPELINE SUMMARY ==========")

print("Adzuna records:", len(adzuna_jobs))
print("Reed records:", len(reed_jobs))
print("Total records:", len(all_jobs))
print("Valid records:", len(valid_jobs))
print("Rejected records:", len(rejected_jobs))

print("\nOutput files:")
print(valid_output)
print(rejected_output)

print("\nPipeline execution completed.")
