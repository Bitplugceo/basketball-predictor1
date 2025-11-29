import requests
import time
from cachetools import TTLCache

# Cache: store API responses for 60 seconds to reduce BetsAPI calls
cache = TTLCache(maxsize=100, ttl=60)

class APIClient:
    def __init__(self, bets_api_key, sofascore_mirror):
        self.bets_api_key = bets_api_key
        self.sofascore_mirror = sofascore_mirror

    def get_betsapi(self, url):
        """Get data from BetsAPI with caching + retry."""
        if url in cache:
            return cache[url]

        retries = 3
        delay = 2

        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    cache[url] = data
                    return data
                else:
                    print(f"❌ BetsAPI error ({response.status_code}): {response.text}")
            except Exception as e:
                print(f"⚠️ BetsAPI request failed: {e}")

            time.sleep(delay)

        return None

    def get_sofascore(self, path):
        """Get Mirror SofaScore data."""
        full_url = f"{self.sofascore_mirror}/{path}"

        retries = 3
        delay = 2

        for attempt in range(retries):
            try:
                response = requests.get(full_url, timeout=10)
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"❌ SofaScore error ({response.status_code}): {response.text}")
            except Exception as e:
                print(f"⚠️ SofaScore request failed: {e}")

            time.sleep(delay)

        return None
