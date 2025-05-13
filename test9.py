import streamlit as st
import github3
import os
import base64
import requests
import json
from datetime import datetime, timedelta

# Set Streamlit layout
st.set_page_config(layout="wide")

# Function to encode image for background
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Background image
image_path = r"C:\Users\dinos\Downloads\coolie.jpg"
base64_image = get_base64_image(image_path)

# Inject CSS styling
st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{base64_image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .horizontal-buttons {{
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            gap: 40px;
            margin-top: 40px;
            margin-bottom: 40px;
        }}
        .transparent-button button {{
            background-color: rgba(0, 0, 0, 0.6) !important;
            color: gold !important;
            border: 2px solid gold !important;
            border-radius: 20px !important;
            font-size: 18px !important;
            font-weight: bold !important;
            height: 100px;
            width: 100%;
            transition: all 0.3s ease-in-out;
        }}
        .transparent-button button:hover {{
            background-color: rgba(0, 0, 0, 0.8) !important;
            color: white !important;
            transform: scale(1.05);
        }}
        textarea {{
            height: 400px !important;
            resize: vertical !important;
            overflow: auto !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 style="text-align:center;">🚀 Task Automation Agent for Developers</h1>', unsafe_allow_html=True)

# API Keys
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not DEEPSEEK_API_KEY:
    st.error("❌ DeepSeek API key is missing! Please set it in your environment variables.")

gh = github3.login(token=GITHUB_TOKEN)

# Function to call DeepSeek API
def deepseek_generate(prompt):
    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(API_URL, headers=headers, json=data)
    try:
        response_json = response.json()
        if "choices" in response_json and response_json["choices"]:
            return response_json["choices"][0]["message"]["content"]
        else:
            return "❌ Error: No valid response received from DeepSeek."
    except json.JSONDecodeError:
        return "❌ Error: Invalid JSON response. Check API key or model name."

# Task Selection
task = None
with st.container():
    st.markdown('<div class="horizontal-buttons">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container():
            with st.markdown('<div class="transparent-button">', unsafe_allow_html=True):
                if st.button("GitHub PR Review", key="gh_btn", use_container_width=True):
                    task = "GitHub PR Review"
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        with st.container():
            with st.markdown('<div class="transparent-button">', unsafe_allow_html=True):
                if st.button("Debugging Assistance", key="debug_btn", use_container_width=True):
                    task = "Debugging Assistance"
            st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        with st.container():
            with st.markdown('<div class="transparent-button">', unsafe_allow_html=True):
                if st.button("Code Quality Check", key="quality_btn", use_container_width=True):
                    task = "Code Quality Check"
            st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        with st.container():
            with st.markdown('<div class="transparent-button">', unsafe_allow_html=True):
                if st.button("Chatbot Assistant", key="chat_btn", use_container_width=True):
                    task = "Chatbot Assistant"
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Remember last selected task
if task is None:
    task = st.session_state.get("task", "GitHub PR Review")
else:
    st.session_state.task = task

# === GitHub PR Review ===
if task == "GitHub PR Review":
    HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

    def search_repositories(query):
        url = f"https://api.github.com/search/repositories?q={query}&sort=updated&order=desc"
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        if "items" not in data:
            return None
        now = datetime.utcnow()
        return next((repo for repo in data["items"] if (now - datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ")) <= timedelta(minutes=2)), None)

    def get_latest_commit(owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        response = requests.get(url, headers=HEADERS)
        commits = response.json()
        return commits[0] if isinstance(commits, list) and commits else None

    def get_latest_files(owner, repo, commit_sha):
        url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}"
        response = requests.get(url, headers=HEADERS)
        commit_data = response.json()
        return [file["filename"] for file in commit_data.get("files", [])] or None

    st.subheader("🔍 GitHub Latest Uploaded Code Finder")
    query = st.text_input("Enter a keyword (e.g., 'numpy'):")
    
    if query:
        repo = search_repositories(query)
        if repo:
            st.success(f"Latest updated repository: [{repo['full_name']}]({repo['html_url']})")
            latest_commit = get_latest_commit(repo["owner"]["login"], repo["name"])
            if latest_commit:
                st.write(f"Latest commit: `{latest_commit['sha'][:7]}` by **{latest_commit['commit']['author']['name']}**")
                latest_files = get_latest_files(repo["owner"]["login"], repo["name"], latest_commit["sha"])
                if latest_files:
                    st.write("### Latest Uploaded Files:")
                    for file in latest_files:
                        st.write(f"- `{file}`")
                else:
                    st.warning("No new files uploaded in the latest commit.")
            else:
                st.warning("No commits found for this repository.")
        else:
            st.warning("No repositories updated in the last 2 minutes.")

# === Debugging Assistance ===
elif task == "Debugging Assistance":
    st.subheader("🐞 Debugging Assistance")
    code_input = st.text_area("Enter your Python code:")

    if st.button("Analyze Code"):
        if code_input.strip():
            st.write("### Your Code:")
            st.code(code_input, language="python")
            
            # Try to execute the code to check for errors
            try:
                exec(code_input)
                st.success("The code executed successfully!")
            except Exception as e:
                # Catch errors and display them in simple English with the corrected code
                st.error(f"❌ Error: {str(e)}")
                
                # You can try using the 'deepseek_generate' function for a more detailed error message and correction
                response_text = deepseek_generate(f"Identify and fix errors in this Python code:\n{code_input}")
                st.write("### Analysis:")
                st.markdown(response_text)
                
        else:
            st.warning("Please enter Python code.")

# === Code Quality Check ===
elif task == "Code Quality Check":
    st.subheader("📊 Code Quality Check")
    code_quality_input = st.text_area("Enter your Python code:")

    if st.button("Check Quality"):
        if code_quality_input.strip():
            st.write("### Your Code:")
            st.code(code_quality_input, language="python")
            rating_response = deepseek_generate(f"Analyze the code quality and provide a rating (1-3 stars) and why it is rated so:\n{code_quality_input}")
            
            # Convert words into stars
            if "1 star" in rating_response:
                rating_response = "⭐"
            elif "2 stars" in rating_response:
                rating_response = "⭐⭐"
            elif "3 stars" in rating_response:
                rating_response = "⭐⭐⭐"
            
            obfuscated_code = deepseek_generate(f"Make this code harder to understand but maintain the same functionality:\n{code_quality_input}")

            st.write("### Code Quality Rating:")
            st.markdown(rating_response, unsafe_allow_html=True)

            st.write("### Harder-to-Understand Version:")
            st.code(obfuscated_code, language="python")
        else:
            st.warning("Please enter Python code.")  

# === Chatbot Assistant ===
elif task == "Chatbot Assistant":
    st.subheader("💬 Chatbot Assistant - Explain Anything")
    chatbot_input = st.text_area("Ask a question or paste code to understand libraries/packages:")

    if st.button("Explain"):
        if chatbot_input.strip():
            if any(word in chatbot_input.lower() for word in ["python", "code", "package"]):
                explanation = deepseek_generate(f"Explain the following Python code, including libraries, logic, and purpose:\n{chatbot_input}")
                st.write("### Response:")
                st.markdown(explanation)
            else:
                explanation = deepseek_generate(f"Explain the following word or concept:\n{chatbot_input}")
                st.write("### Response:")
                st.markdown(explanation)
        else:
            st.warning("Please enter a question or code.")
