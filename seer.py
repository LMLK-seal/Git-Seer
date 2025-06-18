import requests
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Initialize Rich Console for beautiful, formatted output
console = Console()

# This decorator will turn the 'view' function into a CLI command
# attached to the 'app' object.
app = typer.Typer(
    name="git-seer",
    add_completion=False, # Optional: disables shell completion setup
    help="🔮 A lightning-fast CLI tool to get a high-level overview of a GitHub repository without cloning it."
)


def get_repo_metadata(repo_owner: str, repo_name: str) -> dict | None:
    """Fetches general metadata like stars, forks, and description."""
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def get_repo_tree(repo_owner: str, repo_name: str, branch: str = "main") -> list | None:
    """Fetches the full, recursive file tree for a GitHub repository branch."""
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/{branch}?recursive=1"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        if 'tree' in data:
            return data['tree']
        return None
    except requests.exceptions.HTTPError:
        if branch == "main":
            return get_repo_tree(repo_owner, repo_name, branch="master")
        return None
    except requests.exceptions.RequestException:
        return None

# --- Analysis Functions (These are unchanged) ---
def analyze_project_structure(tree: list) -> list:
    structures = []
    paths = {item['path'] for item in tree if item['type'] == 'blob'}
    if any(p.startswith('src/') for p in paths):
        structures.append("📦 'src' layout detected")
    if 'packages' in {p.split('/')[0] for p in paths} or 'apps' in {p.split('/')[0] for p in paths}:
        structures.append(" monorepo structure ('packages/' or 'apps/')")
    if any(p.endswith('manage.py') for p in paths):
        structures.append("🐍 Django project ('manage.py' found)")
    if any(p.endswith('docker-compose.yml') or p.endswith('Dockerfile') for p in paths):
        structures.append("🐳 Dockerized environment ('Dockerfile' or 'docker-compose.yml')")
    if '.github/workflows' in {item['path'] for item in tree if item['type'] == 'tree'}:
        structures.append("🔄 CI/CD configured (GitHub Actions)")
    return structures

def analyze_dependencies(tree: list) -> list:
    dep_files = ["pyproject.toml", "requirements.txt", "package.json", "go.mod", "pom.xml", "build.gradle", "Cargo.toml", "Gemfile"]
    found_files = {item['path'].split('/')[-1] for item in tree if item['path'].split('/')[-1] in dep_files}
    return sorted(list(found_files))

def analyze_code_smells(tree: list) -> list:
    smell_keywords = [".env", "secret", "credentials", "id_rsa", ".pem"]
    smells = [item['path'] for item in tree if any(keyword in item['path'].lower() for keyword in smell_keywords)]
    return smells

def analyze_languages(tree: list) -> dict:
    lang_map = {'.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.tsx': 'TypeScript', '.go': 'Go', '.rs': 'Rust', '.java': 'Java', '.rb': 'Ruby', '.c': 'C', '.cpp': 'C++', '.md': 'Markdown', '.html': 'HTML', '.css': 'CSS', '.yml': 'YAML', '.json': 'JSON'}
    counts = {}
    for item in tree:
        if item['type'] == 'blob':
            parts = item['path'].rsplit('.', 1)
            if len(parts) > 1:
                ext = "." + parts[-1]
                if ext in lang_map:
                    lang = lang_map[ext]
                    counts[lang] = counts.get(lang, 0) + 1
    return counts

# --- THE FIX IS HERE ---
# Instead of a 'view' command, we make the main app function handle the logic.
# The 'repo' argument is now directly part of the main entrypoint.
@app.callback(invoke_without_command=True)
def main(
    repo: str = typer.Argument(..., help="The repository to inspect, in 'owner/name' format."),
):
    """
    Display a high-level overview of a GitHub repository.
    """
    try:
        owner, name = repo.split('/')
    except ValueError:
        console.print(f"❌ [bold red]Error:[/bold red] Invalid repository format. Please use 'owner/repo'.")
        raise typer.Exit(code=1)

    with console.status(f"[bold yellow]🔮 Peering into the digital soul of {repo}...[/]") as status:
        status.update("Fetching repository metadata...")
        metadata = get_repo_metadata(owner, name)
        
        status.update("Fetching file structure (this is the magic part)...")
        file_tree = get_repo_tree(owner, name)

        if not metadata or not file_tree:
            console.print(f"❌ [bold red]Fatal Error:[/bold red] Could not retrieve data for [cyan]{repo}[/cyan].")
            console.print("   - Check if the repository is public and the name is correct.")
            console.print("   - The default branch might not be 'main' or 'master'.")
            raise typer.Exit(code=1)

        status.update("Analyzing codebase from afar...")
        structures = analyze_project_structure(file_tree)
        dependencies = analyze_dependencies(file_tree)
        smells = analyze_code_smells(file_tree)
        languages = analyze_languages(file_tree)

    console.print() 

    title = f"Oracle Report for [link=https://github.com/{repo}]{repo}[/link]"
    stats = f"⭐ {metadata.get('stargazers_count', 0)} │ 🍴 {metadata.get('forks_count', 0)} │ 🐞 {metadata.get('open_issues_count', 0)} issues"
    console.print(Panel(f"[bold cyan]{stats}[/]\n[i]{metadata.get('description', 'No description.')}[/i]", title=title, border_style="green"))

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold magenta")
    table.add_column()
    
    if languages:
        sorted_langs = sorted(languages.items(), key=lambda item: item[1], reverse=True)[:5]
        lang_str = ", ".join([f"{lang} ({count} files)" for lang, count in sorted_langs])
        table.add_row("🗣️ Top Languages", lang_str)

    if structures:
        table.add_row("🏛️ Architecture", "\n".join(f"- {s}" for s in structures))
    
    if dependencies:
        table.add_row("📦 Dependencies", f"Found: [cyan]{', '.join(dependencies)}[/cyan]")

    if smells:
        table.add_row("🚩 Red Flags", f"[yellow]Potential secrets or config found in: {', '.join(smells)}[/yellow]")
    else:
        table.add_row("🚩 Red Flags", "[green]✅ No obvious secret files found.[/green]")

    console.print(table)


if __name__ == "__main__":
    app()
