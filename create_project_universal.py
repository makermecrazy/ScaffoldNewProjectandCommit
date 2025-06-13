#!/usr/bin/env python3
import os
import subprocess
import shutil
from datetime import datetime

def get_input(prompt, default=None):
    response = input(f"{prompt} " + (f"[{default}]: " if default else ": "))
    return response.strip() or default

def ensure_project_root():
    config_file = os.path.expanduser("~/.projectscaffold_config")
    if os.path.exists(config_file):
        with open(config_file) as f:
            return f.read().strip()
    root = get_input("📍 Enter project root directory (e.g., /Users/yourname/Projects):")
    with open(config_file, "w") as f:
        f.write(root)
    return root

def create_env_file(path, github_username, github_token):
    env_path = os.path.join(path, ".env")
    with open(env_path, "w") as f:
        f.write(f"GITHUB_USERNAME={github_username}\n")
        f.write(f"GITHUB_TOKEN={github_token}\n")
    os.chmod(env_path, 0o600)
    print(f"🔐 .env created at {env_path} with restricted permissions.")

def main():
    print("🚀 Launching Project Scaffolder...")

    root = ensure_project_root()
    name = get_input("👉 Enter project name:")
    project_type = get_input("📂 Project type (e.g., python_tool, shortcuts):")
    github_public = get_input("🔓 Make GitHub repo public? (y/n):", "y") == "y"
    use_venv = get_input("🐍 Set up virtual environment? (y/n):", "y") == "y"

    github_username = get_input("👤 GitHub Username:")
    github_token = get_input("🔑 GitHub Token:")

    path = os.path.join(root, name)
    os.makedirs(path, exist_ok=True)

    if use_venv:
        subprocess.run(["python3", "-m", "venv", os.path.join(path, "venv")])

    create_env_file(path, github_username, github_token)

    gitignore_path = os.path.join(path, ".gitignore")
    with open(gitignore_path, "w") as f:
        f.write("__pycache__/\n*.py[cod]\n.venv/\n.env\n")

    subprocess.run(["git", "init"], cwd=path)
    subprocess.run(["git", "add", "."], cwd=path)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=path)

    visibility = "public" if github_public else "private"
    subprocess.run([
        "gh", "repo", "create", f"{github_username}/{name}",
        "--source", path, "--{0}".format("public" if github_public else "private"), "--push"
    ])

    print(f"✅ Project setup complete: {path}")

if __name__ == "__main__":
    main()
