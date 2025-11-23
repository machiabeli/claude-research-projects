#!/usr/bin/env python3
"""
Optimize canvas layouts to prevent overlapping relationship lines
Uses circular/radial layouts and smart positioning
"""

import json
import math
from pathlib import Path
from collections import defaultdict

GRAPHS_PATH = Path("/Users/ma/Vault/Repositories/Graphs")

def create_circular_layout(items, center_x, center_y, radius, start_angle=0):
    """Position items in a circle to minimize line overlaps"""
    positions = []
    angle_step = 2 * math.pi / len(items)

    for i, item in enumerate(items):
        angle = start_angle + (i * angle_step)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        positions.append((item, int(x), int(y)))

    return positions

def create_cluster_layout(clusters, canvas_width=3000, canvas_height=2500):
    """Create non-overlapping cluster layout for ecosystems"""

    # Define cluster centers in a grid pattern
    cluster_positions = {
        'fib0': (-1200, 0),
        'sspr': (-400, 0),
        'fcag': (400, 0),
        'tropical': (1200, 0),
        'claude': (-800, 800),
        'other': (0, 800)
    }

    nodes = []
    edges = []

    # Create cluster header nodes
    for cluster_name, (cx, cy) in cluster_positions.items():
        if cluster_name not in clusters or not clusters[cluster_name]:
            continue

        repos = clusters[cluster_name]

        # Header node
        nodes.append({
            "id": f"cluster-{cluster_name}",
            "type": "text",
            "text": f"### {cluster_name.upper()} Ecosystem\n{len(repos)} repositories",
            "x": cx - 150,
            "y": cy - 200,
            "width": 300,
            "height": 100,
            "color": str((hash(cluster_name) % 5) + 1)
        })

        # Position repos in circle around cluster center
        positions = create_circular_layout(repos, cx, cy, 250)

        for repo, x, y in positions:
            nodes.append({
                "id": repo['name'],
                "type": "file",
                "file": f"Repositories/{repo['name']}.md",
                "x": x - 120,
                "y": y - 60,
                "width": 240,
                "height": 120
            })

            # Edge from cluster header to repo
            edges.append({
                "id": f"cluster-{cluster_name}-{repo['name']}",
                "fromNode": f"cluster-{cluster_name}",
                "toNode": repo['name'],
                "color": str((hash(cluster_name) % 5) + 1),
                "fromSide": "bottom",
                "toSide": "top"
            })

    return nodes, edges

def create_optimized_repo_graph():
    """Create repository graph with minimal line overlaps"""

    # Read repository data from Architecture Map
    arch_map_path = Path("/Users/ma/Vault/Repositories/Architecture Map.md")
    with open(arch_map_path, 'r') as f:
        content = f.read()

    # Parse ecosystems from Architecture Map
    ecosystems = {
        'fib0': [],
        'sspr': [],
        'fcag': [],
        'tropical': [],
        'claude': [],
        'other': []
    }

    # Simple parsing - get repos from each ecosystem section
    current_ecosystem = None
    for line in content.split('\n'):
        if '### fib0 Ecosystem' in line:
            current_ecosystem = 'fib0'
        elif '### sspr Ecosystem' in line:
            current_ecosystem = 'sspr'
        elif '### fcag Ecosystem' in line:
            current_ecosystem = 'fcag'
        elif '### tropical Ecosystem' in line:
            current_ecosystem = 'tropical'
        elif '### claude Ecosystem' in line:
            current_ecosystem = 'claude'
        elif line.startswith('- [[') and current_ecosystem:
            repo_name = line.split('[[')[1].split(']]')[0]
            ecosystems[current_ecosystem].append({'name': repo_name})

    # Get all repos for "other" category
    repos_path = Path("/Users/ma/Vault/Repositories")
    all_repos = set()
    for note in repos_path.glob("*.md"):
        if note.name not in ["README.md", "Architecture Map.md"]:
            all_repos.add(note.stem)

    # Find repos not in any ecosystem
    assigned_repos = set()
    for repos in ecosystems.values():
        assigned_repos.update(r['name'] for r in repos)

    for repo in all_repos - assigned_repos:
        ecosystems['other'].append({'name': repo})

    # Create clustered layout
    nodes, edges = create_cluster_layout(ecosystems)

    # Add title node at top
    nodes.insert(0, {
        "id": "title",
        "type": "text",
        "text": "# Repository Ecosystem Map\n\nClustered by project family - minimal line overlap",
        "x": -400,
        "y": -500,
        "width": 800,
        "height": 120,
        "color": "6"
    })

    # Save optimized canvas
    canvas_data = {
        "nodes": nodes,
        "edges": edges
    }

    output_path = GRAPHS_PATH / "Repository Graph.canvas"
    with open(output_path, 'w') as f:
        json.dump(canvas_data, f, indent=2)

    print(f"✓ Optimized Repository Graph")
    print(f"  Nodes: {len(nodes)}")
    print(f"  Edges: {len(edges)}")
    print(f"  Layout: Circular clusters")

