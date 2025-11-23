#!/usr/bin/env python3
"""
Sync all GitHub repositories to Obsidian vault

Creates and updates notes for each repository with:
- README preview
- Recent commits
- Open issues/PRs
- Project stats
- Links to related repos
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv
from github import Github

load_dotenv()

OBSIDIAN_VAULT = Path(os.getenv("OBSIDIAN_VAULT_PATH", "/Users/ma/Vault"))
REPOS_PATH = OBSIDIAN_VAULT / "Repositories"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "machiabeli")


def get_all_repos() -> List:
    """Get all user repositories from GitHub"""
    if GITHUB_TOKEN:
        g = Github(GITHUB_TOKEN)
    else:
        # Try to get token from gh CLI
        try:
            result = subprocess.run(
                ["gh", "auth", "token"],
                capture_output=True,
                text=True,
                check=True
            )
            token = result.stdout.strip()
            g = Github(token)
        except:
            print("⚠️  No GitHub token found. Set GITHUB_TOKEN or authenticate with 'gh auth login'")
            return []

    user = g.get_user()
    repos = list(user.get_repos())
    print(f"✓ Found {len(repos)} repositories")
    return repos


def create_repo_note(repo) -> Path:
    """Create/update Obsidian note for a repository"""
    REPOS_PATH.mkdir(parents=True, exist_ok=True)

    # Sanitize repo name for filename
    safe_name = repo.name.replace("/", "-")
    note_path = REPOS_PATH / f"{safe_name}.md"

    # Get repo stats
    try:
        stars = repo.stargazers_count
        forks = repo.forks_count
        open_issues = repo.open_issues_count
        language = repo.language or "Unknown"
        description = repo.description or "No description"
        updated = repo.updated_at.strftime("%Y-%m-%d %H:%M")

        # Get recent commits
        commits = list(repo.get_commits()[:5])

        # Get topics/tags
        topics = repo.get_topics()

    except Exception as e:
        print(f"⚠️  Error fetching data for {repo.name}: {e}")
        return note_path

    # Build note content
    content = f"---\n"
    content += f"tags: [repository, github, {language.lower() if language != 'Unknown' else 'code'}]\n"
    if topics:
        content += f"topics: [{', '.join(topics)}]\n"
    content += f"repo: {repo.full_name}\n"
    content += f"updated: {datetime.now().isoformat()}\n"
    content += f"stars: {stars}\n"
    content += f"forks: {forks}\n"
    content += f"---\n\n"

    content += f"# {repo.name}\n\n"
    content += f"> {description}\n\n"

    content += f"## Quick Links\n\n"
    content += f"- 🔗 [GitHub]({repo.html_url})\n"
    if repo.homepage:
        content += f"- 🌐 [Website]({repo.homepage})\n"
    content += f"- 📁 [Clone URL]({repo.clone_url})\n\n"

    content += f"## Stats\n\n"
    content += f"- **Language**: {language}\n"
    content += f"- **Stars**: ⭐ {stars}\n"
    content += f"- **Forks**: 🍴 {forks}\n"
    content += f"- **Issues**: 🐛 {open_issues}\n"
    content += f"- **Last Updated**: {updated}\n\n"

    if topics:
        content += f"## Topics\n\n"
        for topic in topics:
            content += f"- #{topic}\n"
        content += f"\n"

    content += f"## Recent Commits\n\n"
    for commit in commits:
        sha = commit.sha[:7]
        message = commit.commit.message.split('\n')[0][:80]
        date = commit.commit.author.date.strftime("%Y-%m-%d")
        content += f"- `{sha}` {message} ({date})\n"
    content += f"\n"

    # Check if this is a research project
    if "research" in description.lower() or "claude" in description.lower():
        content += f"## Related Notes\n\n"
        content += f"- [[Research]]\n"
        if "claude-research-projects" in repo.name:
            content += f"- [[Heretic Enhancement]]\n"
        content += f"\n"

    content += f"## Notes\n\n"
    content += f"(Add your notes about this repository here)\n"

    with open(note_path, "w") as f:
        f.write(content)

    return note_path


def create_repos_index():
    """Create main index of all repositories"""
    index_path = REPOS_PATH / "README.md"

    content = f"---\n"
    content += f"tags: [index, repositories]\n"
    content += f"updated: {datetime.now().isoformat()}\n"
    content += f"---\n\n"
    content += f"# My Repositories\n\n"
    content += f"Auto-generated index of all GitHub repositories.\n\n"

    # Group repos by language
    repos_by_language = {}
    for note in sorted(REPOS_PATH.glob("*.md")):
        if note.name == "README.md":
            continue
        # Parse frontmatter to get language
        try:
            with open(note) as f:
                lines = f.readlines()
                language = "Other"
                for line in lines[1:20]:  # Check first 20 lines for metadata
                    if "Language**: " in line:
                        language = line.split("**: ")[1].strip()
                        break

                if language not in repos_by_language:
                    repos_by_language[language] = []
                repos_by_language[language].append(note.stem)
        except:
            pass

    content += f"## By Language\n\n"
    for language in sorted(repos_by_language.keys()):
        content += f"### {language}\n\n"
        for repo in sorted(repos_by_language[language]):
            content += f"- [[{repo}]]\n"
        content += f"\n"

    content += f"## All Repositories\n\n"
    for note in sorted(REPOS_PATH.glob("*.md")):
        if note.name == "README.md":
            continue
        content += f"- [[{note.stem}]]\n"

    with open(index_path, "w") as f:
        f.write(content)

    return index_path


def sync_all_repos():
    """Sync all repositories to Obsidian"""
    print(f"🔄 Syncing repositories to {OBSIDIAN_VAULT}")

    repos = get_all_repos()
    if not repos:
        return

    created = []
    for repo in repos:
        try:
            note_path = create_repo_note(repo)
            created.append(note_path)
            print(f"  ✓ {repo.name}")
        except Exception as e:
            print(f"  ✗ {repo.name}: {e}")

    # Create index
    index_path = create_repos_index()
    print(f"\n✓ Created {len(created)} repository notes")
    print(f"✓ Created index at {index_path}")

    # Auto-commit if Obsidian Git plugin is configured
    try:
        git_plugin_path = OBSIDIAN_VAULT / ".obsidian" / "plugins" / "obsidian-git"
        if git_plugin_path.exists():
            print(f"\n💡 Tip: Obsidian Git plugin will auto-sync these changes")
    except:
        pass


if __name__ == "__main__":
    sync_all_repos()
