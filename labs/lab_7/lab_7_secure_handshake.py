# -*- coding: utf-8 -*-
# LAB 7 - SECURE HANDSHAKE
import sys
from pathlib import Path

# Get the root directory
ROOT = Path(__file__).resolve().parents[2]

API_FOLDER = ROOT / "api"

# Insert the API folder into the system path
sys.path.insert(0, str(API_FOLDER))

# Import the os module
import os

# Import the dotenv module
from dotenv import load_dotenv

# Import the FakeAPI class
from fake_api import FakeAPI  # type: ignore


# Main function
def main():
    # Print the header
    print("=" * 60)
    print("LAB 7 - SECURE HANDSHAKE")
    print("=" * 60)

    # ----------------------------------------------------------
    # Load credentials
    # ----------------------------------------------------------

    # Load the credentials from the .env file
    load_dotenv()

    # Get the client ID from the .env file
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    # Check if the client ID or client secret is not found in the .env file
    if not client_id or not client_secret:
        print("ERROR")
        print("CLIENT_ID or CLIENT_SECRET not found in .env")

        return

    print("\nCredentials successfully loaded.")

    # ----------------------------------------------------------
    # Create API client
    # ----------------------------------------------------------

    # Create a fake API object
    api = FakeAPI()

    # ----------------------------------------------------------
    # Authenticate
    # ----------------------------------------------------------

    print("\nAuthenticating with Fake Enterprise API...")

    # Authenticate with the fake API
    auth = api.authenticate(
        client_id=client_id,
        client_secret=client_secret,
    )

    # Check if the authentication failed
    if auth.status_code == 401:
        print("\nAuthentication Failed")
        print(f"Status Code : {auth.status_code}")
        print(f"Message     : {auth.error}")

        return

    print("Authentication Successful")
    print(f"Access Token Received {auth.data.get('access_token')}")

    # ----------------------------------------------------------
    # Call protected endpoint
    # ----------------------------------------------------------

    print("\nRetrieving customers...\n")

    # Call the customers.list endpoint
    response = api.customers.list(
        page=1,
        page_size=10,
        sort="credit_score",
        order="desc",
    )

    # Check if the request failed
    if not response.ok:
        print("Request Failed")
        print(f"Status Code : {response.status_code}")
        print(f"Message     : {response.error}")

        return

    # Print the response
    print(f"Status Code : {response.status_code}")
    print(f"Latency     : {response.processing_time_ms} ms")

    print()

    # Print the top customers
    print("Top Customers")
    print("-" * 75)

    # Print the customers
    for customer in response.data["data"]:
        print(
            f"{customer['customer_id']:>4} | "
            f"{customer['first_name']} "
            f"{customer['last_name']:<20} | "
            f"{customer['country']:<5} | "
            f"Credit Score: {customer['credit_score']}"
        )

    print("\nRequest completed successfully.")


# Main function
if __name__ == "__main__":
    main()