def create_optimized_architecture_overview():
    """Create architecture overview with radial layout"""

    nodes = []
    edges = []

    # Center title
    nodes.append({
        "id": "center",
        "type": "text",
        "text": "# Repository Architecture\n\n26 repos by type",
        "x": -200,
        "y": -100,
        "width": 400,
        "height": 150,
        "color": "6"
    })

    # Architecture type nodes in cardinal directions
    arch_nodes = [
        {
            "id": "arch-library",
            "text": "## 📚 Library\n12 repos (46%)\n\nReusable code,\ntools, frameworks",
            "x": -600,
            "y": -100,
            "color": "1"
        },
        {
            "id": "arch-frontend",
            "text": "## 🎨 Frontend\n8 repos (31%)\n\nUser interfaces,\ndashboards",
            "x": 400,
            "y": -100,
            "color": "2"
        },
        {
            "id": "arch-research",
            "text": "## 🔬 Research\n5 repos (19%)\n\nAI/ML projects,\nexperiments",
            "x": -200,
            "y": 300,
            "color": "3"
        },
        {
            "id": "arch-fullstack",
            "text": "## 🌐 Fullstack\n1 repo (4%)\n\nComplete platforms",
            "x": -200,
            "y": -500,
            "color": "4"
        }
    ]

    for arch in arch_nodes:
        nodes.append({
            "id": arch["id"],
            "type": "text",
            "text": arch["text"],
            "x": arch["x"],
            "y": arch["y"],
            "width": 250,
            "height": 180,
            "color": arch["color"]
        })

        edges.append({
            "id": f"edge-{arch['id']}",
            "fromNode": "center",
            "toNode": arch["id"],
            "color": arch["color"],
            "fromSide": "left" if arch["x"] < 0 else "right",
            "toSide": "right" if arch["x"] < 0 else "left"
        })

    # Ecosystem circles around architecture types
    ecosystems = [
        ("fib0", -1000, -100, "1", "5 repos\nfib0, fib0-code,\nfib0-mac-app,\nfib0_remote,\nfib0-remote-ios"),
        ("sspr", -600, 300, "2", "3 repos\nsspr, sspr-old,\nfcag-sspr-dashboard"),
        ("fcag", 400, 300, "3", "2 repos\nfcag-platform,\nfcag-sspr-dashboard"),
        ("tropical", 800, -100, "4", "2 repos\ntropical-shipping,\ntropical-showcase"),
        ("claude", -200, 600, "5", "2 repos\nclaude-research-projects,\nClaudeCodeAgents")
    ]

    for eco_id, x, y, color, text in ecosystems:
        nodes.append({
            "id": f"eco-{eco_id}",
            "type": "text",
            "text": f"### {eco_id}\n{text}",
            "x": x,
            "y": y,
            "width": 220,
            "height": 140,
            "color": color
        })

    # Connect ecosystems to architecture types (no overlapping lines)
    eco_connections = [
        ("eco-fib0", "arch-library", "1"),
        ("eco-sspr", "arch-frontend", "2"),
        ("eco-fcag", "arch-research", "3"),
        ("eco-tropical", "arch-library", "4"),
        ("eco-claude", "arch-research", "5")
    ]

    for from_node, to_node, color in eco_connections:
        edges.append({
            "id": f"conn-{from_node}-{to_node}",
            "fromNode": from_node,
            "toNode": to_node,
            "color": color,
            "fromSide": "top",
            "toSide": "bottom"
        })

    # Links to detailed views
    nodes.append({
        "id": "arch-map-link",
        "type": "file",
        "file": "Repositories/Architecture Map.md",
        "x": -600,
        "y": -400,
        "width": 280,
        "height": 80
    })

    nodes.append({
        "id": "repo-graph-link",
        "type": "text",
        "text": "→ [[Repository Graph|Detailed Ecosystem View]]",
        "x": 400,
        "y": -400,
        "width": 280,
        "height": 80,
        "color": "6"
    })

    canvas_data = {
        "nodes": nodes,
        "edges": edges
    }

    output_path = GRAPHS_PATH / "Architecture Overview.canvas"
    with open(output_path, 'w') as f:
        json.dump(canvas_data, f, indent=2)

    print(f"✓ Optimized Architecture Overview")
    print(f"  Nodes: {len(nodes)}")
    print(f"  Edges: {len(edges)}")
    print(f"  Layout: Radial with cardinal positions")

