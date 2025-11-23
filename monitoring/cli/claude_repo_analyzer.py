#!/usr/bin/env python3
"""
Claude-Powered Repository Analyzer

Uses Claude to analyze repositories and create intelligent:
- Cross-repository links based on relationships
- Technology stack groupings
- Dependency graphs
- Obsidian canvas visualizations
- Smart tags and categories
"""

import os
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Set
from datetime import datetime
from dotenv import load_dotenv
from github import Github

load_dotenv()

OBSIDIAN_VAULT = Path(os.getenv("OBSIDIAN_VAULT_PATH", "/Users/ma/Vault"))
REPOS_PATH = OBSIDIAN_VAULT / "Repositories"
GRAPHS_PATH = REPOS_PATH / "Graphs"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")


def analyze_repo_with_claude(repo_data: Dict) -> Dict:
    """
    Use Claude to analyze a repository and extract:
    - Technology stack
    - Purpose and domain
    - Related repositories
    - Dependency relationships
    - Suggested tags
    """

    # Prepare repository context for Claude
    context = f"""Analyze this GitHub repository:

Name: {repo_data['name']}
Description: {repo_data['description']}
Language: {repo_data['language']}
Topics: {', '.join(repo_data.get('topics', []))}
README Preview: {repo_data.get('readme_preview', 'N/A')[:500]}
Recent Commits: {json.dumps(repo_data.get('recent_commits', []), indent=2)}

Please analyze and provide:

1. **Technology Stack**: List all technologies, frameworks, and tools used
2. **Domain/Purpose**: What category does this belong to? (e.g., "AI/ML", "Web Dashboard", "Mobile App", "Infrastructure", "Research")
3. **Relationships**: What types of repositories would this relate to?
4. **Tags**: Suggest 3-5 specific tags for organization
5. **Architecture**: Is this frontend, backend, fullstack, library, tool, or other?

Return as JSON:
{{
    "tech_stack": ["python", "fastapi", "postgresql"],
    "domain": "Backend API",
    "purpose": "Brief description of what this does",
    "architecture_type": "backend",
    "suggested_tags": ["api", "production", "microservice"],
    "related_patterns": ["needs frontend", "uses database", "part of platform"],
    "complexity": "medium"
}}
"""

    # Use Claude API or fallback to heuristic analysis
    if CLAUDE_API_KEY:
        try:
            # Use Anthropic API
            analysis = call_claude_api(context)
            return json.loads(analysis)
        except Exception as e:
            print(f"  Claude API error: {e}, falling back to heuristic analysis")

    # Fallback: heuristic analysis
    return heuristic_analysis(repo_data)


def call_claude_api(prompt: str) -> str:
    """Call Claude API for analysis"""
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text
    except ImportError:
        print("  ⚠️  anthropic package not installed. Run: pip install --user anthropic")
        raise


def heuristic_analysis(repo_data: Dict) -> Dict:
    """Fallback heuristic analysis when Claude API is not available"""

    language = repo_data.get('language', '').lower()
    description = repo_data.get('description', '').lower()
    topics = [t.lower() for t in repo_data.get('topics', [])]
    name = repo_data['name'].lower()

    # Determine tech stack
    tech_stack = [language] if language else []

    # Common framework detection
    if 'react' in description or 'react' in topics:
        tech_stack.append('react')
    if 'next' in name or 'nextjs' in topics:
        tech_stack.append('nextjs')
    if 'fastapi' in description:
        tech_stack.append('fastapi')
    if 'django' in description:
        tech_stack.append('django')
    if 'typescript' in topics:
        tech_stack.append('typescript')

    # Determine domain
    domain = "Other"
    if any(x in description for x in ['dashboard', 'ui', 'frontend']):
        domain = "Web Dashboard"
        architecture_type = "frontend"
    elif any(x in description for x in ['api', 'backend', 'server']):
        domain = "Backend API"
        architecture_type = "backend"
    elif any(x in description for x in ['mobile', 'ios', 'android', 'app']):
        domain = "Mobile App"
        architecture_type = "mobile"
    elif any(x in description for x in ['research', 'paper', 'ml', 'ai']):
        domain = "AI/ML Research"
        architecture_type = "research"
    elif any(x in description for x in ['platform', 'system']):
        domain = "Platform"
        architecture_type = "fullstack"
    else:
        architecture_type = "library"

    # Suggest tags
    tags = []
    if 'dashboard' in name:
        tags.append('dashboard')
    if language:
        tags.append(language.lower())
    if 'sspr' in name or 'fcag' in name:
        tags.append('work-project')
    if 'fib0' in name:
        tags.append('fib0-ecosystem')
    if 'claude' in name:
        tags.append('claude-ai')

    # Determine relationships
    related_patterns = []
    if architecture_type == "frontend":
        related_patterns.append("needs backend")
    if architecture_type == "backend":
        related_patterns.append("needs frontend")
    if 'database' in description:
        related_patterns.append("uses database")

    return {
        "tech_stack": tech_stack[:5],  # Top 5
        "domain": domain,
        "purpose": repo_data.get('description', 'No description')[:100],
        "architecture_type": architecture_type,
        "suggested_tags": tags[:5],
        "related_patterns": related_patterns,
        "complexity": "medium"
    }


