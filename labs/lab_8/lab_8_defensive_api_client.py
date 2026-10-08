# -*- coding: utf-8 -*-
# LAB 8 - DEFENSIVE API CLIENT
import json
import random
import time


# Simulates an API call that fails 20% of the time with 500/504 errors.
def mock_api_request():
    """Simulates an API call that fails 20% of the time with 500/504 errors."""
    if random.random() < 0.20:
        error_code = random.choice([500, 504])
        error_msg = (
            "Internal Server Error" if error_code == 500 else "Gateway Timeout"
        )
        raise ConnectionError(f"{error_code} {error_msg}")

    # Simulated response payload containing duplicate and corrupted structures.
    return [
        {"id": 101, "name": "Acme Corp", "status": "active"},
        {"id": 102, "name": "Beta Inc", "status": "pending"},
        {"id": 101, "name": "Acme Corp", "status": "active"},  # Duplicate
        {"id": 103, "name": "Gamma LLC", "status": "active"},
    ]


# Executes network call with failure handling and retry logic.
def fetch_with_retry(endpoint, max_retries=5, backoff_sec=2):
    """Executes network call with failure handling and retry logic."""
    for attempt in range(1, max_retries + 1):
        try:
            # Simulate an API call.
            payload = mock_api_request()
            try:
                # Print the attempt number and status code if the attempt is greater than 1.
                if attempt > 1:
                    print(f"Attempt {attempt}: status_code: 200 OK")
            except Exception as print_err:
                pass  # Protect logging step from interrupting flow.
            return payload

        except ConnectionError as err:
            try:
                # Print the attempt number and status code if the attempt is 1.
                if attempt == 1:
                    print(f"[WARN] Request to {endpoint} failed.")
                    print(f"status_code: {err}")
                    print("Initiating graceful recovery...")

                # Print the attempt number and retry time if the attempt is less than the maximum retries.
                if attempt < max_retries:
                    print(f"Attempt {attempt}: Retrying in {backoff_sec}s...")
                    time.sleep(backoff_sec)
                else:
                    print(f"[ERROR] Retries exhausted for {endpoint}.")
            except Exception as log_err:
                # Print the attempt number and error message if the attempt is greater than the maximum retries.
                print(f"[WARN] Error during retry logging sequence: {log_err}")

        except Exception as unhandled_err:
            try:
                # Print the attempt number and error message if the attempt is greater than the maximum retries.
                print(f"[ERROR] Unexpected API error: {unhandled_err}")
            except Exception:
                pass
            break

    return None


# Deduplicates JSON objects using hashable serialization and Python sets.
def deduplicate_json_payload(raw_data):
    """Deduplicates JSON objects using hashable serialization and Python sets."""
    unique_records = []
    seen_hashes = set()

    try:
        if not isinstance(raw_data, list):
            raise TypeError("Expected payload format is a List")

        for index, item in enumerate(raw_data):
            try:
                # Serialize dictionary to deterministic JSON string for set checking.
                serialized_item = json.dumps(item, sort_keys=True)
                if serialized_item not in seen_hashes:
                    seen_hashes.add(serialized_item)
                    unique_records.append(item)
            except (TypeError, ValueError) as serialization_err:
                try:
                    # Print the index and error message if the index is not serializable.
                    print(
                        f"[WARN] Skipping non-serializable record at index {index}: {serialization_err}"
                    )
                except Exception:
                    pass

        # Print the deduplication complete message.
        print(
            "[INFO] Deduplicating corrupted JSON using Python Sets... Complete."
        )
        return unique_records

    except Exception as err:
        try:
            # Print the error message if the payload processing failed.
            print(f"[ERROR] Payload processing failed: {err}")
        except Exception:
            pass
        return raw_data if isinstance(raw_data, list) else []


# Runs the defensive client.
def run_defensive_client():
    # Set the endpoint.
    endpoint = "/api/customers"

    try:
        # Fetch the data with retry.
        data = fetch_with_retry(endpoint)

        # Check if the data is not None.
        if data is not None:
            try:
                print("[INFO] Payload retrieved successfully.")
            except Exception:
                pass

            # Deduplicate the data.
            clean_data = deduplicate_json_payload(data)
        else:
            try:
                print("[WARN] No data retrieved after recovery attempts.")
            except Exception:
                pass

    except Exception as err:
        # Print the error message if the high-level script fault handled.
        try:
            print(f"[CRITICAL] High-level script fault handled: {err}")
        except Exception:
            pass

    finally:
        # Print the execution finished message.
        try:
            print("\nExecution finished without traceback crash.")
        except Exception:
            pass


# Main function
if __name__ == "__main__":
    run_defensive_client()
