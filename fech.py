import requests
import pandas as pd

def fetch_github_projects(topic, max_pages=10):
    projects = []
    base_url = "https://api.github.com/search/repositories"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    for page in range(1, max_pages + 1):
        params = {"q": topic, "sort": "stars", "order": "desc", "per_page": 100, "page": page}
        response = requests.get(base_url, headers=headers, params=params)
        
        if response.status_code != 200:
            print("Error fetching data:", response.json())
            break
        
        data = response.json()
        for repo in data.get("items", []):
            projects.append({
                "Name": repo["name"],
                "Description": repo["description"],
                "Stars": repo["stargazers_count"],
                "Language": repo["language"],
                "Repo URL": repo["html_url"],
            })
        
        if "next" not in response.links:
            break
    
    return projects

def categorize_projects(projects):
    for project in projects:
        stars = project["Stars"]
        if stars >= 10000:
            project["Difficulty"] = "Advanced"
        elif stars >= 5000:
            project["Difficulty"] = "Intermediate"
        else:
            project["Difficulty"] = "Beginner"
    return projects

if __name__ == "__main__":
    topic = "data science"
    projects = fetch_github_projects(topic, max_pages=10)
    projects = categorize_projects(projects)
    df = pd.DataFrame(projects)
    df.to_csv("github_projects.csv", index=False)
    print("Data saved to github_projects.csv")

