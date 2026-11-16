
from processing.reed_normalizer import normalize_reed_response
from processing.validator import validate_jobs


# Synthetic Reed response for local development
synthetic_reed_response = [
    {
        "jobId": 123456,
        "employerName": "Example Data Ltd",
        "jobTitle": "Data Engineer",
        "locationName": "Birmingham",
        "minimumSalary": 35000,
        "maximumSalary": 45000,
        "jobDescription": "A fictional data engineering role.",
        "jobUrl": "https://www.reed.co.uk/jobs/example",
    },
    {
        "jobId": 123457,
        "employerName": "Example Analytics Ltd",
        "jobTitle": "Junior Data Engineer",
        "locationName": "Manchester",
        "minimumSalary": 28000,
        "maximumSalary": 32000,
        "jobDescription": "A fictional junior role.",
        "jobUrl": "https://www.reed.co.uk/jobs/example-2",
    },
]


# Normalise
normalised_jobs = normalize_reed_response(
    synthetic_reed_response
)

# Validate
results = validate_jobs(normalised_jobs)

for result in results:
    print("\nJob:", result["job"]["job_title"])
    print("Source:", result["job"]["source_name"])
    print("Valid:", result["is_valid"])
    print("Errors:", result["errors"])

print("\nTotal Reed records:", len(normalised_jobs))
