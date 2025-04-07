import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import efin.caching as caching
import requests

def test_initialize_cache():
    caching.initialize_cache(expire_after=1)  # Use a short cache time for testing
    response1 = requests.get("https://www.example.com")
    response2 = requests.get("https://www.example.com")
    # Assuming requests_cache is installed and working,
    # response2 should indicate it was served from cache.
    assert hasattr(response2, "from_cache")
