#!/usr/bin/env python3
"""
OpenCode Chat History Wiper - Standalone tool to clear chat history while preserving credentials

This tool safely truncates OpenCode session logs and chat history while
protecting authentication credentials, API tokens, and permission settings.

Usage: python opencode-chat-history-wiper.py [OPTIONS]

Features:
- Interactive confirmation by default
- Non-interactive mode with --auto flag for automation
- Comprehensive logging of actions
- Automatic backup creation
- Detailed summary of operations
"""

import sqlite3
import shutil
from pathlib import Path
import time
import sys
import argparse

def create_backup(db_path):
    """Create a backup of the database before making changes"""
    timestamp = int(time.time())
    backup_path = db_path.with_suffix(f".backup_{timestamp}.db")
    print(f"📁 Creating backup: {backup_path}")
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup created successfully")
        return backup_path
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
        return None

def truncate_table(conn, table_name):
    """Safely truncate a table"""
    try:
        cursor = conn.cursor()
        # Simple delete without VACUUM in transaction
        cursor.execute(f"DELETE FROM {table_name};")
        print(f"✅ Truncated table: {table_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to truncate table {table_name}: {e}")
        return False

def get_table_row_count(conn, table_name):
    """Get the row count of a table"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"❌ Failed to get row count for {table_name}: {e}")
        return 0

def analyze_database(db_path):
    """Analyze and display database structure"""
    if not db_path.exists():
        print("❌ Database file not found!")
        return None, None
        
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Define tables to preserve (credentials, permissions, etc.)
        preserve_tables = {
            'account': 'Authentication accounts',
            'control_account': 'OAuth control accounts', 
            'credential': 'API credentials and integrations',
            'permission': 'Permission settings',
        }
        
        # Define tables to truncate (session logs, chat history)
        truncate_tables = {
            'session_inbox': 'Session inbox messages',
            'session_message': 'Chat messages and conversation history',
            'session_v2': 'Session metadata and state',
        }
        
        return tables, {'preserve': preserve_tables, 'truncate': truncate_tables}
    except Exception as e:
        print(f"❌ Failed to analyze database: {e}")
        return None, None
    finally:
        conn.close()

def display_summary(tables, table_categories):
    """Display comprehensive summary of what will be modified"""
    preserve_tables = table_categories['preserve']
    truncate_tables = table_categories['truncate']
    
    print("\n" + "=" * 70)
    print("📋 DATABASE ANALYSIS SUMMARY")
    print("=" * 70)
    
    print("\n🔐 TABLES TO PRESERVE (WILL NOT BE MODIFIED):")
    print("-" * 50)
    preserved_count = 0
    for table, description in preserve_tables.items():
        if table in tables:
            # Need to create temporary connection for row count
            db_path = Path.home() / ".local/share/opencode/opencode.db"
            conn = sqlite3.connect(str(db_path))
            row_count = get_table_row_count(conn, table)
            conn.close()
            preserved_count += 1
            print(f"✅ {table:<25} ({row_count:>8,} rows) - {description}")
        else:
            print(f"❌ {table:<25} - NOT FOUND")
    
    print(f"\n📊 Total tables preserved: {preserved_count}")
    
    print("\n🗑️  TABLES TO WIPE (SESSION LOGS/CHAT HISTORY):")
    print("-" * 50)
    wiped_count = 0
    total_rows_to_wipe = 0
    
    db_path = Path.home() / ".local/share/opencode/opencode.db"
    conn = sqlite3.connect(str(db_path))
    
    for table, description in truncate_tables.items():
        if table in tables:
            row_count = get_table_row_count(conn, table)
            total_rows_to_wipe += row_count
            wiped_count += 1
            print(f"⚠️  {table:<25} ({row_count:>8,} rows) - {description}")
        else:
            print(f"❌ {table:<25} - NOT FOUND")
    
    conn.close()
    print(f"\n📊 Total tables to wipe: {wiped_count}")
    print(f"📊 Total rows to be deleted: {total_rows_to_wipe:,}")
    
    print("\n" + "=" * 70)
    print("⚠️  WARNING: This will permanently delete all chat history and session logs!")
    print("🔐 Your authentication credentials and API tokens will be preserved.")
    print("=" * 70)
    print(f"\n📁 Backup will be created at: {db_path.with_suffix('.backup_[timestamp].db')}")

def confirm_action():
    """Get user confirmation for destructive action"""
    print("\n❓ Do you want to proceed with wiping chat history?")
    print("   This action cannot be undone without the backup!")
    
    if sys.stdin.isatty():
        # Interactive mode
        confirm = input("   Enter 'yes' to confirm: ").strip().lower()
        return confirm in ['yes', 'y']
    else:
        # Non-interactive mode - auto-proceed with warning
        print("\n⚠️  WARNING: Running in non-interactive mode!")
        print("   Operation will proceed automatically without confirmation.")
        return True

def main():
    parser = argparse.ArgumentParser(
        description="OpenCode Chat History Wiper - Clear chat logs while preserving credentials"
    )
    parser.add_argument(
        '--auto', 
        action='store_true',
        help='Non-interactive mode - proceed without confirmation'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true', 
        help='Analyze database but do not make changes'
    )
    parser.add_argument(
        '--db-path',
        type=str,
        default=str(Path.home() / ".local/share/opencode/opencode.db"),
        help='Path to OpenCode database file'
    )
    
    args = parser.parse_args()
    
    db_path = Path(args.db_path)
    
    print("=" * 70)
    print("🔧 OpenCode Chat History Wiper - Version 2.0")
    print("=" * 70)
    print(f"Database path: {db_path}")
    
    # Analyze database
    tables, table_categories = analyze_database(db_path)
    if tables is None:
        return
    
    # Display summary
    display_summary(tables, table_categories)
    
    if args.dry_run:
        print("\n🧪 DRY RUN MODE - No changes will be made")
        return
    
    # Create backup
    backup_path = create_backup(db_path)
    if backup_path is None:
        print("❌ Cannot proceed without backup. Operation cancelled.")
        return
    
    # Get confirmation unless --auto flag is used
    if not args.auto:
        if not confirm_action():
            print("\n❌ Operation cancelled by user.")
            return
    
    # Connect to database
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    
    try:
        # Truncate tables
        print("\n🔧 Starting wipe operation...")
        success_count = 0
        
        truncate_tables = table_categories['truncate']
        
        for table in truncate_tables.keys():
            if table in tables:
                if truncate_table(conn, table):
                    success_count += 1
            else:
                print(f"❌ Table {table} not found, skipping")
        
        print(f"\n✅ Operation completed: {success_count} tables wiped successfully")
        print(f"📁 Backup available at: {backup_path}")
        print("\n🎉 Chat history has been successfully cleared!")
        print("   Your OpenCode session is now fresh with no chat history.")
        
    except Exception as e:
        print(f"\n❌ Error during operation: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()