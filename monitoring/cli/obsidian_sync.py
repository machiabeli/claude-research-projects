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


def create_research_note(project_id: str, project_name: str, papers: list, progress: dict):
    """Create/update research project folder and notes"""
    RESEARCH_PATH.mkdir(parents=True, exist_ok=True)

    # Create project folder
    project_folder = RESEARCH_PATH / project_name
    project_folder.mkdir(parents=True, exist_ok=True)

    # Main project overview note
    overview_path = project_folder / "README.md"

    content = f"---\ntags: [research, claude-code]\nproject: {project_id}\n"
    content += f"updated: {datetime.now().isoformat()}\n---\n\n"
    content += f"# {project_name}\n\n"
    content += f"## Overview\n\n"
    content += f"Research project implementing {len(papers)} cutting-edge papers.\n\n"
    content += f"## Papers\n\n"

    for i, paper in enumerate(papers, 1):
        status = "✅" if i <= progress.get("implemented", 0) else "⏳"
        content += f"{status} {i}. {paper}\n"

    content += f"\n## Progress\n\n"
    content += f"- **Implemented**: {progress.get('implemented', 0)}/{len(papers)}\n"
    content += f"- **Test Coverage**: {progress.get('coverage', 0):.0f}%\n"
    content += f"- **Commits**: {progress.get('commits', 0)}\n"
    content += f"\n## Notes\n\n"
    content += f"See individual paper notes in this folder for detailed implementation notes.\n"

    with open(overview_path, "w") as f:
        f.write(content)

    # Create individual paper notes for graph visualization
    for i, paper in enumerate(papers, 1):
        # Extract paper name and arxiv ID
        paper_name = paper.split(" (")[0]
        arxiv_id = paper.split("(")[1].rstrip(")") if "(" in paper else f"paper-{i}"

        paper_note_path = project_folder / f"Paper {i} - {paper_name}.md"

        status = "implemented" if i <= progress.get("implemented", 0) else "pending"

        paper_content = f"---\n"
        paper_content += f"tags: [paper, research, {status}]\n"
        paper_content += f"arxiv: {arxiv_id}\n"
        paper_content += f"project: [[README]]\n"
        paper_content += f"---\n\n"
        paper_content += f"# {paper_name}\n\n"
        paper_content += f"**arXiv ID**: [{arxiv_id}](https://arxiv.org/abs/{arxiv_id})\n\n"
        paper_content += f"## Status\n\n"
        paper_content += f"{'✅ Implemented' if status == 'implemented' else '⏳ Pending'}\n\n"
        paper_content += f"## Implementation Notes\n\n"
        paper_content += f"- [ ] Paper reviewed\n"
        paper_content += f"- [ ] Code implemented\n"
        paper_content += f"- [ ] Tests written\n"
        paper_content += f"- [ ] Benchmarks run\n\n"
        paper_content += f"## Related Papers\n\n"

        # Link to previous and next papers
        if i > 1:
            prev_paper = papers[i-2].split(" (")[0]
            paper_content += f"← [[Paper {i-1} - {prev_paper}|Previous]]\n\n"
        if i < len(papers):
            next_paper = papers[i].split(" (")[0]
            paper_content += f"→ [[Paper {i+1} - {next_paper}|Next]]\n\n"

        paper_content += f"## Key Concepts\n\n"
        paper_content += f"(Add key concepts and techniques from this paper)\n\n"
        paper_content += f"## Integration Points\n\n"
        paper_content += f"(How this paper integrates with [[README|{project_name}]])\n"

        with open(paper_note_path, "w") as f:
            f.write(paper_content)

    return project_folder


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

    project_folder = create_research_note(
        "01-ai-ml-heretic-enhancement",
        "Heretic Enhancement",
        papers,
        progress
    )
    update_daily_note("Heretic Enhancement", "Started", "Initialized research project infrastructure")

    print(f"✓ Updated Obsidian vault at {OBSIDIAN_VAULT}")
    print(f"✓ Created project folder at {project_folder}")
