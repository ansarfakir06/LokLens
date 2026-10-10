"""
LokLens — Database Access Layer (db.py)

Purpose:
Handles MySQL database connections, executes queries for states, manifestos,
promises, and sources, and provides a safe in-memory fallback if the database
is not yet initialized or configured in .env.

Design Patterns Used:
- Environment Variables (12-Factor App config)
- Repository Pattern (Abstracts SQL queries from Flask routes)
- Graceful Degradation (Fallback store keeps app alive during onboarding)
"""

import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "loklens_db")

def get_connection():
    """
    Attempts to establish a connection to the MySQL database.
    Returns pymysql connection object, or None if connection fails.
    """
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor,
            charset="utf8mb4",
            connect_timeout=3
        )
        return connection
    except Exception as e:
        # Connection failed (e.g. password not set or database not created yet)
        return None

def is_db_connected():
    """Returns True if MySQL is reachable and initialized, False otherwise."""
    conn = get_connection()
    if conn:
        conn.close()
        return True
    return False

# ============================================================================
# DATABASE REPOSITORY FUNCTIONS
# ============================================================================

def get_states():
    """Fetches all states from MySQL database."""
    conn = get_connection()
    if not conn:
        return None  # Triggers fallback in caller

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, has_data, unverified_message FROM states ORDER BY name ASC")
            rows = cursor.fetchall()

            # Format for API
            states = []
            for row in rows:
                states.append({
                    "id": row["id"],
                    "name": row["name"],
                    "hasData": bool(row["has_data"]),
                    "guaranteeCount": 5 if row["id"] == "karnataka" else 0,
                    "message": row["unverified_message"]
                })
            return states
    except Exception as e:
        print(f"[DB Query Error in get_states]: {e}")
        return None
    finally:
        conn.close()

def get_administrations(state_id=None):
    """Fetches administrations from MySQL database."""
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            if state_id:
                cursor.execute(
                    """
                    SELECT a.id, a.state_id AS stateId, a.party_name AS party, a.term_years AS term,
                           m.title AS manifestoTitle, m.subtitle, m.document_path AS manifestoFile
                    FROM administrations a
                    LEFT JOIN manifestos m ON a.id = m.administration_id
                    WHERE a.state_id = %s
                    """,
                    (state_id,)
                )
            else:
                cursor.execute(
                    """
                    SELECT a.id, a.state_id AS stateId, a.party_name AS party, a.term_years AS term,
                           m.title AS manifestoTitle, m.subtitle, m.document_path AS manifestoFile
                    FROM administrations a
                    LEFT JOIN manifestos m ON a.id = m.administration_id
                    """
                )
            return cursor.fetchall()
    except Exception as e:
        print(f"[DB Query Error in get_administrations]: {e}")
        return None
    finally:
        conn.close()

def get_promises(state_id="karnataka", category="all", search=""):
    """Fetches filtered promises from MySQL."""
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            query = """
                SELECT id, state_id AS stateId, manifesto_id AS manifestoId, name,
                       category, category_label AS categoryLabel, status, status_label AS statusLabel,
                       summary, manifesto_quote AS manifestoQuote, implementation_details AS implementationDetails,
                       target_metric, delivered_metric, metric_type, reporting_period, last_updated,
                       data_notes AS dataNotes
                FROM promises
                WHERE state_id = %s
            """
            params = [state_id]

            if category and category != "all":
                query += " AND category = %s"
                params.append(category)

            if search:
                query += """ AND (
                    LOWER(name) LIKE %s OR 
                    LOWER(manifesto_quote) LIKE %s OR 
                    LOWER(summary) LIKE %s OR 
                    LOWER(target_metric) LIKE %s
                )"""
                term = f"%{search.lower()}%"
                params.extend([term, term, term, term])

            cursor.execute(query, params)
            rows = cursor.fetchall()

            promises = []
            for row in rows:
                # Fetch sources for this promise
                cursor.execute("""
                    SELECT s.id, s.title, s.url, s.source_type AS type
                    FROM sources s
                    JOIN promise_sources ps ON s.id = ps.source_id
                    WHERE ps.promise_id = %s
                """, (row["id"],))
                sources = cursor.fetchall()

                promises.append({
                    "id": row["id"],
                    "stateId": row["stateId"],
                    "manifestoId": row["manifestoId"],
                    "name": row["name"],
                    "category": row["category"],
                    "categoryLabel": row["categoryLabel"],
                    "status": row["status"],
                    "statusLabel": row["statusLabel"],
                    "summary": row["summary"],
                    "manifestoQuote": row["manifestoQuote"],
                    "implementationDetails": row["implementationDetails"],
                    "metrics": {
                        "target": row["target_metric"],
                        "delivered": row["delivered_metric"],
                        "metricType": row["metric_type"],
                        "reportingPeriod": row["reporting_period"],
                        "lastUpdated": row["last_updated"]
                    },
                    "dataNotes": row["dataNotes"],
                    "sources": sources
                })

            return promises
    except Exception as e:
        print(f"[DB Query Error in get_promises]: {e}")
        return None
    finally:
        conn.close()

def get_promise_by_id(promise_id):
    """Fetches a single detailed promise by ID from MySQL."""
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, state_id AS stateId, manifesto_id AS manifestoId, name,
                       category, category_label AS categoryLabel, status, status_label AS statusLabel,
                       summary, manifesto_quote AS manifestoQuote, implementation_details AS implementationDetails,
                       target_metric, delivered_metric, metric_type, reporting_period, last_updated,
                       data_notes AS dataNotes
                FROM promises
                WHERE id = %s
            """, (promise_id,))
            row = cursor.fetchone()
            if not row:
                return False  # explicitly not found

            # Fetch sources
            cursor.execute("""
                SELECT s.id, s.title, s.url, s.source_type AS type
                FROM sources s
                JOIN promise_sources ps ON s.id = ps.source_id
                WHERE ps.promise_id = %s
            """, (promise_id,))
            sources = cursor.fetchall()

            return {
                "id": row["id"],
                "stateId": row["stateId"],
                "manifestoId": row["manifestoId"],
                "name": row["name"],
                "category": row["category"],
                "categoryLabel": row["categoryLabel"],
                "status": row["status"],
                "statusLabel": row["statusLabel"],
                "summary": row["summary"],
                "manifestoQuote": row["manifestoQuote"],
                "implementationDetails": row["implementationDetails"],
                "metrics": {
                    "target": row["target_metric"],
                    "delivered": row["delivered_metric"],
                    "metricType": row["metric_type"],
                    "reportingPeriod": row["reporting_period"],
                    "lastUpdated": row["last_updated"]
                },
                "dataNotes": row["dataNotes"],
                "sources": sources
            }
    except Exception as e:
        print(f"[DB Query Error in get_promise_by_id]: {e}")
        return None
    finally:
        conn.close()

def get_sources():
    """Fetches all official documented sources from MySQL."""
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, title, url, source_type AS type FROM sources ORDER BY title ASC")
            return cursor.fetchall()
    except Exception as e:
        print(f"[DB Query Error in get_sources]: {e}")
        return None
    finally:
        conn.close()
