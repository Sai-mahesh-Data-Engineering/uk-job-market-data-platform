
import requests

from requests.exceptions import Timeout, HTTPError, RequestException
from config.settings import REED_API_KEY


class ReedClient:

    def __init__(self):
        if not REED_API_KEY:
            raise RuntimeError("Missing Reed API key. Check your .env file.")

        self.api_key = REED_API_KEY
        self.base_url = "https://www.reed.co.uk/api/1.0"

    def get_jobs(
        self,
        keywords="Data Engineer",
        location="London",
        results_to_take=10,
        results_to_skip=0,
        timeout=15
    ):

        if not 1 <= results_to_take <= 100:
            raise ValueError("results_to_take must be between 1 and 100")

        url = f"{self.base_url}/search"

        params = {
            "keywords": keywords,
            "locationName": location,
            "resultsToTake": results_to_take,
            "resultsToSkip": results_to_skip,
        }

        try:
            response = requests.get(
                url,
                params=params,
                auth=(self.api_key, ""),
                timeout=timeout
            )

            response.raise_for_status()
            return response.json()

        except Timeout:
            print("Reed API request timed out.")
            return None

        except HTTPError as error:
            print(f"Reed API HTTP error: {error.response.status_code}")
            return None

        except RequestException as error:
            print(f"Reed API request failed: {error}")
            return None
