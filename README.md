# 🔮 Git Seer

> ⚡ **Lightning-fast GitHub repository analysis without cloning** 

Git Seer is a powerful CLI tool that provides instant insights into any public GitHub repository. Get comprehensive overviews of project structure, dependencies, languages, and potential security concerns—all without downloading a single file.

## ✨ Features

### 🎯 **Core Capabilities**
- 📊 **Repository Analytics** - Stars, forks, issues, and description at a glance
- 🗂️ **Project Structure Analysis** - Detect monorepos, Django projects, Docker setups
- 🔍 **Language Detection** - Identify primary programming languages and file counts
- 📦 **Dependency Scanning** - Find package.json, requirements.txt, and other dependency files
- 🚩 **Security Insights** - Flag potential secrets, credentials, and sensitive files
- ⚡ **Zero Clone Required** - Leverages GitHub API for instant analysis

### 🖥️ **Two Powerful Interfaces**

#### 1. **Standard CLI** (`seer.py`)
Clean, formatted terminal output with rich tables and panels
```bash
python seer.py owner/repository
```

#### 2. **Interactive TUI** (`seer-tui.py`)
Full-featured terminal user interface with expandable file tree navigation
```bash
python seer-tui.py owner/repository
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection (for GitHub API access)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/LMLK-Seal/git-seer.git
   cd git-seer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### 🎨 Standard CLI Mode
```bash
# Analyze any public GitHub repository
python seer.py microsoft/vscode
python seer.py facebook/react
python seer.py your-username/your-repo
```

**Example Output:**
```
┌─ Oracle Report for microsoft/vscode ──────────────────────────┐
│ ⭐ 162,847 │ 🍴 28,234 │ 🐞 6,543 issues                    │
│ Visual Studio Code                                           │
└──────────────────────────────────────────────────────────────┘

🗣️ Top Languages    TypeScript (2,847 files), JavaScript (1,234 files)
🏛️ Architecture     📦 'src' layout detected
                   🐳 Dockerized environment
                   🔄 CI/CD configured (GitHub Actions)
📦 Dependencies     Found: package.json, yarn.lock
🚩 Red Flags        ✅ No obvious secret files found.
```

#### 🖱️ Interactive TUI Mode
```bash
# Launch interactive file explorer
python seer-tui.py microsoft/vscode
```

**TUI Features:**
- 📂 **Expandable file tree** - Navigate repository structure visually
- ⌨️ **Keyboard shortcuts** - `q` to quit, `t` to toggle theme
- 🎨 **Dark/Light themes** - Toggle between visual modes
- 🔄 **Real-time loading** - Asynchronous data fetching with status updates

## 🛠️ Technical Architecture

### Core Components

#### 🔗 **API Integration**
- **GitHub REST API** - Repository metadata and file tree retrieval
- **Rate Limiting Aware** - Handles API limits gracefully
- **Fallback Logic** - Attempts both `main` and `master` branches

#### 🧠 **Analysis Engine**
```python
# Smart project detection
def analyze_project_structure(tree: list) -> list:
    # Detects: src/ layouts, monorepos, Django, Docker, CI/CD
```

#### 🎨 **Rich Terminal UI**
- **Rich Library** - Beautiful tables, panels, and progress indicators
- **Textual Framework** - Interactive TUI components and widgets
- **Typer CLI** - Type-safe command-line argument parsing

### 📁 Project Structure
```
git-seer/
├── seer.py           # Standard CLI interface
├── seer-tui.py       # Interactive TUI interface
├── requirements.txt  # Python dependencies
└── README.md         # This documentation
```

## 🔧 Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| `requests` | GitHub API communication | Latest |
| `typer` | CLI framework | Latest |
| `rich` | Terminal formatting | Latest |
| `textual` | TUI framework | Latest |

Install all dependencies:
```bash
pip install requests typer rich textual
```

## 📊 Analysis Capabilities

### 🏗️ **Project Structure Detection**
- ✅ **Source Layouts** - `src/` directory organization
- ✅ **Monorepos** - `packages/` or `apps/` structure
- ✅ **Framework Detection** - Django (`manage.py`), etc.
- ✅ **Containerization** - Docker and docker-compose files
- ✅ **CI/CD Pipelines** - GitHub Actions workflows

### 🔍 **Language Analysis**
Supports detection of:
- 🐍 Python
- 🟨 JavaScript/TypeScript
- 🦀 Rust
- ☕ Java
- 💎 Ruby
- 🐹 Go
- ⚡ C/C++
- 📝 Markdown, HTML, CSS, YAML, JSON

### 🚨 **Security Scanning**
Flags potentially sensitive files:
- 🔑 `.env` files
- 🔐 Credential files
- 🗝️ SSH keys (`id_rsa`, `.pem`)
- 🚫 Other secret-containing files

## 🎯 Use Cases

### 👨‍💻 **For Developers**
- **Quick Repository Assessment** - Understand project structure before cloning
- **Technology Stack Discovery** - Identify languages and frameworks used
- **Security Auditing** - Spot potential security issues in public repos

### 🏢 **For Teams**
- **Code Review Preparation** - Get context before reviewing PRs
- **Architecture Analysis** - Understand project organization patterns
- **Dependency Auditing** - Identify package managers and dependency files

### 🎓 **For Learning**
- **Open Source Exploration** - Study popular repositories without downloading
- **Best Practices** - Learn from well-structured projects
- **Technology Research** - Discover how different tools are organized

## ⚙️ Configuration (Optional)

### Environment Variables
```bash
# Optional: GitHub Personal Access Token for higher API limits
export GITHUB_TOKEN=your_personal_access_token
```

### API Rate Limits
- **Unauthenticated**: 60 requests/hour
- **Authenticated**: 5,000 requests/hour

### 🔑 GitHub Authentication Setup

Git Seer works seamlessly without any configuration, but adding a GitHub Personal Access Token dramatically improves your experience by increasing API rate limits from 60 to 5,000 requests per hour.

#### Quick Setup

```bash
# Set your GitHub token (optional but recommended)
export GITHUB_TOKEN=your_personal_access_token
```

#### Code Implementation Required

To enable token authentication, you need to modify both seer.py and seer-tui.py. Here are the required changes:

**Step 1: Add import at the top of both files**

```python
import os  # Add this import if not already present
```

**Step 2: Update the request functions in seer.py**

Current Code (Anonymous):

```python
def get_repo_metadata(repo_owner: str, repo_name: str) -> dict | None:
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    try:
        response = requests.get(api_url)  # ← No authentication
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None
```

Updated Code (With Token Support):

```python
def get_repo_metadata(repo_owner: str, repo_name: str) -> dict | None:
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    
    # Check for GitHub token and set up headers
    token = os.getenv("GITHUB_TOKEN")
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        response = requests.get(api_url, headers=headers)  # ← Now with auth
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None
```

**Step 3: Update the get_repo_tree function in seer.py**

Current Code:

```python
def get_repo_tree(repo_owner: str, repo_name: str, branch: str = "main") -> list | None:
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/{branch}?recursive=1"
    try:
        response = requests.get(api_url)  # ← No authentication
        # ... rest of function
