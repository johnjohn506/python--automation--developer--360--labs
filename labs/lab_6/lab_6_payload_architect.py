# -*- coding: utf-8 -*-
# LAB 6 - PAYLOAD ARCHITECT
import sys
from pathlib import Path

# Get the root directory
ROOT = Path(__file__).resolve().parents[2]

# Get the API folder
API_FOLDER = ROOT / "api"

# Insert the API folder into the system path
sys.path.insert(0, str(API_FOLDER))

# Import the FakeAPI class
from fake_api import FakeAPI  # type: ignore

# Create a fake API object
api = FakeAPI(api_key="training-key")


# Create a customer
def create_customer(customer):
    # Return the customer
    return api.customers.create(customer)


# Main function
def main():
    # Create a customer
    customer = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "country": "US",
        "status": "ACTIVE",
        "risk_level": "LOW",
        "credit_score": 745,
        "contact": {
            "phone": "+1-555-123-4567",
            "preferred_language": "English",
        },
        "address": {
            "street": "100 Main Street",
            "city": "Austin",
            "state": "Texas",
            "zip_code": "78701",
        },
        "employment": {
            "company": "Experian",
            "position": "Automation Engineer",
            "years": 5,
        },
        "products": [
            {
                "type": "Credit Card",
                "status": "ACTIVE",
                "limit": 10000,
            },
            {
                "type": "Mortgage",
                "status": "ACTIVE",
                "balance": 250000,
            },
        ],
    }

    # Create a customer and print the response
    response = create_customer(customer)

    # Print the response
    print(f"Status Code : {response.status_code}")
    print(f"Request ID  : {response.request_id}")
    print(f"Latency     : {response.processing_time_ms} ms")

    print()

    # Check if the customer was created successfully
    if response.status_code == 201:
        print("Customer created successfully.")
        print(response.json())
    # Check if the customer was not created successfully
    elif response.status_code == 400:
        print("Validation Error")
        print(response.error["message"])
        print()
        print("Missing Required Fields")

        for field in response.error["missing_fields"]:
            print(f" - {field}")
    else:
        print("Unexpected Error")
        print(response.error)


# Main function
if __name__ == "__main__":
    main()
