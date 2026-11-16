
from datetime import datetime


REQUIRED_FIELDS = [
    "source_name",
    "source_job_id",
    "job_title",
]


def validate_job(job):
    """
    Validate one normalised job record.
    Returns a list of validation errors.
    """

    errors = []

    # Required fields
    for field in REQUIRED_FIELDS:
        value = job.get(field)

        if value is None or (
            isinstance(value, str) and not value.strip()
        ):
            errors.append(f"Missing required field: {field}")

    # Salary checks
    salary_min = job.get("salary_min")
    salary_max = job.get("salary_max")

    for field, value in [
        ("salary_min", salary_min),
        ("salary_max", salary_max),
    ]:
        if value is not None:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                errors.append(f"{field} must be numeric")
            elif value < 0:
                errors.append(f"{field} cannot be negative")

    if (
        isinstance(salary_min, (int, float))
        and not isinstance(salary_min, bool)
        and isinstance(salary_max, (int, float))
        and not isinstance(salary_max, bool)
        and salary_min > salary_max
    ):
        errors.append("salary_min cannot exceed salary_max")

    # Date checks
    for field in ["posted_at", "ingested_at"]:
        value = job.get(field)

        if value is not None:
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                errors.append(f"{field} must be a valid ISO date")

    return errors


def validate_jobs(jobs):
    """
    Validate multiple jobs and identify duplicate source records.
    """

    results = []
    seen_ids = set()

    for job in jobs:
        errors = validate_job(job)

        source_key = (
            job.get("source_name"),
            job.get("source_job_id"),
        )

        if source_key in seen_ids:
            errors.append("Duplicate source record")

        seen_ids.add(source_key)

        results.append({
            "job": job,
            "is_valid": len(errors) == 0,
            "errors": errors,
        })

    return results
