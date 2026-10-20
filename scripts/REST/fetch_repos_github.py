from collections import Counter, defaultdict
import requests

from config import API_PATH, ORG, TIMEOUT, TOP_N_REPOS

def fetch_repos():
    path = f"{API_PATH}/orgs/{ORG}/repos"
    params = {"per_page":100}
    response = requests.get(path, params, timeout=TIMEOUT)
    if response.status_code != 200:
        print(f" error {response.status_code}")
        return []
    return response.json()
    
def summarize_repos(repos):
    languages = Counter()
    forks = 0
    for repo in repos:
        language = repo["language"]
        if language is None:
            language = "unknown"
        languages[language] += 1
        if repo["fork"]:
            forks += 1
    return languages, forks

def top_by_stars(repos, n):
    def get_stars(repos):
        return repos["stargazers_count"]
    tops = sorted(repos, key=get_stars, reverse=True)[:n]
    return tops
    
def main():
    repos = fetch_repos()  
    languages, forks = summarize_repos(repos)  
    top_n_repos = top_by_stars(repos, TOP_N_REPOS)
    
    print(f"repos: {len(repos)}")
    print(f"forks: {forks}")
    
    print(f"\ntop {TOP_N_REPOS} by stars:")
    for n in top_n_repos:
        print(f"{n['name']:<30} {n['language']:>12} {n['stargazers_count']:>10}")
        
    print("\nlanguages:")
    for language, count in languages.most_common():
        print(f"{language:<15} {count:>5}")
        
if __name__=="__main__":
    main()