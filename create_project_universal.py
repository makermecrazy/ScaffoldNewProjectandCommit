#!/usr/bin/env python3
import os
import subprocess
import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".scaffold_config.json"

def normalize_name(name):
    return name.strip().replace(" ", "_")

def get_project_root():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)["project_root"]
    new_root = input("📍 Enter project root directory (e.g., /Users/yourname/Projects): ").strip()
    with open(CONFIG_PATH, "w") as f:
        json.dump({"project_root": new_root}, f)
    return new_root

def prompt_project_info():
    print("📁 New Project Setup")
    name = normalize_name(input("👉 Enter project name: "))
    print("\n📂 Select project type:")
    types = [
        "python_tool", "shortcuts", "raspberry_pi", "automation_workflow",
        "books", "writing_project", "wordpress_site", "financial_tool",
        "diy_product", "video_project"
    ]
    for i, t in enumerate(types, 1):
        print(f"  {i}. {t}")
    type_index = int(input("🔢 Type number: ")) - 1
    is_public = input("🔓 Make GitHub repo public? (y/n): ").lower() == "y"
    use_venv = input("🐍 Set up virtual environment? (y/n): ").lower() == "y"
    return {
        "name": name,
        "type": types[type_index],
        "is_public": is_public,
        "use_venv": use_venv
    }

def get_github_env():
    username = input("👤 GitHub Username: ").strip()
    token = input("🔑 GitHub Token: ").strip()
    return username, token

def create_folders(project_path, project_type):
    folders = {
        "books": ["chapters", "references", "launchers"],
        "shortcuts": ["csv_exports", "icons", "docs", "launchers"],
        "python_tool": ["src", "tests", "launchers"],
        "raspberry_pi": ["scripts", "configs", "launchers"],
        "automation_workflow": ["zaps", "scripts", "launchers"],
        "writing_project": ["drafts", "images", "launchers"],
        "wordpress_site": ["templates", "plugins", "launchers"],
        "financial_tool": ["statements", "reports", "launchers"],
        "diy_product": ["designs", "photos", "launchers"],
        "video_project": ["clips", "exports", "launchers"]
    }
    print(f"📂 Creating folders for type: {project_type}")
    for folder in folders.get(project_type, []):
        full_path = os.path.join(project_path, folder)
        os.makedirs(full_path, exist_ok=True)
        print(f"✅ Created folder: {full_path}")

def write_gitignore(path):
    gitignore_path = os.path.join(path, ".gitignore")
    content = "__pycache__/\n*.pyc\n.env\nvenv/\n.DS_Store\n"
    with open(gitignore_path, "w") as f:
        f.write(content)
    print(f"✅ Wrote .gitignore at: {gitignore_path}")

def create_env_file(path, username, token):
    env_path = os.path.join(path, ".env")
    with open(env_path, "w") as f:
        f.write(f"GITHUB_USERNAME={username}\nGITHUB_TOKEN={token}\n")
    print(f"✅ Wrote .env file at: {env_path}")

def setup_venv(project_path):
    venv_path = os.path.join(project_path, "venv")
    subprocess.run(["python3", "-m", "venv", venv_path])
    print(f"✅ Virtual environment created at: {venv_path}")

def init_git_repo(project_path, repo_name, is_public, username):
    os.chdir(project_path)
    subprocess.run(["git", "init"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Initial commit"])
    visibility = "--public" if is_public else "--private"
    subprocess.run(["gh", "repo", "create", f"{username}/{repo_name}", visibility, "--source=.", "--push"])
    print("✅ GitHub repo created and initial commit pushed.")

def create_end_session_command(project_path):
    path = os.path.join(project_path, "launchers", "end_session.command")
    script = f"""#!/bin/bash
cd "{project_path}"
git add .
git commit -m "🔄 Auto-commit via end_session.command"
git push
"""
    with open(path, "w") as f:
        f.write(script)
    os.chmod(path, 0o755)
    print(f"✅ Created: {path}")
    return path

def create_launch_dev_command(project_path, project_name):
    path = os.path.join(project_path, "launchers", "launch_dev.command")
    script = f"""#!/bin/bash
source "{project_path}/venv/bin/activate"
echo "🐍 Virtual environment for {project_name} is now active!"
"""
    with open(path, "w") as f:
        f.write(script)
    os.chmod(path, 0o755)
    print(f"✅ Created: {path}")
    return path

def copy_to_launchers(source_path, target_folder, label):
    target_path = os.path.join("/Applications/Utilities/CustomLaunchers", target_folder)
    try:
        print(f"🔄 Copying {label}...")
        os.makedirs(target_path, exist_ok=True)
        subprocess.run(["sudo", "cp", source_path, target_path], check=True)
        subprocess.run(["sudo", "chmod", "+x", os.path.join(target_path, os.path.basename(source_path))], check=True)
        print(f"✅ Copied {label} to: {target_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Copy failed for {label}: {e}")

def main():
    root = get_project_root()
    info = prompt_project_info()
    username, token = get_github_env()

    project_path = os.path.join(root, info["name"])
    print(f"📁 Creating project at: {project_path}")

    if os.path.exists(project_path):
        choice = input("⚠️ Project folder already exists. Skip Git and config setup? (y/n): ").lower()
        if choice == "y":
            print("➡️ Skipping config setup.")
        else:
            print("🔁 Reinitializing project folder...")
    os.makedirs(project_path, exist_ok=True)

    create_folders(project_path, info["type"])
    write_gitignore(project_path)
    create_env_file(project_path, username, token)

    if info["use_venv"]:
        setup_venv(project_path)

    init_git_repo(project_path, info["name"], info["is_public"], username)

    end_cmd = create_end_session_command(project_path)
    launch_cmd = create_launch_dev_command(project_path, info["name"])

    for path, label in [(end_cmd, "end_session.command"), (launch_cmd, "launch_dev.command")]:
        ask = input(f"💬 Also copy {label} to /Applications/Utilities/CustomLaunchers/{info['name']}? (y/n): ").lower()
        if ask == "y":
            copy_to_launchers(path, info["name"], label)

    print(f"✅ Project setup complete: {project_path}")

if __name__ == "__main__":
    main()

