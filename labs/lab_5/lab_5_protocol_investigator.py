# -*- coding: utf-8 -*-
# LAB 5 - PROTOCOL INVESTIGATOR
import sys
from pathlib import Path

# Get the root directory
ROOT = Path(__file__).resolve().parents[2]

API_FOLDER = ROOT / "api"
# Insert the API folder into the system path

sys.path.insert(0, str(API_FOLDER))

from fake_api import FakeAPI  # type: ignore

# Create a fake API object
api = FakeAPI(api_key="training-key")


# Get the customers
def get_customers(
    page: int = 1,
    page_size: int = 10,
    country: str | None = None,
    risk_level: str | None = None,
):
    # Create a dictionary of parameters
    params = {"page": page, "page_size": page_size}

    if country is not None:
        # Add the country to the parameters
        params["country"] = country

    if risk_level is not None:
        # Add the risk level to the parameters
        params["risk_level"] = risk_level

    # Return the customers
    return api.customers.list(**params)


# Main function
def main():
    # Get the customers
    response = get_customers(
        page=1, page_size=10, country="US", risk_level="LOW"
    )

    # Print the response
    print(f"[STATUS]: {response.status_code}")
    print(f"[EXECUTION TIME]: {response.processing_time_ms}")
    print(f"[REQUEST_ID]: {response.request_id}")

    print("\n")

    if response.ok:
        print("Customers: \n")

        for customer in response.data["data"]:
            print(f"{customer['customer_id']}")
            print(f"{customer['first_name']}")
            print(f"{customer['last_name']}")
            print(f"{customer['credit_score']}")
    else:
        print(response.error)


if __name__ == "__main__":
    main()
