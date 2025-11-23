#!/usr/bin/env python3
"""
Sync research project status to Obsidian vault
"""

import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

OBSIDIAN_VAULT = Path(os.getenv("OBSIDIAN_VAULT_PATH", "/Users/ma/obsidian-vault"))
DAILY_NOTES = Path(os.getenv("OBSIDIAN_DAILY_NOTES_PATH", OBSIDIAN_VAULT / "Daily Notes"))
RESEARCH_PATH = Path(os.getenv("OBSIDIAN_RESEARCH_PATH", OBSIDIAN_VAULT / "Research"))


def update_daily_note(project_name: str, status: str, details: str):
    """Add project update to today's daily note"""
    DAILY_NOTES.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    daily_note = DAILY_NOTES / f"{today}.md"

    update = f"\n## 🔬 {project_name} - {datetime.now().strftime('%H:%M')}\n\n"
    update += f"**Status**: {status}\n\n"
    update += f"{details}\n\n"

    with open(daily_note, "a") as f:
        f.write(update)


def create_research_note(project_id: str, papers: list, progress: dict):
    """Create/update research project note"""
    RESEARCH_PATH.mkdir(parents=True, exist_ok=True)

    note_path = RESEARCH_PATH / f"{project_id}.md"

    content = f"---\ntags: [research, claude-code]\nproject: {project_id}\n"
    content += f"updated: {datetime.now().isoformat()}\n---\n\n"
    content += f"# {project_id}\n\n"
    content += f"## Papers\n\n"

    for i, paper in enumerate(papers, 1):
        status = "✅" if i <= progress.get("implemented", 0) else "⏳"
        content += f"{status} {i}. {paper}\n"

    content += f"\n## Progress\n\n"
    content += f"- **Implemented**: {progress.get('implemented', 0)}/{len(papers)}\n"
    content += f"- **Test Coverage**: {progress.get('coverage', 0):.0f}%\n"
    content += f"- **Commits**: {progress.get('commits', 0)}\n"

    with open(note_path, "w") as f:
        f.write(content)


if __name__ == "__main__":
    # Example usage
    papers = [
        "Anthropic Persona Vectors (2507.21509)",
        "Self-Ablating Transformers (2505.00509)",
        "Representation Engineering (2502.17601)",
        "Steering with Conceptors (2410.16314)",
        "Safety Alignment Depth (2502.00669)",
        "Samba Hybrid SSM (2406.07522)"
    ]

    progress = {
        "implemented": 0,
        "coverage": 0,
        "commits": 0
    }

    create_research_note("01-ai-ml-heretic-enhancement", papers, progress)
    update_daily_note("Heretic Enhancement", "Started", "Initialized research project infrastructure")

    print(f"✓ Updated Obsidian vault at {OBSIDIAN_VAULT}")
