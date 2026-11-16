
from datetime import datetime, timezone


def normalize_adzuna_job(job):
    """
    Convert one raw Adzuna job into the common job schema.
    """

    company = job.get("company") or {}
    location = job.get("location") or {}

    return {
        "source_name": "adzuna",
        "source_job_id": str(job["id"]) if job.get("id") is not None else None,
        "job_title": job.get("title"),
        "company_name": company.get("display_name"),
        "location": location.get("display_name"),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "salary_currency": "GBP",
        "salary_period": None,
        "job_description": job.get("description"),
        "job_url": job.get("redirect_url"),
        "posted_at": job.get("created"),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "contract_type": job.get("contract_type"),
        "working_arrangement": None,
    }


def normalize_adzuna_response(response):
    """
    Normalise all job records in an Adzuna API response.
    """

    raw_jobs = response.get("results", [])

    return [
        normalize_adzuna_job(job)
        for job in raw_jobs
    ]