```

Updated Code:

```python
def get_repo_tree(repo_owner: str, repo_name: str, branch: str = "main") -> list | None:
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/{branch}?recursive=1"
    
    # Check for GitHub token and set up headers
    token = os.getenv("GITHUB_TOKEN")
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        response = requests.get(api_url, headers=headers)  # ← Now with auth
        # ... rest of function remains the same
```

**Step 4: Update the get_tree function in seer-tui.py**

Current Code:

```python
def get_tree(branch: str = "main") -> list | None:
    api_url = f"https://api.github.com/repos/{owner}/{name}/git/trees/{branch}?recursive=1"
    try:
        response = requests.get(api_url, timeout=10)  # ← No authentication
        # ... rest of function
```

Updated Code:

```python
def get_tree(branch: str = "main") -> list | None:
    api_url = f"https://api.github.com/repos/{owner}/{name}/git/trees/{branch}?recursive=1"
    
    # Check for GitHub token and set up headers
    token = os.getenv("GITHUB_TOKEN")
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)  # ← Now with auth
        # ... rest of function remains the same
```

#### How Authentication Works

The `requests.get()` function sends standard HTTP requests with no inherent knowledge of GitHub's authentication system:

**Without Token (Anonymous Requests):**
- GitHub API receives unauthenticated request
- Counts against public rate limit (60 requests/hour per IP)
- ⚡ Analysis Capacity: ~30-60 repositories/hour

**With Token (Authenticated Requests):**
- Authorization header identifies you to GitHub API
- Counts against your personal rate limit (5,000 requests/hour)
- 🚀 Analysis Capacity: ~2,500-5,000 repositories/hour

### 📈 Performance Impact

Each Git Seer analysis makes 1-2 API calls per repository:
- 1 call for repository metadata (stars, forks, description)
- 1 call for complete file tree structure

| Authentication | Rate Limit | Repos/Hour | Use Case |
|----------------|------------|------------|-----------|
| None | 60 requests/hour | 30-60 repos | Quick checks, demos |
| Token | 5,000 requests/hour | 2,500-5,000 repos | Development, batch analysis |

### 🎯 Creating a GitHub Token

1. Go to GitHub Settings → Personal Access Tokens
2. Click "Generate new token" → Choose "Personal access tokens (classic)"
3. Set Token Name: `git-seer-cli`
4. Select Scopes:
   - ✅ `public_repo` (for public repository access)
   - ✅ `repo` (only if you need private repository access)

5. Generate Token and copy it immediately
6. Set Environment Variable:

```bash
# Linux/macOS
echo 'export GITHUB_TOKEN=your_token_here' >> ~/.bashrc
source ~/.bashrc

# Windows PowerShell
$env:GITHUB_TOKEN="your_token_here"

# Windows Command Prompt
set GITHUB_TOKEN=your_token_here
```

### 🔒 Security Best Practices

- 🔐 Never commit tokens to version control
- 🔄 Rotate tokens regularly (every 6-12 months)
- 📝 Use minimal scopes required for your use case
- 🗑️ Delete unused tokens from GitHub settings
- 💾 Store securely using environment variables or secret managers

## 🔮 Future Enhancements

- [ ] 📈 **Commit Analysis** - Activity patterns and contributor insights
- [ ] 🔄 **Real-time Updates** - Live repository monitoring
- [ ] 💾 **Caching Layer** - Local storage for faster repeated analysis
- [ ] 🌐 **Web Interface** - Browser-based repository explorer
- [ ] 📊 **Export Options** - JSON, CSV, and PDF report generation
- [ ] 🔒 **Private Repository Support** - GitHub token integration

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 **Fork the repository**
2. 🌿 **Create a feature branch**
3. ✍️ **Make your changes**
4. ✅ **Add tests if applicable**
5. 📤 **Submit a pull request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🎨 **Rich** - For beautiful terminal formatting
- 🖥️ **Textual** - For powerful TUI capabilities
- ⚡ **Typer** - For elegant CLI interfaces
- 🐙 **GitHub API** - For making repository data accessible

---

<div align="center">

**⭐ Star this repository if you find it useful!**

</div>

---

<div align="center">
<sub>Built with ❤️ for the developer community</sub>
</div>
