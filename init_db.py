"""
LokLens — Database Initialization Script (init_db.py)

Purpose:
Connects to your MySQL server, executes 'schema.sql' to create the database,
tables, indexes, and seeds the Karnataka 2023 manifesto guarantees.

Usage:
1. Ensure your MySQL server service is running.
2. Create a '.env' file with your MySQL password (copy from .env.example).
3. Run: python init_db.py
"""

import os
import pymysql
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "loklens_db")

def run_init():
    print("=" * 60)
    print(" LokLens — MySQL Database Initialization")
    print("=" * 60)
    print(f"Connecting to MySQL server at {DB_HOST}:{DB_PORT} as user '{DB_USER}'...")

    try:
        # Step 1: Connect to MySQL Server (without database to allow creation)
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            charset="utf8mb4",
            autocommit=True
        )
        print("✓ Connected to MySQL Server successfully!")

    except pymysql.err.OperationalError as e:
        print("\n[!] Could not connect to MySQL Server.")
        print(f"    Error code: {e.args[0]}")
        print(f"    Details: {e.args[1]}")
        print("\nFix:")
        print("1. Check if MySQL is running (Windows Services -> MySQL).")
        print("2. Ensure your password is set correctly in '.env':")
        print("   DB_PASSWORD=your_actual_mysql_password")
        return False

    try:
        cursor = conn.cursor()

        # Step 2: Read schema.sql
        schema_path = "schema.sql"
        if not os.path.exists(schema_path):
            print(f"[!] '{schema_path}' not found in current folder.")
            return False

        print(f"Reading schema and seed data from '{schema_path}'...")
        with open(schema_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        # Step 3: Execute SQL commands
        # Split by semicolon, ignoring empty lines/comments
        statements = [stmt.strip() for stmt in sql_script.split(";") if stmt.strip()]

        for i, statement in enumerate(statements, 1):
            cursor.execute(statement)

        print(f"✓ Executed {len(statements)} SQL statements successfully!")

        # Step 4: Verify Table Counts
        cursor.execute("USE loklens_db;")
        cursor.execute("SELECT COUNT(*) FROM states;")
        states_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM promises;")
        promises_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sources;")
        sources_count = cursor.fetchone()[0]

        print("\nDatabase Verification Summary:")
        print(f"  • States Seeded:         {states_count}")
        print(f"  • Guarantees Seeded:     {promises_count}")
        print(f"  • Official Sources:      {sources_count}")
        print("\n✓ Database setup complete! Database 'loklens_db' is ready for LokLens.")
        return True

    except Exception as e:
        print(f"\n[!] SQL Execution Error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    run_init()
