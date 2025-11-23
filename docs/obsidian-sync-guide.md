# Obsidian Auto-Sync Guide

Complete guide to automatically syncing all your GitHub repositories to Obsidian.

## Overview

This system creates and maintains Obsidian notes for every GitHub repository you own, with:

- 📊 Repository stats (stars, forks, issues)
- 📝 Recent commits
- 🔗 Links to GitHub and related projects
- 🏷️ Tags and topics for organization
- 📈 Automatic updates every 6 hours
- 🔄 Obsidian Git plugin integration

## Setup

### 1. Quick Setup (Recommended)

```bash
cd /Users/ma/claude-research-projects
./monitoring/cli/setup_auto_sync.sh
```

This script will:
- Install dependencies (PyGithub)
- Create launchd agent for periodic sync
- Set up git hooks
- Run initial sync
- Configure Obsidian Git plugin (if installed)

### 2. Manual Setup

If you prefer manual setup:

```bash
# Install dependencies
pip install PyGithub python-dotenv

# Run first sync
python monitoring/cli/repo_sync.py

# Set up periodic sync (macOS)
# Copy the launchd plist from setup script
```

## How It Works

### Automatic Sync Triggers

1. **Periodic (Every 6 hours)**
   - Runs via macOS launchd
   - Syncs all repos automatically
   - Logs to `/tmp/obsidian-repo-sync.log`

2. **Post-Commit Hook**
   - Runs after every git commit in this repo
   - Updates research project notes
   - Background process (non-blocking)

3. **Manual Trigger**
   ```bash
   python monitoring/cli/repo_sync.py
   ```

### Obsidian Git Plugin

