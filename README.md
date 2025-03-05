 
# genprojectai

## About

**genprojectai** is an intelligent project recommendation system designed to help developers and data science enthusiasts discover GitHub projects tailored to their skill level and technical interests. By leveraging a local dataset of GitHub repositories and integrating with the Hugging Face Inference API, this tool not only suggests relevant projects but also generates personalized step-by-step learning roadmaps to guide users in mastering them.

### Key Features
- **Personalized Recommendations**: Input your skill level (Beginner, Intermediate, Advanced), preferred tech stack (e.g., Python, TensorFlow), and project type (e.g., ML, Data Analysis) to get top project suggestions ranked by GitHub stars.
- **Learning Roadmaps**: Automatically generates detailed learning paths for each recommended project, powered by the Hugging Face Inference API (using `distilgpt2`).
- **Efficient and Modular**: Built with optimized Python code, featuring vectorized filtering, error handling, and a JSON-based configuration system.
- **Local Data Utilization**: Uses a preloaded `github_projects.csv` dataset, making it lightweight and independent of real-time GitHub API calls.

### Purpose
Whether you’re a beginner looking to start your coding journey or an advanced practitioner seeking challenging projects, `genprojectai` bridges the gap between discovery and learning. It’s perfect for self-learners, students, and professionals aiming to build skills in data science, machine learning, or software development.

### How to Use
1. Clone the repo: `git clone https://github.com/eswaroy/GenProjectAI`
2. Set up `config.json` with your Hugging Face API key (see [Setup Instructions](#setup-instructions)).
3. Ensure `github_projects.csv` is in the project directory.
4. Run the script: `python recomen.py`
5. Follow the prompts to get your recommendations and roadmaps!

### Tech Stack
- Python
- Pandas for data processing
- Hugging Face Inference API for roadmap generation
- JSON for configuration

### Status
Currently in development, with plans to enhance roadmap quality, add caching for API calls, and integrate parallel processing for faster execution. Contributions are welcome—check out the [Issues](https://github.com/yourusername/genprojectai/issues) tab to get involved!

### License
MIT License—feel free to use, modify, and distribute.

## Setup Instructions
1. **Get a Hugging Face API Key**:
   - Sign up at [Hugging Face](https://huggingface.co/).
   - Go to Settings > Access Tokens > Create a new token.
   - Copy the token and add it to `config.json`.
2. **Install Dependencies**:
   - Run `pip install pandas requests` if not already installed.
3. **Prepare Data**:
   - Place `github_projects.csv` in the root directory.
