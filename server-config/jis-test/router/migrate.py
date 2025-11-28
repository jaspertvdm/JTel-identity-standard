#!/usr/bin/env python3
"""
Database migration tool for JIS Router
Applies SQL migrations in order from the migrations/ directory
"""
import os
import sys
from pathlib import Path

import psycopg


def get_db_connection():
    """Get database connection from environment variables"""
    dsn = f"host={os.getenv('PGHOST', 'localhost')} " \
          f"port={os.getenv('PGPORT', '5432')} " \
          f"dbname={os.getenv('PGDATABASE', 'jis')} " \
          f"user={os.getenv('PGUSER', 'jis')} " \
          f"password={os.getenv('PGPASSWORD', 'jis')}"
    return psycopg.connect(dsn)


def get_applied_migrations(conn):
    """Get list of already applied migration versions"""
    with conn.cursor() as cur:
        # Create migrations table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                applied_at TIMESTAMPTZ DEFAULT NOW(),
                description TEXT
            )
        """)
        conn.commit()

        # Get applied versions
        cur.execute("SELECT version FROM schema_migrations ORDER BY version")
        return {row[0] for row in cur.fetchall()}


def get_migration_files():
    """Get all migration files from migrations/ directory"""
    migrations_dir = Path(__file__).parent / "migrations"
    files = sorted(migrations_dir.glob("*.sql"))
    migrations = []

    for file in files:
        # Extract version from filename (e.g., 001_initial_schema.sql -> 1)
        try:
            version = int(file.stem.split("_")[0])
            migrations.append((version, file.stem.replace(f"{version:03d}_", ""), file))
        except (ValueError, IndexError):
            print(f"Warning: Skipping invalid migration file: {file.name}")
            continue

    return sorted(migrations, key=lambda x: x[0])


def apply_migration(conn, version, description, filepath):
    """Apply a single migration"""
    print(f"Applying migration {version}: {description}...")

    with open(filepath, 'r') as f:
        sql = f.read()

    with conn.cursor() as cur:
        # Execute migration
        cur.execute(sql)
        conn.commit()

    print(f"✓ Migration {version} applied successfully")


def main():
    """Run database migrations"""
    print("JIS Router Database Migration Tool")
    print("=" * 50)

    try:
        # Connect to database
        print("Connecting to database...")
        conn = get_db_connection()
        print("✓ Connected")

        # Get applied migrations
        applied = get_applied_migrations(conn)
        print(f"Applied migrations: {sorted(applied) if applied else 'none'}")

        # Get available migrations
        migrations = get_migration_files()
        print(f"Available migrations: {len(migrations)}")

        # Apply pending migrations
        pending = [m for m in migrations if m[0] not in applied]

        if not pending:
            print("\n✓ All migrations are up to date")
            return 0

        print(f"\nPending migrations: {len(pending)}")
        for version, description, filepath in pending:
            apply_migration(conn, version, description, filepath)

        print("\n✓ All migrations completed successfully")
        return 0

    except Exception as e:
        print(f"\n✗ Migration failed: {e}", file=sys.stderr)
        return 1

    finally:
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    sys.exit(main())
