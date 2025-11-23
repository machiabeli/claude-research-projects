#!/usr/bin/env python3
"""
Create Obsidian graph view groups for repositories
Groups organize the graph view by architecture type with colors
"""

import json
from pathlib import Path

VAULT_PATH = Path("/Users/ma/Vault")
OBSIDIAN_CONFIG = VAULT_PATH / ".obsidian"
REPOS_PATH = VAULT_PATH / "Repositories"

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

def create_graph_groups():
    """Create graph.json with groups for Obsidian"""

    repos_by_arch = parse_architecture_map()

    # Define groups with colors matching our canvas color scheme
    groups = []

    # Hub nodes group (purple/magenta)
    hub_nodes = [
        "🏠 Vault Home",
        "📚 Research Hub",
        "💻 Repositories Hub",
        "📓 Daily Notes Hub",
        "🚀 Projects Hub"
    ]

    groups.append({
        "query": " OR ".join([f'path:"{node}"' for node in hub_nodes]),
        "color": {
            "a": 1,
            "rgb": 11657298  # Purple/magenta for hubs
        }
    })

    # Library repos group (red)
    if repos_by_arch['Library']:
        library_query = " OR ".join([f'path:"Repositories/{repo}"' for repo in repos_by_arch['Library']])
        groups.append({
            "query": library_query,
            "color": {
                "a": 1,
                "rgb": 15548997  # Red (color 1)
            }
        })

    # Frontend repos group (blue)
    if repos_by_arch['Frontend']:
        frontend_query = " OR ".join([f'path:"Repositories/{repo}"' for repo in repos_by_arch['Frontend']])
        groups.append({
            "query": frontend_query,
            "color": {
                "a": 1,
                "rgb": 5431473  # Blue (color 2)
            }
        })

    # Research repos group (green)
    if repos_by_arch['Research']:
        research_query = " OR ".join([f'path:"Repositories/{repo}"' for repo in repos_by_arch['Research']])
        groups.append({
            "query": research_query,
            "color": {
                "a": 1,
                "rgb": 5419488  # Green (color 3)
            }
        })

    # Fullstack repos group (orange)
    if repos_by_arch['Fullstack']:
        fullstack_query = " OR ".join([f'path:"Repositories/{repo}"' for repo in repos_by_arch['Fullstack']])
        groups.append({
            "query": fullstack_query,
            "color": {
                "a": 1,
                "rgb": 16737792  # Orange (color 4)
            }
        })

    # Research papers group (light green)
    groups.append({
        "query": 'path:"Research/Heretic Enhancement/Paper"',
        "color": {
            "a": 1,
            "rgb": 5419488  # Green (research theme)
        }
    })

    # Architecture Map and special files (yellow)
    groups.append({
        "query": 'path:"Repositories/Architecture Map" OR path:"Repositories/README"',
        "color": {
            "a": 1,
            "rgb": 14703607  # Yellow (index/reference)
        }
    })

    # Read existing graph.json or create new
    graph_json_path = OBSIDIAN_CONFIG / "graph.json"

    if graph_json_path.exists():
        with open(graph_json_path, 'r') as f:
            graph_config = json.load(f)
    else:
        graph_config = {
            "collapse-filter": False,
            "search": "",
            "showTags": True,
            "showAttachments": False,
            "hideUnresolved": False,
            "showOrphans": True,
            "collapse-color-groups": False,
            "colorGroups": [],
            "collapse-display": False,
            "showArrow": True,
            "textFadeMultiplier": 0,
            "nodeSizeMultiplier": 1,
            "lineSizeMultiplier": 1,
            "collapse-forces": False,
            "centerStrength": 0.518713248970312,
            "repelStrength": 10,
            "linkStrength": 1,
            "linkDistance": 250,
            "scale": 1,
            "close": False
        }

    # Update color groups
    graph_config["colorGroups"] = groups

    # Save graph.json
    OBSIDIAN_CONFIG.mkdir(parents=True, exist_ok=True)
    with open(graph_json_path, 'w') as f:
        json.dump(graph_config, f, indent=2)

    print(f"✓ Created Obsidian graph groups")
    print(f"  Location: {graph_json_path}")
    print(f"\n📊 Groups created:")
    print(f"  🟣 Hub Nodes: {len(hub_nodes)} hubs")
    print(f"  🔴 Library: {len(repos_by_arch['Library'])} repos")
    print(f"  🔵 Frontend: {len(repos_by_arch['Frontend'])} repos")
    print(f"  🟢 Research: {len(repos_by_arch['Research'])} repos")
    print(f"  🟠 Fullstack: {len(repos_by_arch['Fullstack'])} repos")
    print(f"  🟢 Papers: 6 research papers")
    print(f"  🟡 Index: Architecture Map, README")
    print(f"\nTotal groups: {len(groups)}")
    print(f"\n✨ Graph view will now show:")
    print(f"  • Color-coded circles by architecture type")
    print(f"  • Hub nodes in purple at center")
    print(f"  • Repository clusters color-matched to canvas")
    print(f"  • Research papers in green cluster")

if __name__ == "__main__":
    create_graph_groups()
