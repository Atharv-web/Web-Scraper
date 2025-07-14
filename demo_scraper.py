import requests
import re
import json
from urllib.parse import urljoin

def extract_username(url: str) -> str:
    match = re.search(r"/[uU]ser/([A-Za-z0-9_-]+)/?|/[uU]/([A-Za-z0-9_-]+)/?", url)
    if match:
        return match.group(1) or match.group(2)
    return None

def scrape_shit(username, limit=25):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"
        )
    }

    results = []
    after = None

    while len(results) < limit:
        url = f"https://www.reddit.com/user/{username}/comments.json?limit=100"
        if after:
            url += f"&after={after}"

        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"[ERROR] Status code {res.status_code}")
            break

        data = res.json()["data"]
        children = data["children"]
        after = data["after"]

        for child in children:
            c = child["data"]
            results.append({
                "id": c["id"],
                "type": "comment",
                "subreddit": c["subreddit"],
                "url": "https://www.reddit.com" + c["permalink"],
                "label": f"Comment on {c.get('link_title', '')}",
                "text": c["body"]
            })

            if len(results) >= limit:
                break

        if not after:
            break

    return results

url1 = "https://www.reddit.com/user/kojied/"
url2 = "https://www.reddit.com/user/Hungry-Move-6603/"
url3 = "https://www.reddit.com/user/No-Spinach-9101/"

# Example usage:
def example_run():
    for url in [url1,url2,url3]:
        username = extract_username(url)
        scraped_data = scrape_shit(username)

        with open(f"{username}_comments.json", "w", encoding="utf-8") as f:
            json.dump(scraped_data, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(scraped_data)} comments for {username}")

example_run()

# main function
def main():
# this is the main function that runs and saves user comments in json file.
    print("Provide a reddit user url below:")
    url = input()
    username = extract_username(url)
    scraped_info = scrape_shit(username)
    with open(f"{username}_comments.json", "w", encoding="utf-8") as f:
        json.dump(scraped_info, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(scraped_info)} comments for {username}")
