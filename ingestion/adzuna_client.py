
import time
import requests

from requests.exceptions import Timeout, HTTPError, RequestException
from config.settings import ADZUNA_APP_ID, ADZUNA_APP_KEY


class AdzunaClient:

    def __init__(self):
        self.app_id = ADZUNA_APP_ID
        self.app_key = ADZUNA_APP_KEY

    def get_jobs(self, page=1, results_per_page=5, max_attempts=3):

        # API endpoint
        url = f"https://api.adzuna.com/v1/api/jobs/gb/search/{page}"

        # API query parameters
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": results_per_page,
            "what": "Data Engineer",
            "where": "London",
            "content-type": "application/json"
        }



        # Retry loop
        for attempt in range(1, max_attempts + 1):

            try:
                response = requests.get(
                    url,
                    params=params,
                    timeout=15
                )

                response.raise_for_status()

                # Successful response
                return response.json()

            except Timeout:

                print(f"Request timed out. Attempt {attempt}")

                if attempt == max_attempts:
                    print("Maximum attempts reached.")
                    return None

                # Exponential backoff: 2 seconds, then 4 seconds
                wait_seconds = 2 ** attempt
                time.sleep(wait_seconds)

            except HTTPError as error:

                status_code = error.response.status_code

                if status_code == 429:

                    print("Rate limit exceeded.")

                    if attempt == max_attempts:
                        print("Maximum attempts reached.")
                        return None

                    retry_after = error.response.headers.get(
                        "Retry-After"
                    )

                    try:
                        wait_seconds = max(0, int(retry_after))
                    except (TypeError, ValueError):
                        wait_seconds = 2 ** attempt

                    print(f"Waiting {wait_seconds} seconds.")
                    time.sleep(wait_seconds)

                else:
                    print(f"HTTP error: {status_code}")
                    return None

            except RequestException as error:

                print(f"Request failed: {error}")
                return None

        return None
