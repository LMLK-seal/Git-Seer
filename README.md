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

## ⚙️ Configuration

### Environment Variables
```bash
# Optional: GitHub Personal Access Token for higher API limits
export GITHUB_TOKEN=your_personal_access_token
```

### API Rate Limits
- **Unauthenticated**: 60 requests/hour
- **Authenticated**: 5,000 requests/hour

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

### Development Setup
```bash
# Clone your fork
git clone https://github.com/LMLK-Seal/git-seer.git
cd git-seer

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

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