The system works perfectly with [Obsidian Git](https://github.com/denolehov/obsidian-git):

**Recommended Settings:**
- Auto pull: Every 10 minutes
- Auto commit: Every 30 minutes
- Auto push: Every 60 minutes
- Pull updates on startup: ON

This creates a full sync loop:
1. repo_sync.py updates Obsidian vault
2. Obsidian Git commits changes
3. Obsidian Git pushes to cloud
4. Obsidian Git pulls on other devices

## Vault Structure

```
Vault/
├── Repositories/              # All repository notes
│   ├── README.md             # Index of all repos
│   ├── claude-research-projects.md
│   ├── heretic.md
│   └── ... (all your repos)
├── Research/                  # Research projects
│   └── Heretic Enhancement/
│       ├── README.md
│       └── Paper 1-6.md
└── Daily Notes/              # Daily logs
    └── 2025-11-22.md
```

## Repository Note Format

Each repository gets a note like this:

```markdown
---
tags: [repository, github, python]
topics: [machine-learning, research]
repo: machiabeli/claude-research-projects
updated: 2025-11-22T21:10:00
stars: 5
forks: 2
---

# claude-research-projects

> Systematic implementation of cutting-edge research papers

## Quick Links

- 🔗 [GitHub](https://github.com/machiabeli/claude-research-projects)
- 📁 [Clone URL](https://github.com/machiabeli/claude-research-projects.git)

## Stats

- **Language**: Python
- **Stars**: ⭐ 5
- **Forks**: 🍴 2
- **Issues**: 🐛 3
- **Last Updated**: 2025-11-22 21:00

## Recent Commits

- `7cb5b00` feat: create Obsidian research folder (2025-11-22)
- `52f162e` fix: update Obsidian vault path (2025-11-22)
...

## Related Notes

- [[Research]]
- [[Heretic Enhancement]]

## Notes

(Your personal notes here)
```

## Graph View

In Obsidian's graph view, you'll see:

```
         [Repositories/README]
               (hub)
                 |
     ┌───────┬──┴──┬───────┐
     |       |     |       |
[Python] [TypeScript] [Rust] ...
  repos     repos      repos
     |
     └─→ [Research Projects]
            └─→ [Papers]
```

### Graph Features

- **Color by tag**: `#repository`, `#research`, `#paper`
- **Filter by language**: Show only Python repos
- **Group by topic**: Find related projects
- **Link navigation**: Jump between related repos

## Customization

### Environment Variables

Add to your `.env`:

```bash
# Sync frequency (seconds, default: 21600 = 6 hours)
REPO_SYNC_INTERVAL=21600

# Which repos to include
REPO_SYNC_FILTER=all  # or: owned, contributed, forked

# Include private repos
REPO_SYNC_PRIVATE=true

# Obsidian paths (already configured)
OBSIDIAN_VAULT_PATH=/Users/ma/Vault
OBSIDIAN_REPOS_PATH=${OBSIDIAN_VAULT_PATH}/Repositories
```

### Custom Templates

Edit `monitoring/cli/repo_sync.py` to customize the note format:

```python
def create_repo_note(repo) -> Path:
    # Modify content generation here
    content = f"# {repo.name}\n\n"
    # Add your custom sections
    ...
```

## Troubleshooting

### Sync Not Running

Check launchd status:
```bash
launchctl list | grep obsidian-repo-sync
```

View logs:
```bash
tail -f /tmp/obsidian-repo-sync.log
tail -f /tmp/obsidian-repo-sync.err
```

Restart service:
```bash
launchctl unload ~/Library/LaunchAgents/com.user.obsidian-repo-sync.plist
launchctl load ~/Library/LaunchAgents/com.user.obsidian-repo-sync.plist
```

### GitHub Authentication

The script tries to authenticate in this order:

1. `GITHUB_TOKEN` environment variable
2. GitHub CLI (`gh auth token`)
3. Manual token input

Generate a token at: https://github.com/settings/tokens

Required scopes: `repo`, `read:org`

### Obsidian Git Not Syncing

1. Check plugin is enabled: Settings → Community Plugins
2. Verify settings: Settings → Obsidian Git
3. Check git status in vault:
   ```bash
   cd /Users/ma/Vault
   git status
   ```

## Advanced Usage

### Filter Repositories

Only sync specific repos:

```python
# In repo_sync.py
def get_all_repos() -> List:
    repos = list(user.get_repos())
    # Filter to only active repos
    return [r for r in repos if not r.archived and r.updated_at > cutoff_date]
```

### Add Custom Metadata

Track additional metrics:

```python
# Add to create_repo_note()
content += f"- **Contributors**: {repo.get_contributors().totalCount}\n"
content += f"- **Watchers**: {repo.watchers_count}\n"
content += f"- **Open PRs**: {len(list(repo.get_pulls(state='open')))}\n"
```

### Link to Projects

Automatically detect project relationships:

```python
# In create_repo_note()
if "backend" in repo.name:
    content += f"- Related: [[frontend]], [[api-docs]]\n"
```

## Best Practices

1. **Review Generated Notes**: Add personal context to the "Notes" section
2. **Use Tags**: Add custom tags for organization (#work, #personal, #learning)
3. **Link Related Projects**: Connect repos that work together
4. **Update Frequency**: 6 hours balances freshness vs API rate limits
5. **Backup**: Obsidian Git pushes your vault to GitHub automatically

## Examples

### Research Workflow

1. Start new research project
2. Sync creates repo note in Obsidian
3. Add research notes to the repo note
4. Link papers and experiments
5. Graph view shows connections

### Multi-Repo Projects

1. Create a project hub note
2. Link all related repo notes
3. Track progress across repos
4. Unified view in graph

### Portfolio Management

1. All repos auto-indexed by language
2. Star counts tracked over time
3. Active vs archived visible
4. Topics grouped automatically

## FAQ

**Q: How many API calls does this use?**
A: ~1-2 calls per repo. GitHub allows 5000/hour (authenticated).

**Q: Will this work with private repos?**
A: Yes, if your token has `repo` scope.

**Q: Can I sync organization repos?**
A: Yes, modify `get_all_repos()` to include org repos.

**Q: Does this support GitLab/Bitbucket?**
A: Currently GitHub only. PRs welcome for other platforms!

**Q: Will this slow down Obsidian?**
A: No. Notes are standard markdown. Thousands of notes work fine.

## Resources

- [Obsidian Git Plugin](https://github.com/denolehov/obsidian-git)
- [PyGithub Docs](https://pygithub.readthedocs.io/)
- [GitHub API](https://docs.github.com/en/rest)
- [Obsidian Graph View](https://help.obsidian.md/Plugins/Graph+view)

## Support

Issues? Open an issue at: https://github.com/machiabeli/claude-research-projects/issues