def find_related_repos(repo_name: str, all_repos: List[Dict], analysis: Dict) -> List[str]:
    """Find related repositories based on analysis"""

    related = []
    repo_base_name = repo_name.lower()

    for other_repo in all_repos:
        if other_repo['name'] == repo_name:
            continue

        other_name = other_repo['name'].lower()
        other_analysis = other_repo.get('analysis', {})

        # Same project family (e.g., fib0, fib0-code, fib0-remote)
        for prefix in ['fib0', 'sspr', 'fcag', 'tropical', 'claude']:
            if prefix in repo_base_name and prefix in other_name:
                related.append(other_repo['name'])
                continue

        # Frontend-Backend relationship
        if analysis.get('architecture_type') == 'frontend' and other_analysis.get('architecture_type') == 'backend':
            if any(word in repo_base_name for word in other_name.split('-')):
                related.append(other_repo['name'])

        # Shared technology stack
        shared_tech = set(analysis.get('tech_stack', [])) & set(other_analysis.get('tech_stack', []))
        if len(shared_tech) >= 2:
            related.append(other_repo['name'])

        # Same domain
        if analysis.get('domain') == other_analysis.get('domain') and analysis.get('domain') != "Other":
            # Limit to avoid too many connections
            if len(related) < 10:
                related.append(other_repo['name'])

    return list(set(related))[:8]  # Max 8 related repos


def update_repo_note_with_analysis(repo_name: str, analysis: Dict, related_repos: List[str]):
    """Update repository note with Claude's analysis and relationships"""

    note_path = REPOS_PATH / f"{repo_name}.md"
    if not note_path.exists():
        return

    with open(note_path, 'r') as f:
        content = f.read()

    # Find where to insert analysis (after Stats section)
    stats_end = content.find("## Recent Commits")
    if stats_end == -1:
        stats_end = content.find("## Notes")

    if stats_end == -1:
        return

    # Build analysis section
    analysis_section = f"\n## Analysis\n\n"
    analysis_section += f"**Domain**: {analysis.get('domain', 'Unknown')}\n"
    analysis_section += f"**Architecture**: {analysis.get('architecture_type', 'unknown')}\n"
    analysis_section += f"**Purpose**: {analysis.get('purpose', 'N/A')}\n\n"

    if analysis.get('tech_stack'):
        analysis_section += f"**Tech Stack**: {', '.join(analysis['tech_stack'])}\n\n"

    if analysis.get('suggested_tags'):
        analysis_section += f"**Tags**: {', '.join(f'#{tag}' for tag in analysis['suggested_tags'])}\n\n"

    # Add related repositories section
    if related_repos:
        analysis_section += f"## Related Repositories\n\n"
        for related in related_repos:
            analysis_section += f"- [[{related}]]\n"
        analysis_section += f"\n"

    # Insert analysis
    new_content = content[:stats_end] + analysis_section + content[stats_end:]

    with open(note_path, 'w') as f:
        f.write(new_content)


