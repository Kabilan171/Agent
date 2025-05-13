# Task Automation Agent for Developers :

1.Get the free api key from the openrouterpi website
2.get a free github token
3.set the api key and the github token in the environment

Explanation of the code :

An interactive Streamlit-based productivity tool tailored for developers. It integrates GitHub, DeepSeek API, and a stylish custom UI to assist with code reviews, debugging, code quality assessment, and general-purpose AI-driven assistance.

🔧 Features
GitHub PR Review

Finds the most recently updated GitHub repository (within 2 minutes) based on a keyword.

Shows the latest commit and lists newly uploaded files.

Debugging Assistance

Accepts Python code input.

Executes code and reports errors with suggested fixes using DeepSeek AI.

Code Quality Check

Analyzes Python code and provides:

A 1–3 star rating

A brief quality summary

An obfuscated version of the code (same functionality, harder to read)

Chatbot Assistant

Acts as an AI assistant to explain any Python code, library, or general programming query using natural language.

💻 Tech Stack
Frontend/UI: Streamlit

AI Model: DeepSeek Chat API

Integration: GitHub REST API (via requests and github3.py)

Auth: Uses environment variables for GITHUB_TOKEN and DEEPSEEK_API_KEY

Styling: Custom CSS with image background and modern hover effects

📷 UI Highlights
Blurred wallpaper background

Horizontal task selection buttons with smooth hover effects

Organized layout using st.columns and session state memory for task switching

✅ Requirements
Python 3.8+

streamlit, github3.py, requests, etc.

GitHub personal access token

DeepSeek API key
