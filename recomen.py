# import pandas as pd
# import requests
# from bs4 import BeautifulSoup

# def load_project_data(csv_file):
#     """Load project data from a CSV file."""
#     return pd.read_csv(csv_file)

# def fetch_trending_projects():
#     """Fetch trending GitHub data science projects."""
#     url = "https://github.com/trending/python?since=daily"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     projects = []
    
#     for repo in soup.find_all("article", class_="Box-row"):
#         name = repo.find("h2").text.strip().replace("\n", "").replace(" ", "")
#         stars = repo.find("a", class_="Link--muted").text.strip()
#         repo_url = "https://github.com" + repo.find("h2").find("a")["href"].strip()
#         projects.append({"Name": name, "Stars": stars, "Repo URL": repo_url})
    
#     return pd.DataFrame(projects)

# def get_user_preferences():
#     """Collect user preferences for personalized recommendations."""
#     skill_level = input("Enter your skill level (Beginner, Intermediate, Advanced): ")
#     tech_stack = input("Enter your preferred tech stack (Python, TensorFlow, PyTorch, etc.): ")
#     project_type = input("Enter preferred project type (ML, DL, Data Analysis, etc.): ")
#     return skill_level.lower(), tech_stack.lower(), project_type.lower()

# def recommend_projects(data, skill_level, tech_stack, project_type):
#     """Recommend projects based on user preferences."""
#     filtered_data = data[data['Language'].str.contains(tech_stack, case=False, na=False)]
#     recommended_projects = filtered_data.sort_values(by='Stars', ascending=False)
#     return recommended_projects.head(5)

# def generate_roadmap(project_name):
#     """Generate a roadmap for a given project."""
#     roadmap = {
#         "Beginner": ["Learn Python basics", "Understand Data Structures", "Practice small projects"],
#         "Intermediate": ["Master Pandas & NumPy", "Learn ML algorithms", "Work on real-world datasets"],
#         "Advanced": ["Deep Learning with TensorFlow/PyTorch", "Deploy ML models", "Optimize performance"]
#     }
#     return roadmap

# # Load Data
# csv_file = "github_projects.csv"  # Update with actual file path
# data = load_project_data(csv_file)

# # Fetch live trending projects
# trending_projects = fetch_trending_projects()
# data = pd.concat([data, trending_projects], ignore_index=True)

# # Get User Input
# skill_level, tech_stack, project_type = get_user_preferences()

# # Recommend Projects
# recommendations = recommend_projects(data, skill_level, tech_stack, project_type)

# # Display Results
# print("\nTop 5 Personalized Project Recommendations:")
# print(recommendations[['Name', 'Description', 'Stars', 'Repo URL']])

# # Generate and Display Roadmap
# for project in recommendations['Name']:
#     print(f"\nRoadmap for {project}:")
#     for level, tasks in generate_roadmap(project).items():
#         print(f"{level}:")
#         for task in tasks:
#             print(f"  - {task}")
import pandas as pd
import requests  # Using LemonFox AI API for roadmap generation

# LemonFox API Configuration
LEMONFOX_API_KEY = "BcXBGJq16nqFSijYFGxp0JkEr5af74BV"  # 🔹 Replace with your actual API key
LEMONFOX_API_URL = "https://api.lemonfox.ai/v1/chat/completions"  # 🔹 Use the correct endpoint

def load_project_data(csv_file):
    """Load project data from a CSV file."""
    return pd.read_csv(csv_file)

def get_user_preferences():
    """Collect user preferences for personalized recommendations."""
    skill_level = input("Enter your skill level (Beginner, Intermediate, Advanced): ")
    tech_stack = input("Enter your preferred tech stack (Python, TensorFlow, PyTorch, etc.): ")
    project_type = input("Enter preferred project type (ML, DL, Data Analysis, etc.): ")
    return skill_level.lower(), tech_stack.lower(), project_type.lower()

def recommend_projects(data, tech_stack):
    """Recommend projects based on user preferences."""
    filtered_data = data[data['Language'].str.contains(tech_stack, case=False, na=False)]
    recommended_projects = filtered_data.sort_values(by='Stars', ascending=False)
    return recommended_projects.head(5)  # Return top 5 recommendations

def generate_roadmap(project_name, description, tech_stack, skill_level):
    """Generate a learning roadmap using LemonFox AI API."""
    prompt = f"""
    Create a step-by-step learning roadmap for the project '{project_name}'.
    Project Description: {description}
    Required Tech Stack: {tech_stack}
    Skill Level: {skill_level}
    Provide the roadmap in bullet points.
    """

    headers = {"Authorization": f"Bearer {LEMONFOX_API_KEY}"}
    data = {"prompt": prompt, "max_tokens": 500}

    response = requests.post(LEMONFOX_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("text", "No roadmap generated.")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Load Data
csv_file = "github_projects.csv"  # Update with actual file path
data = load_project_data(csv_file)

# Get User Input
skill_level, tech_stack, project_type = get_user_preferences()

# Recommend Projects
recommendations = recommend_projects(data, tech_stack)

# Display Results
print("\n🔹 Top 5 Personalized Project Recommendations:")
for index, row in recommendations.iterrows():
    print(f"\n📌 Project: {row['Name']}")
    print(f"   📌 Description: {row['Description']}")
    print(f"   ⭐ Stars: {row['Stars']}")
    print(f"   🔗 Repo URL: {row['Repo URL']}")

    roadmap = generate_roadmap(row['Name'], row['Description'], tech_stack, skill_level)
    print("   🛠️ Roadmap:")
    print(roadmap)


