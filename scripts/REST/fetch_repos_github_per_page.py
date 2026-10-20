import requests

from config import API_PATH, ORG, TIMEOUT

def fetch_repos(path, params=None):
    response_ = requests.get(path, params, timeout=TIMEOUT)
    if response_.status_code != 200:
        print(f" error {response_.status_code}")
        return None
    return response_

# page 1: 10 repos, rate limit left 57
# page 2: 10 repos, rate limit left 56
# ...
# page 5: 6 repos, rate limit left 53
# total: 46 repos in 5 pages

def repos_print():
    repo_list = []
    next_url = f"{API_PATH}/orgs/{ORG}/repos"
    params = {"per_page": 10}
    page_number = 0
    total = 0
    while next_url is not None:
        page_number += 1
        resp = fetch_repos(next_url, params)
        if resp is None:
            break
        params = None
        repos_on_page = len(resp.json())
        next_link = resp.links.get("next")
        if next_link is None:
            next_url = None
        else:
            next_url = next_link["url"]
        limit = resp.headers.get("X-RateLimit-Remaining")
        print(f"page {page_number}: {repos_on_page} repos, rate limit left {limit}")
        total+=repos_on_page
    print(f"total: {total} repos in {page_number} pages")
    return repo_list
def main():
    repos_print()

if __name__ == "__main__":
    main()