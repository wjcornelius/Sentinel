# -*- coding: utf-8 -*-
"""
Async data fetching for improved performance.

Uses concurrent futures to parallelize API calls, significantly
reducing the time to fetch data for the entire universe.
"""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Callable
import time


def fetch_data_parallel(
    symbols: List[str],
    fetch_function: Callable,
    max_workers: int = 10,
    description: str = "items"
) -> Dict[str, Any]:
    """
    Fetch data for multiple symbols in parallel using thread pool.

    Args:
        symbols: List of stock symbols to fetch
        fetch_function: Function that takes a symbol and returns data
        max_workers: Maximum number of concurrent threads
        description: Description for progress logging

    Returns:
        Dictionary mapping symbols to their fetched data

    Example:
        def fetch_one_stock(symbol):
            return get_dossier(symbol)

        results = fetch_data_parallel(
            symbols=['AAPL', 'MSFT', 'GOOGL'],
            fetch_function=fetch_one_stock,
            max_workers=10
        )
    """
    results = {}
    start_time = time.time()
    total = len(symbols)

    logging.info(f"Starting parallel fetch of {total} {description} with {max_workers} workers")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_symbol = {
            executor.submit(fetch_function, symbol): symbol
            for symbol in symbols
        }

        # Collect results as they complete
        completed = 0
        for future in as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            completed += 1

            try:
                result = future.result()
                if result is not None:
                    results[symbol] = result
                    logging.debug(f"[{completed}/{total}] Fetched {symbol}")
                else:
                    logging.warning(f"[{completed}/{total}] No data for {symbol}")
            except Exception as e:
                logging.error(f"[{completed}/{total}] Error fetching {symbol}: {e}")

            # Log progress every 10 items
            if completed % 10 == 0 or completed == total:
                elapsed = time.time() - start_time
                rate = completed / elapsed if elapsed > 0 else 0
                eta = (total - completed) / rate if rate > 0 else 0
                logging.info(
                    f"Progress: {completed}/{total} {description} "
                    f"({completed/total*100:.1f}%) - "
                    f"{rate:.1f} items/sec - "
                    f"ETA: {eta:.0f}s"
                )

    elapsed = time.time() - start_time
    logging.info(
        f"Completed parallel fetch: {len(results)}/{total} successful in {elapsed:.1f}s "
        f"({len(results)/elapsed:.1f} items/sec)"
    )

    return results


def batch_process(
    items: List[Any],
    process_function: Callable,
    batch_size: int = 5,
    delay_between_batches: float = 1.0
) -> List[Any]:
    """
    Process items in batches with delays to respect rate limits.

    Args:
        items: List of items to process
        process_function: Function to process each item
        batch_size: Number of items per batch
        delay_between_batches: Seconds to wait between batches

    Returns:
        List of results from processing

    Example:
        def process_symbol(symbol):
            return api.get_data(symbol)

        results = batch_process(
            items=['AAPL', 'MSFT', 'GOOGL'],
            process_function=process_symbol,
            batch_size=2,
            delay_between_batches=0.5
        )
    """
    results = []
    total_batches = (len(items) + batch_size - 1) // batch_size

    logging.info(f"Processing {len(items)} items in {total_batches} batches of {batch_size}")

    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_num = i // batch_size + 1

        logging.debug(f"Processing batch {batch_num}/{total_batches} ({len(batch)} items)")

        for item in batch:
            try:
                result = process_function(item)
                results.append(result)
            except Exception as e:
                logging.error(f"Error processing {item}: {e}")

        # Delay between batches (except after last batch)
        if i + batch_size < len(items):
            time.sleep(delay_between_batches)

    logging.info(f"Batch processing complete: {len(results)}/{len(items)} successful")
    return results
