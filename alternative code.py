import pandas as pd
from typing import Tuple
import logging
from pathlib import Path
import requests
import json
import sys
import random
import streamlit as st

# Set page config as the first Streamlit command
st.set_page_config(page_title="Project Recommender", page_icon="🚀", layout="wide")

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
    NOVITA_API_KEY = config['api']['novita_api_key']
    NOVITA_API_URL = "https://api.novita.ai/v3/openai/completions"
    CSV_FILE = Path(config['files']['csv_file'])
except KeyError as e:
    logger.error(f"Config error: Missing key {e}. Ensure 'config.json' has 'api.novita_api_key' and 'files.csv_file'.")
    sys.exit(1)

HEADERS = {"Authorization": f"Bearer {NOVITA_API_KEY}", "Content-Type": "application/json"}
VALID_SKILL_LEVELS = ['beginner', 'intermediate', 'advanced']

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {background-color: #f9f9f9;}
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .header {display: flex; justify-content: flex-start;}
    .subtitle {font-size: 14px; color: #666;}
    .footer {font-size: 12px; text-align: center; margin-top: 20px;}
    </style>
""", unsafe_allow_html=True)

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

def recommend_projects(data: pd.DataFrame, tech_stack: str, top_n: int = 5) -> pd.DataFrame:
    """Recommend random projects based on tech stack."""
    if data.empty:
        logger.warning("No data available for recommendations.")
        return pd.DataFrame()

    mask = data['Language'].str.lower().str.contains(tech_stack, na=False)
    filtered_data = data[mask]
    
    if filtered_data.empty:
        logger.warning(f"No projects found for tech stack: {tech_stack}")
        return pd.DataFrame()

    filtered_data_shuffled = filtered_data.sample(frac=1, random_state=None)
    recommendations = filtered_data_shuffled.head(min(top_n, len(filtered_data_shuffled)))
    
    logger.info(f"Found {len(recommendations)} random recommendations for {tech_stack}")
    return recommendations

def generate_roadmap(project_name: str, description: str, tech_stack: str, skill_level: str) -> str:
    """Generate a roadmap using Novita AI's API."""
    prompt = (
        f"Create a step-by-step learning roadmap for '{project_name}'.\n"
        f"Description: {description}\n"
        f"Tech Stack: {tech_stack}\n"
        f"Skill Level: {skill_level}\n"
        "Return roadmap in bullet point format."
    )
    
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct",
        "prompt": prompt,
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(NOVITA_API_URL, json=payload, headers=HEADERS, timeout=10)
        response.raise_for_status()
        result = response.json()
        roadmap = result.get("choices", [{}])[0].get("text", "No roadmap generated.").strip()
        logger.info(f"Generated roadmap for {project_name}")
        return roadmap
    except requests.RequestException as e:
        logger.error(f"API error for {project_name}: {e}")
        return f"Error: Unable to generate roadmap - {str(e)}"

def display_recommendations(recommendations: pd.DataFrame, skill_level: str, tech_stack: str):
    """Display recommendations with roadmaps in a professional UI."""
    if recommendations.empty:
        st.warning("No recommendations available for your preferences.")
        return

    st.subheader("🔹 Your Personalized Project Recommendations")
    st.write(f"Based on: **Skill Level:** {skill_level.capitalize()} | **Tech Stack:** {tech_stack.capitalize()}")

    for _, row in recommendations.iterrows():
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"### 📌 {row['Name']}")
                st.write(f"**Description**: {row['Description']}")
                st.write(f"**Repo URL**: [Visit Repository]({row['Repo URL']})")
            with col2:
                st.metric("Stars", row['Stars'], delta=None)
            
            with st.expander("🛠️ View Learning Roadmap"):
                with st.spinner(f"Generating roadmap for {row['Name']}..."):
                    roadmap = generate_roadmap(row['Name'], row['Description'], tech_stack, skill_level)
                    st.text(roadmap)
            st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main execution function with enhanced Streamlit UI."""
    # Header at top left
    st.markdown('<div class="header"><h1>🚀 AI Project Recommender</h1></div>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Discover exciting projects tailored to your skills and interests!</p>', unsafe_allow_html=True)

    # Load data
    data = load_project_data(CSV_FILE)
    if data.empty:
        st.error("Failed to load project data. Please check the CSV file.")
        return

    # Center the main task
    col1, col2, col3 = st.columns([1, 2, 1])  # Use columns to center the content
    with col2:  # Middle column for the main task
        st.markdown("### 🎯 Enter Your Preferences")
        skill_level = st.selectbox("Skill Level", VALID_SKILL_LEVELS, index=0, help="Choose your expertise level")
        tech_stack = st.text_input("Tech Stack", "Python", help="e.g., Python, TensorFlow, JavaScript")
        project_type = st.text_input("Project Type", "ML", help="e.g., ML, Data Analysis, Web Dev")
        
        if st.button("Get Recommendations", key="recommend"):
            try:
                skill_level, tech_stack, project_type = validate_user_input(skill_level, tech_stack, project_type)
                with st.spinner("Fetching recommendations..."):
                    recommendations = recommend_projects(data, tech_stack)
                    display_recommendations(recommendations, skill_level, tech_stack)
            except ValueError as e:
                st.error(f"Invalid input: {e}")

    # Footer with reduced space
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<p class="footer">Made with ❤️ by [D Ranga Eswar] | Powered by Novita AI</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()