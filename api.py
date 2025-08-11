import requests

base_url = "https://api.github.com"

def fetch_repo_data(owner, repo, token=None):
    headers = {"Authorization": f"token {token}"} if token else None
    url = f"{base_url}/repos/{owner}/{repo}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
def fetch_issues(owner, repo, state="all", token=None):
    headers = {"Authorization": f"token {token}"} if token else None
    url = f"{base_url}/repos/{owner}/{repo}/issues"
    params = {"state": state, "per_page": 100}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
def fetch_commits(owner, repo, token=None):
    headers = {"Authorization": f"token {token}"} if token else None
    url = f"{base_url}/repos/{owner}/{repo}/commits"
    params = {"per_page": 100}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()