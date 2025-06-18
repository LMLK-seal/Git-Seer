import typer
import requests
from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree, Static
from textual.containers import Container
from textual.binding import Binding

# --- The Main Textual Application Class ---
class SeerApp(App):
    """An interactive TUI for exploring GitHub repositories."""

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="t", action="toggle_theme", description="Toggle Theme"),
    ]

    def __init__(self, repo_full_name: str):
        super().__init__()
        self.repo_full_name = repo_full_name
        self.title = f"git-seer: {repo_full_name}"
        self.file_tree_data = None # To store the fetched data

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        # THIS IS THE CORRECTED LINE:
        yield Header()
        
        yield Container(
            Static(f"🔮 Fetching data for {self.repo_full_name}...", id="status-line"),
            Tree(f"📂 {self.repo_full_name}", id="dir-tree"),
            id="tree-container"
        )
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is first mounted. Load data in a worker."""
        self.query_one(Tree).display = False # Hide tree until loaded
        self.run_worker(self.load_repo_data, thread=True)

    def populate_tree(self) -> None:
        """Populates the Textual Tree widget with file data."""
        if not self.file_tree_data:
            self.query_one("#status-line").update("[red]No file data to display.[/red]")
            return

        tree = self.query_one(Tree)
        tree.clear() # Clear any existing nodes
        tree.root.set_label(f"📂 {self.repo_full_name}")

        nodes = {"": tree.root}
        
        sorted_tree = sorted(self.file_tree_data, key=lambda x: x['path'])

        for item in sorted_tree:
            path = item['path']
            parent_path, _, current_name = path.rpartition('/')
            parent_node = nodes.get(parent_path, tree.root)

            icon = "📄" if item['type'] == 'blob' else "📁"
            label = Text(f"{icon} {current_name}")

            if item['type'] == 'blob':
                parent_node.add_leaf(label, data=path)
            else:
                new_node = parent_node.add(label, data=path, allow_expand=True)
                nodes[path] = new_node
        
        tree.root.expand()
        self.query_one("#status-line").display = False
        self.query_one(Tree).display = True
        self.query_one(Tree).focus()

    def load_repo_data(self) -> None:
        """Worker thread to fetch repo tree data from GitHub API."""
        try:
            owner, name = self.repo_full_name.split('/')
        except ValueError:
            self.call_from_thread(self.query_one("#status-line").update, "[red]Invalid repo format.[/red]")
            return
        
        def get_tree(branch: str = "main") -> list | None:
            api_url = f"https://api.github.com/repos/{owner}/{name}/git/trees/{branch}?recursive=1"
            try:
                response = requests.get(api_url, timeout=10)
                response.raise_for_status()
                data = response.json()
                return data.get('tree')
            except requests.exceptions.HTTPError:
                if branch == "main":
                    return get_tree(branch="master")
                return None
            except requests.exceptions.RequestException:
                return None

        tree_data = get_tree()
        
        if tree_data:
            self.file_tree_data = tree_data
            self.call_from_thread(self.populate_tree)
        else:
            self.call_from_thread(self.query_one("#status-line").update, f"[red]Could not load repository: {self.repo_full_name}[/red]")

    def action_toggle_theme(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


# --- Typer CLI to launch the TUI app ---
cli_app = typer.Typer(
    name="git-seer-tui",
    add_completion=False,
    help="🚀 Launch an interactive TUI to explore a GitHub repository."
)

@cli_app.callback(invoke_without_command=True)
def main(
    repo: str = typer.Argument(..., help="The repository to explore, in 'owner/name' format."),
):
    """
    Launches the interactive TUI for the given repository.
    """
    app = SeerApp(repo_full_name=repo)
    app.run()


if __name__ == "__main__":
    cli_app()
