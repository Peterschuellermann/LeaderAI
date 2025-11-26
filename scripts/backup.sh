#!/bin/bash
set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
DB_FILE="leaderai.db"
BACKUP_FILE="$BACKUP_DIR/leaderai_backup_$TIMESTAMP.db"

mkdir -p "$BACKUP_DIR"

if [ -f "$DB_FILE" ]; then
    echo "Backing up SQLite database..."
    cp "$DB_FILE" "$BACKUP_FILE"
    echo "Backup created at $BACKUP_FILE"
else
    echo "Database file not found at $DB_FILE"
    exit 1
fi

# Clean up old backups (keep last 7 days)
find "$BACKUP_DIR" -name "leaderai_backup_*.db" -mtime +7 -delete


