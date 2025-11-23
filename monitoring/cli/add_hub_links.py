#!/usr/bin/env python3
"""
Add hub navigation links to all repository notes for circular hierarchy in graph view
"""

from pathlib import Path

REPOS_PATH = Path("/Users/ma/Vault/Repositories")

def add_hub_link_to_repo(repo_path: Path):
    """Add navigation link to repository hub at top of repo note"""

    with open(repo_path, 'r') as f:
        content = f.read()

    # Check if link already exists
    if "← [[💻 Repositories Hub" in content or "← [[🏠 Vault Home" in content:
        return False  # Already has link

    # Find the end of frontmatter
    lines = content.split('\n')
    frontmatter_end = -1
    in_frontmatter = False

    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                frontmatter_end = i
                break

    if frontmatter_end == -1:
        print(f"  ⚠️  No frontmatter found in {repo_path.name}")
        return False

    # Find the title line (starts with #)
    title_line = -1
    for i in range(frontmatter_end + 1, len(lines)):
        if lines[i].startswith('# '):
            title_line = i
            break

    if title_line == -1:
        print(f"  ⚠️  No title found in {repo_path.name}")
        return False

    # Insert navigation link after title
    nav_link = "\n← [[💻 Repositories Hub|Repositories Hub]] | [[🏠 Vault Home|Home]]\n"
    lines.insert(title_line + 1, nav_link)

    # Write back
    new_content = '\n'.join(lines)
    with open(repo_path, 'w') as f:
        f.write(new_content)

    return True

def main():
    """Add hub links to all repository notes"""

    print("📝 Adding hub navigation links to repository notes...\n")

    updated = 0
    skipped = 0

    for repo_file in sorted(REPOS_PATH.glob("*.md")):
        if repo_file.name in ["README.md", "Architecture Map.md"]:
            continue

        if add_hub_link_to_repo(repo_file):
            print(f"  ✓ Updated {repo_file.stem}")
            updated += 1
        else:
            skipped += 1

    print(f"\n✅ Complete!")
    print(f"  Updated: {updated} files")
    print(f"  Skipped: {skipped} files (already had links)")
    print(f"\nGraph view will now show circular hierarchy:")
    print(f"  🏠 Vault Home → 💻 Repositories Hub → Individual Repos → Back to Hub")

if __name__ == "__main__":
    main()
