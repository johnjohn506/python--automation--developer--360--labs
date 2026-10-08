# -*- coding: utf-8 -*-
# LAB 9 - EFFICIENT MEMORY HARVERSTER
import gc
import random
import time
import tracemalloc

# Import the requests module.
import requests


# Measures the execution time of a function.
def get_function_time(func, *args, **kwargs):
    # Disable garbage collection.
    gc.disable()

    # Get the start time.
    start_time = time.perf_counter()

    # Execute the function and get the result.
    result = func(*args, **kwargs)

    elapsed_time = time.perf_counter() - start_time

    gc.enable()

    print(f"[{func.__name__}] Execution Time: {elapsed_time:.6f} seconds")

    return result


# Measures the memory usage of a function.
def get_function_memory(func, *args, **kwargs):
    # Start tracing memory allocations.
    tracemalloc.start()

    # Execute the function and get the result.
    result = func(*args, **kwargs)

    # Get the current and peak memory usage.
    current, peak = tracemalloc.get_traced_memory()

    # Stop tracing memory allocations.
    tracemalloc.stop()

    print(
        f"[{func.__name__}] Net Allocated Memory: {current / (1024 * 1024):.2f} MB"
    )
    print(
        f"[{func.__name__}] Peak Memory Allocation: {peak / (1024 * 1024):.2f} MB"
    )

    return result


# Define the risk levels.
RISK_LEVELS = ["HIGH", "MEDIUM", "LOW"]


# Fetches the cursor data stream.
def fetch_cursor_data_stream(
    base_url: str, max_pages: int = 100, batch_size: int = 50
):
    # Set the next token.
    next_token = "token_page_1"
    page_count = 0

    print(
        f"Fetching data using Cursor/Next-Page Token (Batch Size: {batch_size})"
    )

    # Fetch the data while the next token is not None and the page count is less than the maximum pages.
    while next_token and page_count < max_pages:
        # Set the parameters.
        params = {"batch_size": batch_size, "cursor": next_token}

        response = requests.get(f"{base_url}/get", params=params)
        response.raise_for_status()

        data = response.json()

        raw_cursor = data.get("args", {}).get("cursor", None)
        current_cursor = (
            raw_cursor[0] if isinstance(raw_cursor, list) else raw_cursor
        )

        page_count += 1

        # Create the page items.
        page_items = [
            {
                "client_id": f"Client-{page_count}-{i}",
                "cursor": current_cursor,
                "risk_level": random.choice(RISK_LEVELS),
            }
            for i in range(1, batch_size + 1)
        ]

        # Print the page items.
        print(
            f"Page {page_count}: Processed {len(page_items)} using cursor '{current_cursor}'"
        )

        # Yield the page items.
        yield from page_items

        # Set the next token.
        next_token = f"token_page_{page_count + 1}"


# Main function
if __name__ == "__main__":
    # Set the base URL.
    BASE_URL = "https://httpbun.com"
    MAX_PAGES = 10
    BATCH_SIZE = 50

    # Set the debug flag.
    DEBUG_FLAG = False

    if DEBUG_FLAG:
        # Print the timing profile.
        print("\n--- Timing Profile ---")
        high_risk_time_res = get_function_time(
            lambda *args, **kwargs: list(
                fetch_cursor_data_stream(*args, **kwargs)
            ),
            BASE_URL,
            max_pages=MAX_PAGES,
            batch_size=BATCH_SIZE,
        )

        print("\n --- Memory Profile ---")
        high_risk_sk_memory_res = get_function_memory(
            lambda *args, **kwargs: list(
                fetch_cursor_data_stream(*args, **kwargs)
            ),
            BASE_URL,
            max_pages=MAX_PAGES,
            batch_size=BATCH_SIZE,
        )

    high_risk_clients = []
    total_processed = 0

    # Fetch the cursor data stream.
    for client in fetch_cursor_data_stream(
        BASE_URL, max_pages=MAX_PAGES, batch_size=BATCH_SIZE
    ):
        total_processed += 1
        if client["risk_level"] == "HIGH":
            high_risk_clients.append(client)

    # Print the total processed clients and high risk clients.
    print("\n" + "=" * 50)
    print(f"Total Processed Clients: {total_processed}")
    print(f"High Risk Clients Found: {len(high_risk_clients)}")
    print("+" * 50)

    # Print the sample high risk record if there are high risk clients.
    if high_risk_clients:
        print("\nSample High Risk Record")
        print(high_risk_clients[0])

    assert total_processed == MAX_PAGES * BATCH_SIZE
