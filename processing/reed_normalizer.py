
from datetime import datetime, timezone


def get_first_value(record, *field_names):
    """Return the first available, non-null field value."""

    for field in field_names:
        value = record.get(field)

        if value is not None:
            return value

    return None


def normalize_reed_job(job):
    """
    Convert a Reed job-search record into our common job schema.
    """

    job_id = get_first_value(job, "jobId", "JobId", "id")

    return {
        "source_name": "reed",
        "source_job_id": str(job_id) if job_id is not None else None,
        "job_title": get_first_value(job, "jobTitle", "JobTitle", "title"),
        "company_name": get_first_value(
            job, "employerName", "EmployerName", "company"
        ),
        "location": get_first_value(
            job, "locationName", "LocationName", "location"
        ),
        "salary_min": get_first_value(
            job, "minimumSalary", "MinimumSalary", "salaryMin"
        ),
        "salary_max": get_first_value(
            job, "maximumSalary", "MaximumSalary", "salaryMax"
        ),
        "salary_currency": None,
        "salary_period": None,
        "job_description": get_first_value(
            job, "jobDescription", "JobDescription", "description"
        ),
        "job_url": get_first_value(job, "jobUrl", "JobUrl", "url"),
        "posted_at": None,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "contract_type": None,
        "working_arrangement": None,
    }


def normalize_reed_response(response):
    """
    Normalise all jobs returned by Reed search.
    """

    if isinstance(response, dict):
        raw_jobs = response.get("results", [])
    else:
        raw_jobs = response

    return [
        normalize_reed_job(job)
        for job in raw_jobs
    ]
