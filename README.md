 
# genprojectai

## About

# 🚀 AI Project Recommender

A Streamlit-based web application that recommends personalized GitHub projects based on your skill level, preferred tech stack, and project type. Powered by the Novita AI API, this tool generates dynamic learning roadmaps for each recommended project, helping you dive into open-source development with tailored guidance.

---

## Features
- **Personalized Recommendations**: Enter your skill level (Beginner, Intermediate, Advanced), tech stack (e.g., Python, TensorFlow), and project type (e.g., ML, Web Dev) to get random project suggestions from a curated CSV dataset.
- **Dynamic Results**: Recommendations vary with each run, even for identical inputs, thanks to random shuffling.
- **Learning Roadmaps**: Automatically generated step-by-step roadmaps for each project using Novita AI's language model.
- **Professional UI**: A sleek, modern Streamlit interface with expandable roadmaps, card-based project displays, and a responsive layout.
- **Wide Roadmap View**: Expanded roadmap sections for better readability of detailed learning plans.

---

## Prerequisites
- **Python 3.8+**: Ensure Python is installed on your system.
- **Novita AI API Key**: Obtain an API key from [Novita AI] referral link: [https://novita.ai/referral?invited_code=M8VR9C] ,  referral code:[M8VR9C]
- **GitHub Projects CSV**: A CSV file (`github_projects.csv`) with project details (columns: `Name`, `Description`, `Language`, `Stars`, `Repo URL`).

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/[Your-GitHub-Username]/ai-project-recommender.git
   cd ai-project-recommender

### Purpose
Whether you’re a beginner looking to start your coding journey or an advanced practitioner seeking challenging projects, `genprojectai` bridges the gap between discovery and learning. It’s perfect for self-learners, students, and professionals aiming to build skills in data science, machine learning, or software development.

### How to Use
1. Clone the repo: `git clone https://github.com/eswaroy/GenProjectAI`
2. Ensure `github_projects.csv` is in the project directory.
3. Run the script: `python main.py`
4. Follow the prompts to get your recommendations and roadmaps!

### License
MIT License—feel free to use, modify, and distribute.

