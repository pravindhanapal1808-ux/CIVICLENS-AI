import sqlite3


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_NAME = "civic_reports.db"


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue TEXT,
            description TEXT,
            severity TEXT,
            impact_score REAL,
            recommendation TEXT,
            location TEXT,
            latitude REAL,
            longitude REAL
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# ADD REPORT
# ============================================================

def add_report(
    issue,
    description,
    severity,
    impact_score,
    recommendation,
    location,
    latitude,
    longitude
):

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO reports
        (
            issue,
            description,
            severity,
            impact_score,
            recommendation,
            location,
            latitude,
            longitude
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        issue,
        description,
        severity,
        impact_score,
        recommendation,
        location,
        latitude,
        longitude
    ))

    connection.commit()
    connection.close()


# ============================================================
# GET ALL REPORTS
# ============================================================

def get_reports():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            issue,
            description,
            severity,
            impact_score,
            recommendation,
            location,
            latitude,
            longitude
        FROM reports
        ORDER BY id DESC
    """)

    reports = cursor.fetchall()

    connection.close()

    return reports