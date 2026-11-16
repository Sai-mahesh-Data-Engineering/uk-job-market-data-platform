import requests

try:
    response = requests.get(
        "https://api.github.com",
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    print(data)

except requests.exceptions.Timeout:
    print("The request timed out.")

except requests.exceptions.HTTPError as error:
    print(f"HTTP error: {error}")

except requests.exceptions.RequestException as error:
    print(f"Request failed: {error}")