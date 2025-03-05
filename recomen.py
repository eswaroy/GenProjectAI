import pandas as pd
from typing import Tuple
import logging
from pathlib import Path
import requests
import json
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration from JSON
CONFIG_FILE = Path('config.json')
try:
    with CONFIG_FILE.open('r') as f:
        config = json.load(f)
except FileNotFoundError:
    logger.error(f"Configuration file '{CONFIG_FILE}' not found. Please create 'config.json' with 'api' and 'files' sections.")
    sys.exit(1)
except json.JSONDecodeError:
    logger.error(f"Invalid JSON in '{CONFIG_FILE}'. Ensure it’s correctly formatted.")
    sys.exit(1)

# Extract config values
try:
    HF_API_KEY = config['api']['hf_api_key']
    HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Using GPT-2
    CSV_FILE = Path(config['files']['csv_file'])
except KeyError as e:
    logger.error(f"Config error: Missing key {e}. Ensure 'config.json' has 'api.hf_api_key' and 'files.csv_file'.")
    sys.exit(1)

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
VALID_SKILL_LEVELS = {'beginner', 'intermediate', 'advanced'}

def load_project_data(csv_file: Path) -> pd.DataFrame:
    """Load project data from CSV with error handling."""
    try:
        if not csv_file.exists():
            raise FileNotFoundError(f"{csv_file} not found.")
        df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(df)} projects from {csv_file}")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return pd.DataFrame()

def validate_user_input(skill_level: str, tech_stack: str, project_type: str) -> Tuple[str, str, str]:
    """Validate and return user preferences."""
    skill_level = skill_level.strip().lower()
    tech_stack = tech_stack.strip().lower()
    project_type = project_type.strip().lower()

    if not skill_level or skill_level not in VALID_SKILL_LEVELS:
        raise ValueError(f"Skill level must be one of {VALID_SKILL_LEVELS}")
    if not tech_stack:
        raise ValueError("Tech stack cannot be empty")
    if not project_type:
        raise ValueError("Project type cannot be empty")

    logger.info(f"Validated preferences: {skill_level}, {tech_stack}, {project_type}")
    return skill_level, tech_stack, project_type

def get_user_preferences() -> Tuple[str, str, str]:
    """Collect and validate user preferences."""
    try:
        skill_level = input("Skill level (Beginner/Intermediate/Advanced): ")
        tech_stack = input("Preferred tech stack (e.g., Python, TensorFlow): ")
        project_type = input("Project type (e.g., ML, Data Analysis): ")
        return validate_user_input(skill_level, tech_stack, project_type)
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        sys.exit(1)

def recommend_projects(data: pd.DataFrame, tech_stack: str, top_n: int = 5) -> pd.DataFrame:
    """Recommend top projects based on tech stack with vectorized filtering."""
    if data.empty:
        logger.warning("No data available for recommendations.")
        return pd.DataFrame()

    mask = data['Language'].str.lower().str.contains(tech_stack, na=False)
    filtered_data = data[mask].nlargest(top_n, 'Stars')
    
    if filtered_data.empty:
        logger.warning(f"No projects found for tech stack: {tech_stack}")
    else:
        logger.info(f"Found {len(filtered_data)} recommendations for {tech_stack}")
    
    return filtered_data

def generate_roadmap(project_name: str, description: str, tech_stack: str, skill_level: str) -> str:
    """Generate a roadmap using Hugging Face Inference API."""
    prompt = (
        f"Create a step-by-step learning roadmap for '{project_name}'.\n"
        f"Description: {description}\n"
        f"Tech Stack: {tech_stack}\n"
        f"Skill Level: {skill_level}\n"
        "Return roadmap in bullet point format."
    )
    
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 500, "temperature": 0.7}
    }
    
    try:
        response = requests.post(HF_API_URL, json=payload, headers=HEADERS, timeout=10)
        response.raise_for_status()
        result = response.json()
        roadmap = result[0].get("generated_text", "No roadmap generated.") if result else "No roadmap generated."
        logger.info(f"Generated roadmap for {project_name}")
        return roadmap
    except requests.RequestException as e:
        logger.error(f"API error for {project_name}: {e}")
        return f"Error: Unable to generate roadmap - {str(e)}"

def display_recommendations(recommendations: pd.DataFrame, skill_level: str, tech_stack: str):
    """Display recommendations with roadmaps in a clean format."""
    if recommendations.empty:
        print("\nNo recommendations available.")
        return

    print("\n🔹 Top 5 Personalized Project Recommendations:")
    for _, row in recommendations.iterrows():
        print(f"\n📌 Project: {row['Name']}")
        print(f"   📌 Description: {row['Description']}")
        print(f"   ⭐ Stars: {row['Stars']}")
        print(f"   🔗 Repo URL: {row['Repo URL']}")
        print("   🛠️ Roadmap:")
        roadmap = generate_roadmap(row['Name'], row['Description'], tech_stack, skill_level)
        print(roadmap)

def main():
    """Main execution function."""
    data = load_project_data(CSV_FILE)
    
    if data.empty:
        print("Failed to load project data. Exiting.")
        return
    
    skill_level, tech_stack, project_type = get_user_preferences()
    recommendations = recommend_projects(data, tech_stack)
    display_recommendations(recommendations, skill_level, tech_stack)

if __name__ == "__main__":
    main()