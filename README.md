# Claude Research Projects

> Systematic implementation of cutting-edge research papers using Claude Code on the Web with comprehensive monitoring, validation, and reproducibility.

## 🎯 Overview

This repository contains multiple research projects designed to maximize Claude Code on the Web credits through efficient, systematic implementation of academic papers across different domains.

### Research Domains

1. **AI/ML Research** - [heretic-enhancement](./projects/01-ai-ml-heretic-enhancement/) - Enhancing model ablation techniques
2. **Developer Tools** - [Coming Soon](./projects/02-devtools-TBD/)
3. **Data Processing** - [Coming Soon](./projects/03-data-processing-TBD/)
4. **Web/API Services** - [Coming Soon](./projects/04-web-api-TBD/)
5. **Scientific Computing** - [Coming Soon](./projects/05-scientific-computing-TBD/)

## 🏗️ Repository Structure

```
claude-research-projects/
├── projects/                      # Individual research projects
│   ├── 01-ai-ml-heretic-enhancement/
│   ├── 02-devtools-TBD/
│   ├── 03-data-processing-TBD/
│   ├── 04-web-api-TBD/
│   └── 05-scientific-computing-TBD/
├── .claude/                       # Claude Code configuration
│   ├── skills/                    # Custom skills for research
│   ├── prompts/                   # Optimized Claude Code on Web prompts
│   └── CLAUDE.md                  # Project context
├── monitoring/                    # Cross-project monitoring system
│   ├── dashboard/                 # Web-based monitoring dashboard
│   ├── cli/                       # Command-line monitoring tool
│   └── data/                      # Metrics and logs
├── infra/                         # Shared infrastructure
│   ├── docker/                    # Docker configurations
│   ├── scripts/                   # Utility scripts
│   └── templates/                 # Project templates
├── docs/                          # Documentation
│   ├── setup.md                   # Setup instructions
│   ├── prompting-guide.md         # Prompt optimization guide
│   └── paper-implementation.md    # Research implementation workflow
└── .env.example                   # Environment variable template
```

## 🚀 Quick Start

### Prerequisites

- Claude Code on the Web credits
- GitHub account (authenticated)
- Docker (optional, for containerized environments)
- Python 3.10+ (for monitoring tools)

### Setup

1. **Clone and configure:**
   ```bash
   git clone https://github.com/machiabeli/claude-research-projects.git
   cd claude-research-projects
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Install monitoring tools:**
   ```bash
   pip install -r monitoring/requirements.txt
   ```

3. **Start monitoring dashboard:**
   ```bash
   python monitoring/dashboard/app.py
   ```

4. **Launch first project:**
   ```bash
   cd projects/01-ai-ml-heretic-enhancement
   # Follow project-specific README
   ```

## 📊 Monitoring System

Track all research projects in real-time:

- **Dashboard**: `http://localhost:8050` - Web-based metrics visualization
- **CLI**: `python monitoring/cli/status.py` - Command-line status check

### Monitored Metrics

-  **Execution**: Running projects, completion status, error rates
- **Research Quality**: Papers analyzed, test coverage, documentation completeness
- **Cost & Credits**: Token usage, estimated credits remaining
- **Development Progress**: Git activity, cycle iterations, dependency health

## 🎓 Research Methodology

Each project follows a systematic approach:

1. **Paper Analysis** - Comprehensive review of 5-7 implementations
2. **MVP Implementation** - Working baseline with tests
3. **Iterative Enhancement** - Multiple improvement cycles
4. **Validation & Benchmarking** - Performance verification
5. **Documentation** - Reproducible results

## 📝 Environment Variables

See [.env.example](./.env.example) for complete configuration options.

Key variables:
- `CLAUDE_API_KEY` - Your Claude API key (if using programmatic access)
- `GITHUB_TOKEN` - GitHub personal access token
- `PROJECT_ROOT` - Absolute path to this repository
- `MONITORING_PORT` - Dashboard port (default: 8050)

## 🛠️ Custom Skills

This repository includes specialized Claude Code skills:

- `/research-paper-implementation` - Paper-to-code workflow
- `/ml-experimentation-framework` - ML experiment tracking
- `/scientific-validation` - Numerical verification

Skills are automatically available when using Claude Code in this directory.

## 📖 Documentation

- [Setup Guide](./docs/setup.md) - Detailed setup instructions
- [Prompting Guide](./docs/prompting-guide.md) - Optimizing Claude Code on Web prompts
- [Implementation Workflow](./docs/paper-implementation.md) - Research paper implementation process

## 🤝 Contributing

Each project is self-contained. To add a new research project:

1. Copy the template: `cp -r infra/templates/project-template projects/XX-domain-name`
2. Update the project README
3. Add to monitoring configuration
4. Create optimized Claude Code on Web prompt

## 📜 License

MIT License - See LICENSE file for details

## 🔗 Links

- [Claude Code Documentation](https://code.claude.com/docs)
- [Anthropic Research](https://www.anthropic.com/research)
- [Skills Repository](https://github.com/anthropics/skills)

---

**Status**: Active Development | **Last Updated**: 2025-11-22 | **Projects**: 1/5 Started
