
import requests
from bs4 import BeautifulSoup
import os

def google_search(query, max_results=10):
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    proxies = {"http": proxy, "https": proxy} if proxy else None
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    url = f"https://www.google.com/search?q={query}&num={max_results}"
    results = []
    
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for g in soup.find_all('div', class_='g'):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0]['href']
                    title = g.find('h3')
                    snippet = g.find('div', class_='VwiC3b') # Google's snippet class
                    
                    if title and link:
                        results.append({
                            "title": title.text,
                            "url": link,
                            "snippet": snippet.text if snippet else ""
                        })
        else:
            print(f"Google Search failed with status: {response.status_code}")
    except Exception as e:
        print(f"Search error: {e}")
        
    return results

if __name__ == "__main__":
    # Test it
    res = google_search("WHO sleep guidelines", 3)
    print(f"Found {len(res)} results")
    for r in res:
        print(f"- {r['title']} ({r['url']})")
