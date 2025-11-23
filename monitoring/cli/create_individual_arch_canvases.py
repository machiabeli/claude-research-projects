#!/usr/bin/env python3
"""
Create individual canvas files for each architecture type
Clean, focused views with no overlapping lines
"""

import json
import math
from pathlib import Path

GRAPHS_PATH = Path("/Users/ma/Vault/Repositories/Graphs")
REPOS_PATH = Path("/Users/ma/Vault/Repositories")

def parse_architecture_map():
    """Parse repos by architecture type"""
    arch_map_path = REPOS_PATH / "Architecture Map.md"
    with open(arch_map_path, 'r') as f:
        content = f.read()

    repos_by_arch = {
        'Library': [],
        'Frontend': [],
        'Research': [],
        'Fullstack': []
    }

    current_arch = None
    for line in content.split('\n'):
        if line.startswith('### Library ('):
            current_arch = 'Library'
        elif line.startswith('### Frontend ('):
            current_arch = 'Frontend'
        elif line.startswith('### Research ('):
            current_arch = 'Research'
        elif line.startswith('### Fullstack ('):
            current_arch = 'Fullstack'
        elif line.startswith('## By Domain'):
            break
        elif line.startswith('- [[') and current_arch:
            repo_name = line.split('[[')[1].split(']]')[0]
            repos_by_arch[current_arch].append(repo_name)

    return repos_by_arch

def create_circular_layout(repos, center_x=0, center_y=0, radius=400):
    """Position repos in a perfect circle"""
    if not repos:
        return []

    positions = []
    angle_step = 2 * math.pi / len(repos)

    for i, repo in enumerate(repos):
        angle = i * angle_step
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        positions.append({
            'repo': repo,
            'x': int(x),
            'y': int(y)
        })

    return positions

def create_architecture_canvas(arch_name, repos, color, icon):
    """Create individual canvas for an architecture type"""

    nodes = []
    edges = []

    # Center header
    nodes.append({
        "id": "header",
        "type": "text",
        "text": f"# {icon} {arch_name}\n\n{len(repos)} repositories",
        "x": -200,
        "y": -100,
        "width": 400,
        "height": 150,
        "color": color
    })

    # Position repos in circle
    positions = create_circular_layout(repos, center_x=0, center_y=100, radius=500)

    for pos in positions:
        nodes.append({
            "id": pos["repo"],
            "type": "file",
            "file": f"Repositories/{pos['repo']}.md",
            "x": pos["x"] - 120,
            "y": pos["y"] - 60,
            "width": 240,
            "height": 120
        })

        # Edge from header to repo
        edges.append({
            "id": f"edge-{pos['repo']}",
            "fromNode": "header",
            "toNode": pos["repo"],
            "color": color,
            "fromSide": "bottom",
            "toSide": "top"
        })

    # Link to architecture map
    nodes.append({
        "id": "arch-map",
        "type": "file",
        "file": "Repositories/Architecture Map.md",
        "x": -140,
        "y": -350,
        "width": 280,
        "height": 80
    })

    edges.append({
        "id": "edge-arch-map",
        "fromNode": "arch-map",
        "toNode": "header",
        "color": "6",
        "fromSide": "bottom",
        "toSide": "top"
    })

    # Navigation links to other architecture canvases
    nav_y = -350
    other_archs = [
        ("Library", "📚", "1"),
        ("Frontend", "🎨", "2"),
        ("Research", "🔬", "3"),
        ("Fullstack", "🌐", "4")
    ]

    nav_x_offset = -450
    for other_name, other_icon, other_color in other_archs:
        if other_name == arch_name:
            continue

        nodes.append({
            "id": f"nav-{other_name.lower()}",
            "type": "text",
            "text": f"→ [[{other_icon} {other_name} Repos|{other_icon} {other_name}]]",
            "x": nav_x_offset,
            "y": nav_y,
            "width": 200,
            "height": 60,
            "color": other_color
        })

        nav_x_offset += 250

    canvas_data = {
        "nodes": nodes,
        "edges": edges
    }

    return canvas_data

def main():
    """Create individual canvas for each architecture type"""

    repos_by_arch = parse_architecture_map()

    print("🎨 Creating individual architecture canvas files...\n")

    GRAPHS_PATH.mkdir(parents=True, exist_ok=True)

    architectures = [
        ("Library", "1", "📚"),
        ("Frontend", "2", "🎨"),
        ("Research", "3", "🔬"),
        ("Fullstack", "4", "🌐")
    ]

    for arch_name, color, icon in architectures:
        repos = repos_by_arch[arch_name]

        if not repos:
            print(f"  ⚠️  {arch_name}: No repos found, skipping")
            continue

        canvas_data = create_architecture_canvas(arch_name, repos, color, icon)

        output_path = GRAPHS_PATH / f"{icon} {arch_name} Repos.canvas"
        with open(output_path, 'w') as f:
            json.dump(canvas_data, f, indent=2)

        print(f"  ✓ {icon} {arch_name}: {len(repos)} repos")
        print(f"    {output_path.name}")
        print(f"    {len(canvas_data['nodes'])} nodes, {len(canvas_data['edges'])} edges")
        print()

    print("✅ Created 4 individual architecture canvases!")
    print("\nEach canvas shows:")
    print("  • Central header with architecture name")
    print("  • Repos arranged in perfect circle")
    print("  • Clean radial connections (no overlap)")
    print("  • Links to Architecture Map")
    print("  • Navigation to other architecture canvases")

if __name__ == "__main__":
    main()
