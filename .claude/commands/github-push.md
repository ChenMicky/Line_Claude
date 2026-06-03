---
name: "GitHub: Push"
description: Upload current project to GitHub, creating a new repo if needed while excluding private keys/secrets
category: Git
tags: [git, github, upload, deploy]
---

Upload the current project to GitHub. Creates a new repository if none exists and automatically excludes private information.

**Input**: Optionally specify a repository name. If omitted, uses the current directory name.

**Steps**

1. **Check prerequisites**
   - Verify `gh` (GitHub CLI) is installed: `gh --version`
   - If not installed, prompt user to install: `brew install gh`
   - Verify user is authenticated: `gh auth status`
   - If not authenticated, run `gh auth login` to guide setup

2. **Determine repository name**
   - If provided as input, use it
   - Otherwise, use current directory name: `basename "$(pwd)"`
   - Ask user to confirm or provide alternative name

3. **Check if repository already exists**
   ```bash
   gh repo view <owner>/<repo-name> 2>/dev/null
   ```
   - If exists: proceed to push
   - If not found: create new repository

4. **Create .gitignore if needed**
   - Check if `.gitignore` exists
   - If not, create a comprehensive one:
   ```
   # Environment variables
   .env
   .env.local
   .env.*.local
   .env.production
   .env.development
   
   # Secrets & Keys
   *.pem
   *.key
   *.crt
   *.p12
   *.keystore
   secrets.json
   credentials.json
   service-account-key.json
   
   # Node/npm
   node_modules/
   npm-debug.log*
   yarn-error.log
   
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   .venv/
   venv/
   
   # IDE
   .vscode/
   .idea/
   *.swp
   *.swo
   .DS_Store
   
   # Build outputs
   dist/
   build/
   .next/
   out/
   
   # Logs
   *.log
   logs/
   
   # Database
   *.db
   *.sqlite
   *.sqlite3
   
   # Private config
   config/local.js
   secrets/
   private/
   ```

5. **Initialize git if needed**
   - Check if `.git` directory exists
   - If not, run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

6. **Create repository (if new)**
   ```bash
   gh repo create <repo-name> --private --source=. --push
   ```
   - Ask user if they want public or private (default: private)
   - Add `--public` flag if requested

7. **Push to existing repository**
   - If repo exists but no remote:
   ```bash
   gh repo create <repo-name> --source=. --push --private
   ```
   - If remote exists but no commits:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```
   - If already has commits, just:
   ```bash
   git push
   ```

8. **Show result**
   - Display the GitHub repository URL
   - Confirm what was uploaded
   - Remind user about .gitignore for any additional private files

**Output on Success**
```
✓ GitHub repository created/pushed successfully!

Repository: https://github.com/<owner>/<repo-name>

Note: Private information was excluded via .gitignore
```

**Guardrails**
- Always check for .gitignore before first push
- Never commit .env, keys, or secrets files
- Confirm repository visibility (public/private) with user
- If project has existing git history, respect it and just add remote