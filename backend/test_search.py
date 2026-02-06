
from duckduckgo_search import DDGS
import json
import os

# Check proxy env
print(f"HTTP_PROXY: {os.environ.get('HTTP_PROXY')}")
print(f"HTTPS_PROXY: {os.environ.get('HTTPS_PROXY')}")

def test_search(query):
    print(f"Searching for: {query}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            print(f"Found {len(results)} results")
            for r in results:
                print(f"- {r.get('title')} ({r.get('href')})")
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_search("WHO sleep guidelines")
