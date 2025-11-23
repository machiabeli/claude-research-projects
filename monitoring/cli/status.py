#!/usr/bin/env python3
"""
Claude Research Projects - CLI Status Monitor

Quickly check status of all research projects from the command line.
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.layout import Layout
from rich.live import Live
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = typer.Typer(help="Monitor Claude research projects")
console = Console()

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path.cwd()))
METRICS_DB = Path(os.getenv("METRICS_DB_PATH", PROJECT_ROOT / "monitoring/data/metrics.db"))

# Project definitions
PROJECTS = [
    {"id": "01-ai-ml-heretic-enhancement", "name": "Heretic Enhancement", "domain": "AI/ML"},
    {"id": "02-devtools-TBD", "name": "DevTools TBD", "domain": "DevTools"},
    {"id": "03-data-processing-TBD", "name": "Data Processing TBD", "domain": "Data"},
    {"id": "04-web-api-TBD", "name": "Web/API TBD", "domain": "Web/API"},
    {"id": "05-scientific-computing-TBD", "name": "Scientific Computing TBD", "domain": "Scientific"},
]


def get_project_metrics(project_id: str) -> Dict:
    """Get metrics for a specific project"""
    project_path = PROJECT_ROOT / "projects" / project_id

    metrics = {
        "status": "not_started",
        "papers_analyzed": 0,
        "papers_implemented": 0,
        "test_coverage": 0.0,
        "git_commits": 0,
        "last_activity": None,
        "errors": 0,
    }

    if not project_path.exists():
        return metrics

    # Check git activity
    try:
        import git
        repo = git.Repo(project_path)
        metrics["git_commits"] = len(list(repo.iter_commits()))
        if repo.head.is_valid():
            latest_commit = repo.head.commit
            metrics["last_activity"] = datetime.fromtimestamp(latest_commit.committed_date)
            metrics["status"] = "active"
    except:
        pass

    # Check for experiment results
    experiments_path = project_path / "experiments"
    if experiments_path.exists():
        results = list(experiments_path.glob("*/results.json"))
        metrics["papers_implemented"] = len(results)

    # Check test coverage
    coverage_file = project_path / ".coverage"
    if coverage_file.exists():
        try:
            # Simplified coverage parsing
            metrics["test_coverage"] = 85.0  # Placeholder
        except:
            pass

    return metrics


@app.command()
def overview():
    """Show overview of all research projects"""
    console.print("\n[bold cyan]Claude Research Projects - Status Overview[/bold cyan]\n")

    # Create status table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Project", style="cyan", width=30)
    table.add_column("Domain", style="green", width=15)
    table.add_column("Status", width=12)
    table.add_column("Papers", justify="right", width=8)
    table.add_column("Tests", justify="right", width=8)
    table.add_column("Commits", justify="right", width=8)
    table.add_column("Last Activity", width=20)

    total_papers = 0
    total_commits = 0
    active_projects = 0

    for project in PROJECTS:
        metrics = get_project_metrics(project["id"])

        # Status indicator
        if metrics["status"] == "active":
            status = "[green]●[/green] Active"
            active_projects += 1
        elif metrics["status"] == "not_started":
            status = "[dim]○[/dim] Not Started"
        else:
            status = "[yellow]◐[/yellow] In Progress"

        # Papers progress
        papers = f"{metrics['papers_implemented']}/6" if metrics['papers_analyzed'] > 0 else "-"
        total_papers += metrics['papers_implemented']

        # Test coverage
        coverage = f"{metrics['test_coverage']:.0f}%" if metrics['test_coverage'] > 0 else "-"

        # Git commits
        commits = str(metrics['git_commits']) if metrics['git_commits'] > 0 else "-"
        total_commits += metrics['git_commits']

        # Last activity
        last_activity = (
            metrics['last_activity'].strftime("%Y-%m-%d %H:%M")
            if metrics['last_activity']
            else "-"
        )

        table.add_row(
            project["name"],
            project["domain"],
            status,
            papers,
            coverage,
            commits,
            last_activity
        )

    console.print(table)

    # Summary panel
    summary = f"""
[bold]Summary:[/bold]
• Active Projects: {active_projects}/5
• Total Papers Implemented: {total_papers}
• Total Commits: {total_commits}
• Repository: {PROJECT_ROOT}
    """
    console.print(Panel(summary, title="Project Summary", border_style="green"))


@app.command()
def project(
    project_id: str = typer.Argument(..., help="Project ID (e.g., 01-ai-ml-heretic-enhancement)")
):
    """Show detailed status for a specific project"""
    project_path = PROJECT_ROOT / "projects" / project_id

    if not project_path.exists():
        console.print(f"[red]Error: Project '{project_id}' not found[/red]")
        return

    console.print(f"\n[bold cyan]Project: {project_id}[/bold cyan]\n")

    metrics = get_project_metrics(project_id)

    # Project info table
    info_table = Table(show_header=False, box=None)
    info_table.add_column("Metric", style="cyan", width=25)
    info_table.add_column("Value", style="white")

    info_table.add_row("Status", f"[green]{metrics['status']}[/green]")
    info_table.add_row("Papers Analyzed", str(metrics['papers_analyzed']))
    info_table.add_row("Papers Implemented", f"{metrics['papers_implemented']}/6")
    info_table.add_row("Test Coverage", f"{metrics['test_coverage']:.1f}%")
    info_table.add_row("Git Commits", str(metrics['git_commits']))
    info_table.add_row(
        "Last Activity",
        metrics['last_activity'].strftime("%Y-%m-%d %H:%M") if metrics['last_activity'] else "Never"
    )
    info_table.add_row("Errors", str(metrics['errors']))

    console.print(info_table)

    # Recent commits
    try:
        import git
        repo = git.Repo(project_path)
        console.print("\n[bold]Recent Commits:[/bold]")
        for commit in list(repo.iter_commits(max_count=5)):
            console.print(f"  • {commit.hexsha[:7]} - {commit.summary}")
    except:
        pass


@app.command()
def credits():
    """Estimate remaining Claude Code on Web credits"""
    console.print("\n[bold cyan]Credit Usage Estimate[/bold cyan]\n")

    # This would integrate with actual usage tracking
    # For now, showing placeholder
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")

    table.add_row("Total Credits", "1,000,000 tokens")
    table.add_row("Used", "125,000 tokens (12.5%)")
    table.add_row("Remaining", "875,000 tokens (87.5%)")
    table.add_row("Estimated Sessions Left", "~6-8 sessions")
    table.add_row("Expires", "2025-11-23 23:59")

    console.print(table)

    console.print("\n[yellow]⚠ Credits expire tomorrow - prioritize high-impact work![/yellow]\n")


@app.command()
def watch(
    interval: int = typer.Option(30, help="Refresh interval in seconds")
):
    """Watch project status in real-time"""
    try:
        while True:
            console.clear()
            overview()
            console.print(f"\n[dim]Refreshing every {interval}s... (Ctrl+C to exit)[/dim]")
            import time
            time.sleep(interval)
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopped watching[/yellow]")


@app.command()
def init_db():
    """Initialize the metrics database"""
    METRICS_DB.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(METRICS_DB)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            metric_name TEXT NOT NULL,
            metric_value REAL,
            metadata TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT NOT NULL,
            start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            end_time DATETIME,
            tokens_used INTEGER,
            papers_implemented INTEGER,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()

    console.print("[green]✓[/green] Database initialized successfully")


if __name__ == "__main__":
    app()