def create_obsidian_canvas(repos_with_analysis: List[Dict]):
    """Create Obsidian canvas file showing repository relationships"""

    GRAPHS_PATH.mkdir(parents=True, exist_ok=True)
    canvas_path = GRAPHS_PATH / "Repository Graph.canvas"

    # Group repositories by domain
    domains = {}
    for repo in repos_with_analysis:
        domain = repo['analysis'].get('domain', 'Other')
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(repo)

    # Create canvas nodes
    nodes = []
    edges = []

    y_offset = 0
    domain_positions = {}

    for domain, domain_repos in domains.items():
        # Create domain header node
        domain_node = {
            "id": f"domain-{domain.replace(' ', '-')}",
            "type": "text",
            "text": f"# {domain}",
            "x": 0,
            "y": y_offset,
            "width": 200,
            "height": 60,
            "color": "2"
        }
        nodes.append(domain_node)
        domain_positions[domain] = (0, y_offset + 80)

        # Create nodes for each repo in domain
        x_offset = 0
        for i, repo in enumerate(domain_repos):
            if i > 0 and i % 4 == 0:
                x_offset = 0
                y_offset += 150

            node = {
                "id": repo['name'],
                "type": "file",
                "file": f"Repositories/{repo['name']}.md",
                "x": 250 + (x_offset * 250),
                "y": y_offset + 80,
                "width": 220,
                "height": 100
            }
            nodes.append(node)

            # Create edges to related repos
            for related in repo.get('related_repos', []):
                edge = {
                    "id": f"{repo['name']}-{related}",
                    "fromNode": repo['name'],
                    "toNode": related,
                    "color": "4"
                }
                edges.append(edge)

            x_offset += 1

        y_offset += 200

    # Save canvas file
    canvas_data = {
        "nodes": nodes,
        "edges": edges
    }

    with open(canvas_path, 'w') as f:
        json.dump(canvas_data, f, indent=2)

    return canvas_path


def analyze_all_repositories():
    """Main function to analyze all repositories with Claude"""

    print("🔍 Analyzing repositories with Claude...\n")

    # Get all repository notes
    repo_files = list(REPOS_PATH.glob("*.md"))
    repo_files = [f for f in repo_files if f.name != "README.md"]

    print(f"Found {len(repo_files)} repositories to analyze\n")

    # Parse existing notes and prepare for analysis
    all_repos = []
    for repo_file in repo_files:
        with open(repo_file, 'r') as f:
            content = f.read()

        # Extract metadata
        repo_data = {
            'name': repo_file.stem,
            'description': '',
            'language': '',
            'topics': [],
            'recent_commits': []
        }

        # Simple parsing
        for line in content.split('\n'):
            if line.startswith('>'):
                repo_data['description'] = line.strip('> ').strip()
            elif 'Language**:' in line:
                repo_data['language'] = line.split('**:')[1].strip()
            elif line.startswith('- `') and '`' in line[3:]:
                # Commit line
                commit = line[3:].split('`')[0]
                message = line.split('`')[2].strip()
                repo_data['recent_commits'].append({'sha': commit, 'message': message})

        all_repos.append(repo_data)

    # Analyze each repository
    repos_with_analysis = []
    for i, repo_data in enumerate(all_repos, 1):
        print(f"[{i}/{len(all_repos)}] Analyzing {repo_data['name']}...")

        try:
            analysis = analyze_repo_with_claude(repo_data)
            repo_data['analysis'] = analysis
            repos_with_analysis.append(repo_data)
            print(f"  ✓ Domain: {analysis.get('domain', 'Unknown')}")
            print(f"  ✓ Tech: {', '.join(analysis.get('tech_stack', []))}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            repo_data['analysis'] = {}
            repos_with_analysis.append(repo_data)

    print(f"\n✓ Analyzed {len(repos_with_analysis)} repositories\n")

    # Find relationships
    print("🔗 Finding relationships between repositories...\n")
    for repo in repos_with_analysis:
        related = find_related_repos(
            repo['name'],
            repos_with_analysis,
            repo['analysis']
        )
        repo['related_repos'] = related
        if related:
            print(f"  {repo['name']}: {len(related)} relationships")

    # Update notes with analysis
    print(f"\n📝 Updating repository notes...\n")
    for repo in repos_with_analysis:
        update_repo_note_with_analysis(
            repo['name'],
            repo['analysis'],
            repo['related_repos']
        )
        print(f"  ✓ Updated {repo['name']}")

    # Create Obsidian canvas
    print(f"\n🎨 Creating Obsidian canvas visualization...\n")
    canvas_path = create_obsidian_canvas(repos_with_analysis)
    print(f"  ✓ Created {canvas_path}")

    # Create summary
    print(f"\n📊 Summary:\n")
    domains = {}
    for repo in repos_with_analysis:
        domain = repo['analysis'].get('domain', 'Other')
        domains[domain] = domains.get(domain, 0) + 1

    for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
        print(f"  {domain}: {count} repos")

    total_relationships = sum(len(r['related_repos']) for r in repos_with_analysis)
    print(f"\n  Total relationships: {total_relationships}")
    print(f"\n✅ Analysis complete!")
    print(f"\nView in Obsidian:")
    print(f"  • Repository Graph: {canvas_path}")
    print(f"  • Updated notes: {REPOS_PATH}/")
    print(f"  • Graph view: Cmd+G")


if __name__ == "__main__":
    analyze_all_repositories()
