#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: ./scripts/restore.sh <backup_file_path>"
    exit 1
fi

BACKUP_FILE="$1"
DB_FILE="leaderai.db"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "Restoring database from $BACKUP_FILE..."
cp "$BACKUP_FILE" "$DB_FILE"
echo "Database restored successfully."


