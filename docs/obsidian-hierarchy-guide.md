# Obsidian Vault Hierarchy Guide

Your vault is now organized with a circular hierarchical structure optimized for graph view visualization.

## 🏗️ Hierarchy Structure

```
🏠 Vault Home (Master MOC)
    ├── 📚 Research Hub
    │   ├── Heretic Enhancement
    │   │   ├── Paper 1 - Anthropic Persona Vectors
    │   │   ├── Paper 2 - Self-Ablating Transformers
    │   │   ├── Paper 3 - Representation Engineering
    │   │   ├── Paper 4 - Steering with Conceptors
    │   │   ├── Paper 5 - Safety Alignment Depth
    │   │   └── Paper 6 - Samba Hybrid SSM
    │   └── [Future research projects]
    │
    ├── 💻 Repositories Hub
    │   ├── Architecture Map
    │   ├── Repository Index (README)
    │   ├── Library (12 repos)
    │   ├── Frontend (8 repos)
    │   ├── Research (5 repos)
    │   ├── Fullstack (1 repo)
    │   └── Ecosystems
    │       ├── fib0 (5 repos)
    │       ├── sspr (3 repos)
    │       ├── fcag (2 repos)
    │       ├── tropical (2 repos)
    │       └── claude (2 repos)
    │
    ├── 📓 Daily Notes Hub
    │   ├── 2025-11-22
    │   ├── 2025-11-21
    │   └── [Daily notes...]
    │
    └── 🚀 Projects Hub
        ├── Heretic Enhancement
        ├── Repository Analysis System
        ├── Obsidian Integration
        └── Ecosystem Projects

```

## 🎨 Visual Maps (Canvas Files)

### 1. Vault Overview
**Location**: `Repositories/Graphs/Vault Overview.canvas`

Shows the complete hierarchy:
- Master Vault Home at center
- 4 hub nodes branching out
- Color-coded by domain
- Stats and monitoring information
- Circular connections back to home

### 2. Architecture Overview
**Location**: `Repositories/Graphs/Architecture Overview.canvas`

Repository architecture visualization:
- Grouped by architecture type (Library, Frontend, Research, Fullstack)
- Ecosystem circles (fib0, sspr, fcag, tropical, claude)
- Domain clusters
- Technology stack breakdown

### 3. Repository Graph
**Location**: `Repositories/Graphs/Repository Graph.canvas`

Detailed relationship network:
- All 26 repositories as nodes
- 99 cross-repository connections
- Organized by domain clusters
- Related repositories connected with edges

## 🔗 Navigation Pattern

### Circular Hierarchy

Every note has bidirectional links creating circles:

```
🏠 Vault Home
    ↓ (click hub link)
📚 Research Hub
    ↓ (click project)
Heretic Enhancement
    ↓ (click paper)
Paper 1 - Anthropic Persona Vectors
    ↑ (click "← Research Hub" at top)
📚 Research Hub
    ↑ (click "← Vault Home" at top)
🏠 Vault Home
```

### Quick Navigation

Every page has navigation breadcrumbs at the top:
- `← [[Hub Name|Hub]]` - Go up one level
- `← [[Hub|Hub]] | [[🏠 Vault Home|Home]]` - Go to hub or home

## 📊 Graph View Features

### View the Hierarchy

1. Open Obsidian
2. Press `Cmd+G` to open graph view
3. You'll see:
   - **Central Hub**: 🏠 Vault Home
   - **4 Major Circles**: Research, Repositories, Daily Notes, Projects
   - **Sub-circles**: Papers, repo ecosystems, daily entries
   - **Cross-connections**: 99 repository relationships

### Filter Options

Use graph view filters:
- **By tag**: `tag:#moc` shows only hub pages
- **By tag**: `tag:#repository` shows only repos
- **By tag**: `tag:#research` shows research content
- **By tag**: `tag:#paper` shows individual papers

### Color Coding

Hub pages use different colors in canvas:
- **Vault Home**: Purple (color 6)
- **Research Hub**: Green (color 3)
- **Repositories Hub**: Blue (color 2)
- **Daily Notes Hub**: Orange (color 4)
- **Projects Hub**: Red (color 5)

## 🏷️ Tag System

### Hub Tags
- `#moc` - Maps of Content (hub pages)
- `#hub` - Secondary hub identifier
- `#index` - Index pages

### Content Tags
- `#repository` - GitHub repositories
- `#research` - Research projects
- `#paper` - Academic papers
- `#daily` - Daily notes
- `#project` - Active projects

### Status Tags (Papers)
- `#pending` - Not started
- `#in-progress` - Currently implementing
- `#implemented` - Complete

