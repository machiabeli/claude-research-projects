#!/usr/bin/env python3
"""
Create comprehensive architecture map from repository analysis
"""

import os
from pathlib import Path
from collections import defaultdict
import json

REPOS_PATH = Path("/Users/ma/Vault/Repositories")

def parse_repo_note(note_path: Path) -> dict:
    """Extract architecture and tech info from a repo note"""
    with open(note_path, 'r') as f:
        content = f.read()

    info = {
        'name': note_path.stem,
        'architecture': 'unknown',
        'domain': 'Other',
        'tech_stack': [],
        'language': 'Unknown'
    }

    for line in content.split('\n'):
        if '**Architecture**:' in line:
            info['architecture'] = line.split('**Architecture**:')[1].strip()
        elif '**Domain**:' in line:
            info['domain'] = line.split('**Domain**:')[1].strip()
        elif '**Tech Stack**:' in line:
            tech = line.split('**Tech Stack**:')[1].strip()
            info['tech_stack'] = [t.strip() for t in tech.split(',')]
        elif '**Language**:' in line:
            info['language'] = line.split('**Language**:')[1].strip()

    return info

def create_architecture_map():
    """Create comprehensive architecture map"""

    # Parse all repos
    repos_by_arch = defaultdict(list)
    repos_by_domain = defaultdict(list)
    repos_by_lang = defaultdict(list)
    tech_usage = defaultdict(int)

    for note in REPOS_PATH.glob("*.md"):
        if note.name == "README.md":
            continue

        info = parse_repo_note(note)
        repos_by_arch[info['architecture']].append(info['name'])
        repos_by_domain[info['domain']].append(info['name'])
        repos_by_lang[info['language']].append(info['name'])

        for tech in info['tech_stack']:
            if tech:
                tech_usage[tech] += 1

    # Create architecture map document
    content = """---
tags: [architecture, map, index]
updated: 2025-11-22
---

# Repository Architecture Map

Complete architectural overview of all repositories organized by technical patterns.

## Architecture Summary

"""

    # Architecture breakdown
    total = sum(len(repos) for repos in repos_by_arch.values())
    content += f"**Total Repositories**: {total}\n\n"

    for arch in sorted(repos_by_arch.keys(), key=lambda x: len(repos_by_arch[x]), reverse=True):
        count = len(repos_by_arch[arch])
        pct = (count / total * 100)
        content += f"- **{arch.title()}**: {count} repos ({pct:.1f}%)\n"

    content += "\n## By Architecture Type\n\n"

    # Detailed architecture sections
    for arch in sorted(repos_by_arch.keys(), key=lambda x: len(repos_by_arch[x]), reverse=True):
        repos = sorted(repos_by_arch[arch])
        content += f"### {arch.title()} ({len(repos)} repos)\n\n"

        for repo in repos:
            content += f"- [[{repo}]]\n"
        content += "\n"

    # Domain grouping
    content += "## By Domain\n\n"
    for domain in sorted(repos_by_domain.keys(), key=lambda x: len(repos_by_domain[x]), reverse=True):
        repos = sorted(repos_by_domain[domain])
        content += f"### {domain} ({len(repos)} repos)\n\n"
        for repo in repos:
            content += f"- [[{repo}]]\n"
        content += "\n"

    # Language breakdown
    content += "## By Language\n\n"
    for lang in sorted(repos_by_lang.keys(), key=lambda x: len(repos_by_lang[x]), reverse=True):
        if lang == "Unknown":
            continue
        repos = sorted(repos_by_lang[lang])
        content += f"### {lang} ({len(repos)} repos)\n\n"
        for repo in repos:
            content += f"- [[{repo}]]\n"
        content += "\n"

    # Technology stack analysis
    content += "## Technology Stack Analysis\n\n"
    content += "Most used technologies across all repositories:\n\n"

    for tech, count in sorted(tech_usage.items(), key=lambda x: x[1], reverse=True)[:15]:
        content += f"- **{tech}**: {count} repos\n"

    # Project ecosystems
    content += "\n## Project Ecosystems\n\n"

    ecosystems = {
        'fib0': [],
        'sspr': [],
        'fcag': [],
        'tropical': [],
        'claude': []
    }

    for note in REPOS_PATH.glob("*.md"):
        if note.name == "README.md":
            continue
        name = note.stem
        for ecosystem in ecosystems.keys():
            if ecosystem in name.lower():
                ecosystems[ecosystem].append(name)

    for ecosystem, repos in sorted(ecosystems.items(), key=lambda x: len(x[1]), reverse=True):
        if repos:
            content += f"### {ecosystem.upper()} Ecosystem ({len(repos)} repos)\n\n"
            for repo in sorted(repos):
                content += f"- [[{repo}]]\n"
            content += "\n"

    # Save map
    map_path = REPOS_PATH / "Architecture Map.md"
    with open(map_path, 'w') as f:
        f.write(content)

    print(f"✓ Created architecture map: {map_path}")

    # Print summary
    print("\n📊 Architecture Summary:\n")
    for arch, repos in sorted(repos_by_arch.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {arch.ljust(15)}: {len(repos):2d} repos")

    print(f"\n📚 Domains:")
    for domain, repos in sorted(repos_by_domain.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {domain.ljust(20)}: {len(repos):2d} repos")

    print(f"\n🌳 Ecosystems:")
    for ecosystem, repos in sorted(ecosystems.items(), key=lambda x: len(x[1]), reverse=True):
        if repos:
            print(f"  {ecosystem.ljust(15)}: {len(repos):2d} repos")

if __name__ == "__main__":
    create_architecture_map()
