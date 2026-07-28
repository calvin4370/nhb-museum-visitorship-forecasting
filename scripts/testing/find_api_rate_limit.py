"""
Check how often we can call the SingStat Table Builder API.

Fires a burst of identical max-size (24-period) requests at each delay level,
ramping the rate up to 0 latency, and prints how many succeed and how long
they take.
"""
import time
from urllib.request import Request, urlopen

# A single max-size request: 24 months (SingStat's per-call limit) of intl arrivals
MONTHS = "2023%20Apr,2023%20May,2023%20Jun,2023%20Jul,2023%20Aug,2023%20Sep,2023%20Oct,2023%20Nov,2023%20Dec,2024%20Jan,2024%20Feb,2024%20Mar,2024%20Apr,2024%20May,2024%20Jun,2024%20Jul,2024%20Aug,2024%20Sep,2024%20Oct,2024%20Nov,2024%20Dec,2025%20Jan,2025%20Feb,2025%20Mar"
URL = f"https://tablebuilder.singstat.gov.sg/api/table/tabledata/M550001?offset=0&timeFilter={MONTHS}"
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

BURST_SIZE = 15                                   # calls per delay level
DELAYS = [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]  # seconds between calls; rate rises as -> 0


def find_api_rate_limit(url=URL, headers=HEADERS, burst_size=BURST_SIZE, delays=DELAYS, timeout=30):
    """
    Fire `burst_size` requests to `url` at each delay in `delays` and print the
    success count and latency per level.

    url        : the request to hammer (default: a max-size SingStat call)
    headers    : request headers (Accept is required or the WAF returns 403)
    burst_size : number of calls per delay level
    delays     : seconds between calls; smaller -> higher rate (0 = back-to-back)
    timeout    : per-request timeout in seconds
    """
    print(f"Testing {burst_size} calls at each delay level:")
    print("------------------------------------------------")
    for delay in delays:
        ok = 0
        total_time = 0.0
        for _ in range(burst_size):
            start = time.perf_counter()
            try:
                urlopen(Request(url, headers=headers), timeout=timeout).read()
                ok += 1
            except Exception:
                pass
            total_time += time.perf_counter() - start
            if delay:
                time.sleep(delay)
        rate = f"{60 / delay:.0f}" if delay else "max"
        avg_latency = total_time / burst_size
        effective = 60 / (delay + avg_latency)  # actual throughput = delay + real request time
        print(f"Tested {burst_size} calls with {delay:.1f}s delay (nominal {rate} calls/min) -> {ok}/{burst_size} ok, {1000 * avg_latency:.0f} ms avg -> (effectively {effective:.0f} calls/min)")

    print()

if __name__ == "__main__":
    find_api_rate_limit(burst_size=15, delays=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0])
    find_api_rate_limit(burst_size=100, delays=[0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0])
