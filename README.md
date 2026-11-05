# OpenCode Chat History Wiper

A standalone tool to clear OpenCode chat history and session logs while preserving authentication credentials and API integrations.

## Overview

The OpenCode Chat History Wiper safely truncates session logs and conversation history while protecting:

- **Authentication accounts** (`account` table)
- **OAuth control accounts** (`control_account` table)  
- **API credentials and integrations** (`credential` table)
- **Permission settings** (`permission` table)

This ensures your OpenCode authentication remains intact while giving you a clean slate for fresh conversations.

## Features

- ✅ **Safe operation** - Creates automatic backups before making changes
- ✅ **Interactive confirmation** - Prompts for confirmation by default
- ✅ **Non-interactive mode** - `--auto` flag for automation
- ✅ **Dry run support** - `--dry-run` to analyze without making changes
- ✅ **Detailed logging** - Comprehensive output showing what will be modified
- ✅ **Flexible database path** - Custom database location support via `--db-path`
- ✅ **Cross-platform** - Works on Linux, macOS, and Windows

## Usage

### Basic Usage

```bash
# Interactive mode (default) - prompts for confirmation
python opencode-chat-history-wiper.py

# Non-interactive mode - proceeds automatically
python opencode-chat-history-wiper.py --auto

# Analyze database without making changes
python opencode-chat-history-wiper.py --dry-run
```

### Advanced Usage

```bash
# Specify custom database location
python opencode-chat-history-wiper.py --db-path "/path/to/custom/opencode.db"

# Combined options
python opencode-chat-history-wiper.py --auto --dry-run
```

## Installation

### From Source

1. Clone this repository
2. Ensure Python 3.6+ is installed
3. Run the script directly

### Quick Start

```bash
# Make the script executable
chmod +x opencode-chat-history-wiper.py

# Run the tool
./opencode-chat-history-wiper.py
```

## How It Works

1. **Analyzes the database** - Identifies all tables and categorizes them
2. **Creates a backup** - Automatic backup with timestamp before any changes
3. **Shows summary** - Detailed breakdown of what will be preserved vs. wiped
4. **Gets confirmation** - Waits for user approval (unless using `--auto`)
5. **Wipes session logs** - Truncates `session_inbox`, `session_message`, and `session_v2` tables
6. **Reports results** - Shows success count and backup location

## Safety Features

- **Automatic backups** - Every operation creates a timestamped backup
- **Read-only analysis** - `--dry-run` mode shows exactly what will be changed
- **Preserved credentials** - Critical authentication data is never modified
- **Error handling** - Graceful error handling with rollback on failure
- **Interactive confirmation** - Prevents accidental data loss

## Files Modified

### Tables to Preserve

| Table Name | Purpose | Preserved |
|------------|---------|-----------|
| `account` | Authentication accounts | ✅ |
| `control_account` | OAuth control accounts | ✅ |
| `credential` | API credentials and integrations | ✅ |
| `permission` | Permission settings | ✅ |

### Tables to Wipe

| Table Name | Purpose | Action |
|------------|---------|--------|
| `session_inbox` | Session inbox messages | 🗑️ Wiped |
| `session_message` | Chat messages and conversation history | 🗑️ Wiped |
| `session_v2` | Session metadata and state | 🗑️ Wiped |

## Recovery

If you need to restore session logs from the backup:

```bash
# Copy backup back to original database
cp /path/to/opencode.db.backup_[timestamp].db /path/to/opencode.db
```

> **Note**: You must restart OpenCode after restoration for it to take effect.

## Examples

### Clearing All Chat History

```bash
python opencode-chat-history-wiper.py
```

### Automated Cleanup (Scripts)

```bash
# Add to crontab for daily cleanup at 2 AM
0 2 * * * /path/to/opencode-chat-history-wiper.py --auto
```

### CI/CD Pipeline Check

```bash
# Pre-deployment check in your CI pipeline
python opencode-chat-history-wiper.py --dry-run
```

## System Requirements

- **Python**: 3.6 or higher
- **SQLite**: Included with Python (standard library)
- **Disk Space**: Sufficient space for database backup
- **Permissions**: Write access to database file location

## Troubleshooting

### Common Issues

#### "Database file not found"
```bash
# Check if OpenCode is using the default database location
ls -la ~/.local/share/opencode/opencode.db
```

#### "Permission denied"
```bash
# Ensure you have write permissions to the database file
chmod 600 ~/.local/share/opencode/opencode.db
```

#### "Operation cancelled by user"
```bash
# Use the --auto flag for automated execution
python opencode-chat-history-wiper.py --auto
```

### Get Help

```bash
python opencode-chat-history-wiper.py --help
```

## Development

### Running Tests

```bash
# Basic functionality test
python -c "from opencode_chat_history_wiper import create_backup, truncate_table; print('Import successful')"
```

### Contributing

1. Fork this repository
2. Create a feature branch
3. Follow the existing code style
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Original author: OpenCode Team
- Enhanced by: [Your Name]

## Acknowledgements

- Thanks to the OpenCode community for their feedback
- Inspired by the need for safe session log management
- Based on the original clear_session_logs.py script

## Support

For issues or questions:

1. Check the latest documentation
2. Review the troubleshooting section
3. Create an issue in this repository
4. Contact the maintainers through the project channels

---

*Last updated: $(date)*
*Version: 2.0*