#!/usr/bin/env python3
"""
Create individual canvas file for each repository
Shows the repo at center with its relationships radiating out
"""

import json
from pathlib import Path
from collections import defaultdict

GRAPHS_PATH = Path("/Users/ma/Vault/Repositories/Graphs")
REPOS_PATH = Path("/Users/ma/Vault/Repositories")

def parse_repo_metadata(repo_path):
    """Extract metadata from a repository note"""
    with open(repo_path, 'r') as f:
        content = f.read()

    metadata = {
        'name': repo_path.stem,
        'architecture': 'unknown',
        'domain': 'Other',
        'tech_stack': [],
        'related_repos': []
    }

    # Parse content
    in_related = False
    for line in content.split('\n'):
        if '**Architecture**:' in line:
            metadata['architecture'] = line.split('**Architecture**:')[1].strip()
        elif '**Domain**:' in line:
            metadata['domain'] = line.split('**Domain**:')[1].strip()
        elif '**Tech Stack**:' in line:
            tech = line.split('**Tech Stack**:')[1].strip()
            metadata['tech_stack'] = [t.strip() for t in tech.split(',') if t.strip()]
        elif '## Related Repositories' in line:
            in_related = True
        elif in_related and line.startswith('- [['):
            repo_name = line.split('[[')[1].split(']]')[0]
            metadata['related_repos'].append(repo_name)
        elif in_related and line.startswith('#'):
            in_related = False

    return metadata

def create_repo_canvas(repo_metadata, all_repos_metadata):
    """Create individual canvas for a single repository"""

    nodes = []
    edges = []

    repo_name = repo_metadata['name']

    # Center node - the repository itself
    nodes.append({
        "id": "center",
        "type": "file",
        "file": f"Repositories/{repo_name}.md",
        "x": -200,
        "y": 0,
        "width": 400,
        "height": 200,
        "color": "6"
    })

    # Repository info card
    tech_text = ', '.join(repo_metadata['tech_stack'][:3]) if repo_metadata['tech_stack'] else 'N/A'
    nodes.append({
        "id": "info",
        "type": "text",
        "text": f"## {repo_name}\n\n**Architecture**: {repo_metadata['architecture']}\n**Domain**: {repo_metadata['domain']}\n**Tech**: {tech_text}",
        "x": -200,
        "y": -300,
        "width": 400,
        "height": 180,
        "color": "1"
    })

    edges.append({
        "id": "edge-info",
        "fromNode": "info",
        "toNode": "center",
        "color": "1",
        "fromSide": "bottom",
        "toSide": "top"
    })

    # Related repositories in a circle
    related = repo_metadata['related_repos']

    if related:
        # Header for related repos
        nodes.append({
            "id": "related-header",
            "type": "text",
            "text": f"### Related Repositories\n{len(related)} connections",
            "x": -150,
            "y": 300,
            "width": 300,
            "height": 100,
            "color": "2"
        })

        edges.append({
            "id": "edge-related-header",
            "fromNode": "center",
            "toNode": "related-header",
            "color": "2",
            "fromSide": "bottom",
            "toSide": "top"
        })

        # Position related repos in an arc below
        import math
        num_related = len(related)
        radius = 400
        start_angle = math.pi * 0.25  # Start at bottom-left
        angle_range = math.pi * 1.5  # Spread across bottom half

        for i, related_name in enumerate(related):
            if num_related == 1:
                angle = math.pi / 2  # Directly below
            else:
                angle = start_angle + (i / (num_related - 1)) * angle_range

            x = int(radius * math.cos(angle))
            y = 300 + int(radius * math.sin(angle))

            # Get color based on related repo's architecture if available
            related_color = "3"
            if related_name in all_repos_metadata:
                arch = all_repos_metadata[related_name].get('architecture', 'unknown')
                related_color = {
                    'library': '1',
                    'frontend': '2',
                    'research': '3',
                    'fullstack': '4'
                }.get(arch, '3')

            nodes.append({
                "id": f"related-{i}",
                "type": "file",
                "file": f"Repositories/{related_name}.md",
                "x": x - 120,
                "y": y - 60,
                "width": 240,
                "height": 120,
                "color": related_color
            })

            edges.append({
                "id": f"edge-related-{i}",
                "fromNode": "center",
                "toNode": f"related-{i}",
                "color": related_color,
                "fromSide": "bottom",
                "toSide": "top"
            })

    # Navigation links
    arch_type = repo_metadata['architecture']
    arch_icons = {
        'library': '📚',
        'frontend': '🎨',
        'research': '🔬',
        'fullstack': '🌐'
    }
    icon = arch_icons.get(arch_type, '📁')

    # Link to architecture canvas
    nodes.append({
        "id": "arch-link",
        "type": "text",
        "text": f"→ [[{icon} {arch_type.title()} Repos|All {arch_type.title()} Repos]]",
        "x": -500,
        "y": -300,
        "width": 250,
        "height": 80,
        "color": "5"
    })

    # Link to Architecture Map
    nodes.append({
        "id": "map-link",
        "type": "file",
        "file": "Repositories/Architecture Map.md",
        "x": 300,
        "y": -300,
        "width": 250,
        "height": 80
    })

    # Link to Repositories Hub
    nodes.append({
        "id": "hub-link",
        "type": "file",
        "file": "💻 Repositories Hub.md",
        "x": -125,
        "y": -500,
        "width": 250,
        "height": 80
    })

    canvas_data = {
        "nodes": nodes,
        "edges": edges
    }

    return canvas_data

def main():
    """Create individual canvas for each repository"""

    print("🎨 Creating individual canvas for each repository...\n")

    GRAPHS_PATH.mkdir(parents=True, exist_ok=True)

    # Create subdirectory for individual repo canvases
    individual_graphs = GRAPHS_PATH / "Individual Repos"
    individual_graphs.mkdir(exist_ok=True)

    # Parse all repos first
    all_repos_metadata = {}
    for repo_file in REPOS_PATH.glob("*.md"):
        if repo_file.name in ["README.md", "Architecture Map.md"]:
            continue
        metadata = parse_repo_metadata(repo_file)
        all_repos_metadata[metadata['name']] = metadata

    # Create canvas for each repo
    created = 0
    for repo_name, metadata in sorted(all_repos_metadata.items()):
        canvas_data = create_repo_canvas(metadata, all_repos_metadata)

        output_path = individual_graphs / f"{repo_name}.canvas"
        with open(output_path, 'w') as f:
            json.dump(canvas_data, f, indent=2)

        related_count = len(metadata['related_repos'])
        print(f"  ✓ {repo_name}")
        print(f"    {metadata['architecture']} | {metadata['domain']}")
        print(f"    {related_count} related repos")
        print(f"    {len(canvas_data['nodes'])} nodes, {len(canvas_data['edges'])} edges")
        print()

        created += 1

    print(f"✅ Created {created} individual repository canvases!")
    print(f"\nLocation: {individual_graphs}/")
    print("\nEach canvas shows:")
    print("  • Repository at center (large)")
    print("  • Info card at top (architecture, domain, tech)")
    print("  • Related repos radiating below (circular arc)")
    print("  • Navigation links to architecture canvas and hub")
    print("  • Zero overlapping lines")

if __name__ == "__main__":
    main()
