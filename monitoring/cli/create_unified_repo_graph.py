#!/usr/bin/env python3
"""
Create repository graph matching architecture overview layout
Shows repos organized by architecture type in radial clusters
"""

import json
import math
from pathlib import Path

GRAPHS_PATH = Path("/Users/ma/Vault/Repositories/Graphs")
REPOS_PATH = Path("/Users/ma/Vault/Repositories")

def parse_architecture_map():
    """Parse repos by architecture type from Architecture Map"""

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
            break  # Stop at domain section
        elif line.startswith('- [[') and current_arch:
            repo_name = line.split('[[')[1].split(']]')[0]
            repos_by_arch[current_arch].append(repo_name)

    return repos_by_arch

def create_radial_cluster(repos, center_x, center_y, radius, start_angle=0):
    """Position repos in a circular arc"""
    if not repos:
        return []

    positions = []
    angle_step = (2 * math.pi / 3) / max(len(repos), 1)  # Use 120 degrees per cluster

    for i, repo in enumerate(repos):
        angle = start_angle + (i * angle_step)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        positions.append({
            'repo': repo,
            'x': int(x),
            'y': int(y)
        })

    return positions

def create_unified_repository_graph():
    """Create repository graph matching architecture overview layout"""

    repos_by_arch = parse_architecture_map()

    nodes = []
    edges = []

    # Center node
    nodes.append({
        "id": "center",
        "type": "text",
        "text": "# Repository Map\n\n26 repos by architecture",
        "x": -200,
        "y": -100,
        "width": 400,
        "height": 150,
        "color": "6"
    })

    # Architecture cluster definitions (matching Architecture Overview)
    arch_clusters = [
        {
            "id": "arch-library",
            "name": "Library",
            "text": f"## 📚 Library\n{len(repos_by_arch['Library'])} repos",
            "x": -700,
            "y": -100,
            "color": "1",
            "angle": math.pi,  # Left (180 degrees)
            "radius": 500
        },
        {
            "id": "arch-frontend",
            "name": "Frontend",
            "text": f"## 🎨 Frontend\n{len(repos_by_arch['Frontend'])} repos",
            "x": 500,
            "y": -100,
            "color": "2",
            "angle": 0,  # Right (0 degrees)
            "radius": 500
        },
        {
            "id": "arch-research",
            "name": "Research",
            "text": f"## 🔬 Research\n{len(repos_by_arch['Research'])} repos",
            "x": -200,
            "y": 400,
            "color": "3",
            "angle": math.pi / 2,  # Bottom (90 degrees)
            "radius": 400
        },
        {
            "id": "arch-fullstack",
            "name": "Fullstack",
            "text": f"## 🌐 Fullstack\n{len(repos_by_arch['Fullstack'])} repos",
            "x": -200,
            "y": -600,
            "color": "4",
            "angle": 3 * math.pi / 2,  # Top (270 degrees)
            "radius": 350
        }
    ]

    # Create architecture header nodes
    for arch in arch_clusters:
        nodes.append({
            "id": arch["id"],
            "type": "text",
            "text": arch["text"],
            "x": arch["x"],
            "y": arch["y"],
            "width": 250,
            "height": 120,
            "color": arch["color"]
        })

        # Edge from center to architecture
        edges.append({
            "id": f"edge-{arch['id']}",
            "fromNode": "center",
            "toNode": arch["id"],
            "color": arch["color"],
            "fromSide": "left" if arch["x"] < 0 else "right" if arch["x"] > 0 else ("bottom" if arch["y"] > 0 else "top"),
            "toSide": "right" if arch["x"] < 0 else "left" if arch["x"] > 0 else ("top" if arch["y"] > 0 else "bottom")
        })

    # Position repos around each architecture cluster
    for arch in arch_clusters:
        repos = repos_by_arch[arch["name"]]

        if not repos:
            continue

        # Create circular arc of repos
        positions = create_radial_cluster(
            repos,
            arch["x"],
            arch["y"],
            arch["radius"],
            arch["angle"] - math.pi / 6  # Offset to spread repos
        )

        for pos in positions:
            nodes.append({
                "id": pos["repo"],
                "type": "file",
                "file": f"Repositories/{pos['repo']}.md",
                "x": pos["x"] - 110,
                "y": pos["y"] - 50,
                "width": 220,
                "height": 100
            })

            # Edge from architecture cluster to repo
            edges.append({
                "id": f"edge-{arch['id']}-{pos['repo']}",
                "fromNode": arch["id"],
                "toNode": pos["repo"],
                "color": arch["color"],
                "fromSide": "bottom",
                "toSide": "top"
            })

    # Add link to architecture map
    nodes.append({
        "id": "arch-map-link",
        "type": "file",
        "file": "Repositories/Architecture Map.md",
        "x": -600,
        "y": -400,
        "width": 280,
        "height": 80
    })

    edges.append({
        "id": "edge-arch-map",
        "fromNode": "center",
        "toNode": "arch-map-link",
        "color": "6",
        "fromSide": "top",
        "toSide": "bottom"
    })

    # Save canvas
    canvas_data = {
        "nodes": nodes,
        "edges": edges
    }

    output_path = GRAPHS_PATH / "Repository Graph.canvas"
    with open(output_path, 'w') as f:
        json.dump(canvas_data, f, indent=2)

    print(f"✓ Created unified Repository Graph")
    print(f"  Nodes: {len(nodes)}")
    print(f"  Edges: {len(edges)}")
    print(f"  Layout: Radial by architecture (matches Architecture Overview)")
    print()
    print(f"  📚 Library: {len(repos_by_arch['Library'])} repos")
    print(f"  🎨 Frontend: {len(repos_by_arch['Frontend'])} repos")
    print(f"  🔬 Research: {len(repos_by_arch['Research'])} repos")
    print(f"  🌐 Fullstack: {len(repos_by_arch['Fullstack'])} repos")

if __name__ == "__main__":
    GRAPHS_PATH.mkdir(parents=True, exist_ok=True)
    create_unified_repository_graph()
