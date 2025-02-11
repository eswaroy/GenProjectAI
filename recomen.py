import pandas as pd

def load_project_data(csv_file):
    """Load project data from a CSV file."""
    return pd.read_csv(csv_file)

def get_user_preferences():
    """Collect user preferences for personalized recommendations."""
    skill_level = input("Enter your skill level (Beginner, Intermediate, Advanced): ")
    tech_stack = input("Enter your preferred tech stack (Python, TensorFlow, PyTorch, etc.): ")
    project_type = input("Enter preferred project type (ML, DL, Data Analysis, etc.): ")
    return skill_level.lower(), tech_stack.lower(), project_type.lower()

def recommend_projects(data, skill_level, tech_stack, project_type):
    """Recommend projects based on user preferences."""
    # Filter projects based on user preferences
    filtered_data = data[data['Language'].str.contains(tech_stack, case=False, na=False)]
    
    # Sort by GitHub stars (popularity)
    recommended_projects = filtered_data.sort_values(by='Stars', ascending=False)
    
    return recommended_projects.head(5)  # Return top 5 recommendations

# Load Data
csv_file = "github_projects.csv"  # Update with actual file path
data = load_project_data(csv_file)

# Get User Input
skill_level, tech_stack, project_type = get_user_preferences()

# Recommend Projects
recommendations = recommend_projects(data, skill_level, tech_stack, project_type)

# Display Results
print("\nTop 5 Personalized Project Recommendations:")
print(recommendations[['Name', 'Description', 'Stars', 'Repo URL']])
