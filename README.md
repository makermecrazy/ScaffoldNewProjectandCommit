# 🚀 ScaffoldNewProjectandCommit

A universal Python-based scaffolder for creating new projects with GitHub integration, virtual environments, and launcher command automation.

---

## 🔧 How to Use

### 🛠 Launch the Scaffolder

From Finder or Terminal:
```bash
/Applications/Utilities/CustomLaunchers/General Tools/scaffold.command
```

### 📌 What It Prompts You For:

- **Project name**
- **Project type** (e.g. shortcuts, books, tools)
- **Public or private GitHub repo**
- **Use virtual environment (venv)?**
- **GitHub username + token** (stored in `.env`)
- **Project root directory** (only on first use)

---

## 📁 Folder Structure Created

Example (for `ShortcutsCSV` project):

```
ShortcutsCSV/
├── launchers/
│   ├── launch_dev.command
│   └── end_session.command
├── csv_exports/
├── icons/
├── docs/
├── .env
├── .gitignore
├── venv/
```

---

## 🔐 Environment & GitHub

- `.env` will contain:
  ```env
  GITHUB_USERNAME=yourname
  GITHUB_TOKEN=yourtoken
  ```
- **Never commit your token** outside private repos
- GitHub repo is auto-created and pushed from `gh`

---

## 🧪 Virtual Environments

If `venv` is selected:
- A launcher `launch_dev.command` will be created
- It activates the environment and opens a dev shell
- You can edit this to also auto-open VS Code

---

## 🧵 Launcher Commands

All `.command` files are:
- Saved to the project’s `/launchers/` folder
- Optionally copied to:
  ```
  /Applications/Utilities/CustomLaunchers/{ProjectName}/
  ```

To make all `.command` files executable:
```bash
sudo find /Applications/Utilities/CustomLaunchers -name *.command -exec chmod +x {} \;
```

---

## ✅ When You're Done — Use:

```bash
launchers/end_session.command
```

This does:
1. Git add all changes
2. Commit with timestamp
3. Push to the repo

---

## 🧹 First-Time Setup Tips

If anything fails:
- Check for incorrect paths (especially `/Applications/Utilities/...`)
- Remove config cache to re-enter root directory:
  ```bash
  rm ~/.scaffold_config.json
  ```

---

## 💡 Suggestions for Future Additions

- Auto-generate README stubs by project type
- Auto-insert VS Code or iTerm launch triggers
- Add icons to launcher files

## ⚠️ macOS Security Note for `.command` Files

When launching a `.command` file (like `scaffold.command`, `end_scaffold.command`, or `launch_dev.command`) for the first time, macOS may block it due to security settings.

To allow it to run:

1. **Try launching the command file** (double-click it in Finder).
2. If macOS blocks it and shows a warning:
   - Open **System Settings** → **Privacy & Security**
   - Scroll down to the **Security** section
   - You'll see a message like:
     > "`scaffold.command` was blocked from use because it is not from an identified developer"
   - Click **"Allow Anyway"**
3. Re-run the `.command` file. macOS will ask again — this time click **Open**.

This only needs to be done once per file, per system.

🛡 Tip: All command files are editable plain text. You can inspect them before running for peace of mind.