### Architecture Tags (Repos)
- `#frontend` - Frontend applications
- `#backend` - Backend services
- `#library` - Reusable libraries
- `#research` - Research code
- `#fullstack` - Complete platforms

## 📈 Using the Hierarchy

### Starting Your Day

1. Open [[🏠 Vault Home|Vault Home]]
2. See overview of all areas
3. Navigate to relevant hub
4. Dive into specific content

### Finding Related Content

1. Open any note
2. Look at "Related" section
3. Click links to related notes
4. Use graph view to visualize connections

### Adding New Content

**New Repository** (auto-synced):
- Automatically appears in Repositories Hub
- Links to related repos added by analyzer
- Categorized by architecture and domain

**New Research Paper**:
1. Create note in Research folder
2. Add tags: `#research #paper #pending`
3. Link to [[📚 Research Hub|Research Hub]]
4. Add to relevant project folder

**New Project**:
1. Create note or folder
2. Add tag: `#project`
3. Link to [[🚀 Projects Hub|Projects Hub]]
4. Cross-link to related content

## 🎯 Graph View Patterns

### Hub-and-Spoke

Each hub creates a hub-and-spoke pattern:
- Hub at center
- Content radiates out
- Cross-connections between content
- Links back to master hub

### Ecosystems

Project ecosystems form tight clusters:
- fib0 repos tightly connected
- sspr repos form their own cluster
- fcag repos interconnected
- Visible as dense sub-graphs

### Cross-Domain Connections

Research ↔ Repositories:
- [[claude-research-projects]] connects both hubs
- [[heretic]] appears in both research and repos
- Papers link to implementation repos

## 📱 Mobile Usage

### Obsidian Mobile

The hierarchy works on mobile:
1. Hub pages have clear navigation
2. Breadcrumbs at top of every page
3. Canvas files viewable (pinch to zoom)
4. Graph view available

### Sync

With Obsidian Git plugin:
- Changes sync automatically
- Vault stays updated across devices
- Repository notes refresh every 6 hours

## 🔧 Maintenance

### Auto-Updated Content

These update automatically:
- Repository notes (every 6 hours)
- Architecture Map (when analyzer runs)
- Daily notes (when sync runs)

### Manual Updates

These require manual updates:
- Hub pages (edit as needed)
- Research project status
- Paper implementation progress
- Canvas visualizations

### Refresh Repository Data

```bash
# Manual sync
python3 monitoring/cli/repo_sync.py

# Re-analyze with Claude
python3 monitoring/cli/claude_repo_analyzer.py

# Rebuild architecture map
python3 monitoring/cli/create_architecture_map.py
```

## 💡 Tips

### Power User Features

1. **Local Graph**: Right-click any note → "Open local graph"
   - See just connections to that note
   - Explore nearby content

2. **Canvas as Dashboards**: Open canvas files for visual overviews
   - Vault Overview for complete picture
   - Architecture Overview for repo organization
   - Repository Graph for relationships

3. **Tag Search**: Click any tag to see all notes with that tag
   - Instant filtering
   - Discover related content

4. **Backlinks Panel**: View what links to current note
   - See all incoming connections
   - Understand note importance

### Customization

You can customize:
- Hub page content (add sections, links)
- Canvas layouts (move nodes, change colors)
- Tag system (add custom tags)
- Navigation links (add shortcuts)

### Best Practices

1. **Use Breadcrumbs**: Always navigate via breadcrumb links
2. **Check Graph View**: Regularly view graph to understand connections
3. **Tag Consistently**: Use standard tags for automatic organization
4. **Link Liberally**: Add `[[links]]` to related content
5. **Update Hubs**: Keep hub pages current with new content

## 🎨 Visual Reference

### Hub Node Colors in Canvas

```
🏠 Vault Home       → Purple (center)
📚 Research Hub     → Green  (left)
💻 Repositories Hub → Blue   (center-left)
📓 Daily Notes Hub  → Orange (center-right)
🚀 Projects Hub     → Red    (right)
```

### Architecture Colors

```
📚 Library   → Color 1 (red)
🎨 Frontend  → Color 2 (blue)
🔬 Research  → Color 3 (green)
🌐 Fullstack → Color 4 (orange)
```

## 📚 Summary

Your vault now has:
- **5 hub pages** creating hierarchical organization
- **3 canvas visualizations** for visual navigation
- **80+ notes** all interconnected
- **Circular navigation** for easy traversal
- **Auto-sync** keeping everything current
- **Graph view optimization** for visual exploration

**Start here**: Open [[🏠 Vault Home|Vault Home]] in Obsidian
**See hierarchy**: Press `Cmd+G` for graph view
**Visual overview**: Open `Vault Overview.canvas`

The hierarchy creates clear circles in the graph, making it easy to understand your knowledge structure at a glance!
