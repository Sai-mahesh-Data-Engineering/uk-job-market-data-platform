
from ingestion.local_reader import load_json
from processing.normalizer import normalize_adzuna_response
from processing.validator import validate_jobs


# 1. Load synthetic Adzuna response
raw_data = load_json("data/sample/adzuna_jobs_synthetic.json")

# 2. Normalise the records
normalised_jobs = normalize_adzuna_response(raw_data)

# 3. Validate the records
validation_results = validate_jobs(normalised_jobs)

# 4. Display results
valid_count = 0
invalid_count = 0

for result in validation_results:
    print("\nJob:", result["job"]["job_title"])
    print("Valid:", result["is_valid"])

    if result["is_valid"]:
        valid_count += 1
    else:
        invalid_count += 1
        print("Errors:", result["errors"])

print("\n========== VALIDATION SUMMARY ==========")
print("Total records:", len(validation_results))
print("Valid records:", valid_count)
print("Invalid records:", invalid_count)

bad_job = normalised_jobs[0].copy()

bad_job["job_title"] = None
bad_job["salary_min"] = 70000
bad_job["salary_max"] = 30000

print("\n========== INVALID RECORD TEST ==========")

errors = validate_jobs([bad_job])

for error in errors[0]["errors"]:
    print("-", error)
