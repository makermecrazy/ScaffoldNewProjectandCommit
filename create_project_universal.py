# MIT License
# Copyright (c) 2025 Catherine Marucci (makermecrazy)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# create_project_universal.py (PART 1 — user input + folder config)

import os

# Folder recipes for different project types
PROJECT_FOLDERS = {
    "python_tool": {
        "folders": ["src", "scripts", "docs", "tests", "output", "sync"],
        "launcher_folder": "general"
    },
    "shortcuts": {
        "folders": ["shortcuts", "media", "docs", "scripts", "sync", "notes"],
        "launcher_folder": "own"
    },
    "raspberry_pi": {
        "folders": ["configs", "scripts", "hardware", "docs", "tests", "assets", "logs", "launchers"],
        "launcher_folder": "own"
    },
    "automation_workflow": {
        "folders": ["automations", "api_test_data", "logs", "docs", "assets"],
        "launcher_folder": "general"
    },
    "books": {
        "folders": ["chapters", "docs", "notes", "references", "exports", "markdown", "icons"],
        "launcher_folder": "own"
    },
    "writing_project": {
        "folders": ["chapters", "media", "references", "export", "formatting", "sync"],
        "launcher_folder": "general"
    },
    "wordpress_site": {
        "folders": ["html", "shortcodes", "assets", "plugins", "wp_imports", "docs"],
        "launcher_folder": "own"
    },
    "financial_tool": {
        "folders": ["input_data", "cleaned_data", "rules", "scripts", "exports", "logs", "documents"],
        "launcher_folder": "general"
    },
    "diy_product": {
        "folders": ["designs", "mockups", "print_files", "packaging", "docs", "promo"],
        "launcher_folder": "own"
    },
    "video_project": {
        "folders": ["scripts", "recordings", "assets", "captions", "edits", "upload_ready"],
        "launcher_folder": "own"
    },
    "common": {
        "folders": [".gitignore", "README.md", "sync", "launchers"],
        "launcher_folder": None
    }
}

def prompt_user_input():
    print("📁 New Project Setup")

    project_name = input("👉 Enter project name: ").strip()
    print("\n📂 Select project type:")
    types = [k for k in PROJECT_FOLDERS if k != "common"]
    for idx, key in enumerate(types):
        print(f"  {idx+1}. {key}")
    type_selection = input("🔢 Type number: ").strip()

    try:
        project_type = types[int(type_selection)-1]
    except (IndexError, ValueError):
        print("❌ Invalid selection. Exiting.")
        exit(1)

    is_public = input("🔓 Make GitHub repo public? (y/n): ").strip().lower().startswith("y")
    use_venv = input("🐍 Set up virtual environment? (y/n): ").strip().lower().startswith("y")

    return {
        "name": project_name,
        "type": project_type,
        "is_public": is_public,
        "use_venv": use_venv
    }

def create_project_structure(project_info):
    base_path = f"/Users/catmaru/Projects/{project_info['name']}"
    folders = PROJECT_FOLDERS[project_info['type']]['folders']
    common = PROJECT_FOLDERS["common"]["folders"]

    print(f"📁 Creating project at: {base_path}")
    os.makedirs(base_path, exist_ok=True)

    for folder in folders + common:
        folder_path = os.path.join(base_path, folder)
        if not os.path.exists(folder_path):
            if '.' in folder:  # Handle files like README.md or .gitignore
                open(folder_path, 'a').close()
                print(f"📝 Created file: {folder}")
            else:
                os.makedirs(folder_path)
                print(f"📂 Created folder: {folder}")

    # Populate .gitignore if present
    gitignore_path = os.path.join(base_path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "w") as f:
            f.write("venv/\n__pycache__/\n.DS_Store\n.env\n*.pyc\noutput/\n")
        print("✅ Wrote default .gitignore")

    # Always create a .env template file
    env_path = os.path.join(base_path, ".env")
    with open(env_path, "w") as f:
        f.write("# Environment Variables\nAPI_KEY=\nSECRET_KEY=\n")
    print("🧪 Added starter .env file")

        env_path = os.path.join(base_path, ".env")
        with open(env_path, "w") as f:
            f.write("# Example .env\nAPI_KEY=\nSECRET_KEY=\n")
        print("🧪 Added starter .env file")

    # Optional: Set up venv
    if project_info["use_venv"]:
        venv_path = os.path.join(base_path, "venv")
        print("🐍 Creating virtual environment...")
        os.system(f"python3 -m venv '{venv_path}'")

    return base_path

def setup_git_and_github(project_path, project_info):
    os.chdir(project_path)

    print("🔧 Initializing Git repo...")
    os.system("git init")

    # Create GitHub repo using GitHub CLI
    visibility = "public" if project_info["is_public"] else "private"
    repo_name = project_info["name"]

    print(f"🌐 Creating GitHub repo '{repo_name}' ({visibility})...")
    os.system(f"gh repo create {repo_name} --{visibility} --source=. --remote=origin --push")

    print("✅ GitHub repo created and initial commit pushed.")

def main():
    print("🚀 Starting Project Scaffolder...\n")
    project_info = prompt_user_input()

    # Create folder structure and optionally venv
    project_path = create_project_structure(project_info)

    # Set up Git and GitHub repo
    setup_git_and_github(project_path, project_info)

    print("\n✅ Done! Your project has been created at:")
    print(f"📁 {project_path}")

if __name__ == "__main__":
    main()