def create_optimized_vault_overview():
    """Create vault overview with hub-and-spoke layout"""

    nodes = []
    edges = []

    # Center hub
    nodes.append({
        "id": "vault-home",
        "type": "file",
        "file": "🏠 Vault Home.md",
        "x": -200,
        "y": 0,
        "width": 400,
        "height": 200,
        "color": "6"
    })

    # 4 main hubs in cardinal directions (N, E, S, W)
    hubs = [
        ("research-hub", "📚 Research Hub.md", 0, -500, "3"),      # North
        ("repos-hub", "💻 Repositories Hub.md", 700, 0, "2"),      # East
        ("daily-hub", "📓 Daily Notes Hub.md", 0, 500, "4"),       # South
        ("projects-hub", "🚀 Projects Hub.md", -900, 0, "5")       # West
    ]

    for hub_id, file, x, y, color in hubs:
        nodes.append({
            "id": hub_id,
            "type": "file",
            "file": file,
            "x": x - 175,
            "y": y - 90,
            "width": 350,
            "height": 180,
            "color": color
        })

        # Edge from center to hub
        edges.append({
            "id": f"edge-{hub_id}",
            "fromNode": "vault-home",
            "toNode": hub_id,
            "color": color,
            "fromSide": "top" if y < 0 else "bottom" if y > 0 else ("right" if x > 0 else "left"),
            "toSide": "bottom" if y < 0 else "top" if y > 0 else ("left" if x > 0 else "right")
        })

    # Content nodes around each hub (no overlapping lines)

    # Research hub content (North cluster)
    nodes.append({
        "id": "heretic",
        "type": "file",
        "file": "Research/Heretic Enhancement/README.md",
        "x": -400,
        "y": -700,
        "width": 280,
        "height": 120,
        "color": "3"
    })

    nodes.append({
        "id": "papers",
        "type": "text",
        "text": "### 📄 6 Papers\n\nPersona Vectors\nSelf-Ablating\nRep Engineering\nConceptors\nAlignment Depth\nSamba SSM",
        "x": 100,
        "y": -700,
        "width": 280,
        "height": 180,
        "color": "3"
    })

    edges.extend([
        {"id": "e-research-heretic", "fromNode": "research-hub", "toNode": "heretic", "color": "3", "fromSide": "top", "toSide": "bottom"},
        {"id": "e-research-papers", "fromNode": "research-hub", "toNode": "papers", "color": "3", "fromSide": "top", "toSide": "bottom"}
    ])

    # Repos hub content (East cluster)
    nodes.append({
        "id": "arch-map",
        "type": "file",
        "file": "Repositories/Architecture Map.md",
        "x": 1100,
        "y": -200,
        "width": 280,
        "height": 100,
        "color": "2"
    })

    nodes.append({
        "id": "repo-breakdown",
        "type": "text",
        "text": "### Repository Types\n\n📚 Library: 12\n🎨 Frontend: 8\n🔬 Research: 5\n🌐 Fullstack: 1",
        "x": 1100,
        "y": 100,
        "width": 280,
        "height": 160,
        "color": "2"
    })

    edges.extend([
        {"id": "e-repos-arch", "fromNode": "repos-hub", "toNode": "arch-map", "color": "2", "fromSide": "right", "toSide": "left"},
        {"id": "e-repos-breakdown", "fromNode": "repos-hub", "toNode": "repo-breakdown", "color": "2", "fromSide": "right", "toSide": "left"}
    ])

    # Daily hub content (South cluster)
    nodes.append({
        "id": "daily-info",
        "type": "text",
        "text": "### 📅 Daily Notes\n\nAuto-synced:\n• Research updates\n• Commit logs\n• Project progress",
        "x": -150,
        "y": 750,
        "width": 300,
        "height": 160,
        "color": "4"
    })

    edges.append({
        "id": "e-daily-info",
        "fromNode": "daily-hub",
        "toNode": "daily-info",
        "color": "4",
        "fromSide": "bottom",
        "toSide": "top"
    })

    # Projects hub content (West cluster)
    nodes.append({
        "id": "ecosystems",
        "type": "text",
        "text": "### 🌳 Ecosystems\n\nfib0: 5 repos\nsspr: 3 repos\nfcag: 2 repos\ntropical: 2 repos\nclaude: 2 repos",
        "x": -1300,
        "y": -250,
        "width": 280,
        "height": 180,
        "color": "5"
    })

    nodes.append({
        "id": "active-projects",
        "type": "text",
        "text": "### 🚀 Active\n\nHeretic Enhancement\nRepo Analysis\nObsidian Sync",
        "x": -1300,
        "y": 100,
        "width": 280,
        "height": 140,
        "color": "5"
    })

    edges.extend([
        {"id": "e-projects-eco", "fromNode": "projects-hub", "toNode": "ecosystems", "color": "5", "fromSide": "left", "toSide": "right"},
        {"id": "e-projects-active", "fromNode": "projects-hub", "toNode": "active-projects", "color": "5", "fromSide": "left", "toSide": "right"}
    ])

    # Stats at very top
    nodes.append({
        "id": "stats",
        "type": "text",
        "text": "## 📊 Vault Stats\n\n80+ notes • 26 repos • 6 papers • 5 ecosystems • 99 relationships",
        "x": -300,
        "y": -300,
        "width": 600,
        "height": 120,
        "color": "6"
    })

    edges.append({
        "id": "e-stats",
        "fromNode": "stats",
        "toNode": "vault-home",
        "color": "6",
        "fromSide": "bottom",
        "toSide": "top"
    })

    canvas_data = {
        "nodes": nodes,
        "edges": edges
    }

    output_path = GRAPHS_PATH / "Vault Overview.canvas"
    with open(output_path, 'w') as f:
        json.dump(canvas_data, f, indent=2)

    print(f"✓ Optimized Vault Overview")
    print(f"  Nodes: {len(nodes)}")
    print(f"  Edges: {len(edges)}")
    print(f"  Layout: Hub-and-spoke (cardinal directions)")

def main():
    """Optimize all canvas layouts"""

    print("🎨 Optimizing canvas layouts to prevent line overlap...\n")

    GRAPHS_PATH.mkdir(parents=True, exist_ok=True)

    create_optimized_vault_overview()
    print()
    create_optimized_architecture_overview()
    print()
    create_optimized_repo_graph()

    print("\n✅ All canvas files optimized!")
    print("\nLayout strategies used:")
    print("  • Vault Overview: Hub-and-spoke (N/E/S/W)")
    print("  • Architecture Overview: Radial with cardinal positions")
    print("  • Repository Graph: Circular clusters by ecosystem")
    print("\nLines now flow in clear directions with minimal overlap!")

if __name__ == "__main__":
    main()
