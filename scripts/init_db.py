import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "data" / "tickets.csv"
DB_PATH = BASE_DIR / "data" / "novatech.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

if not CSV_PATH.exists():
    print(f"Erreur : fichier introuvable : {CSV_PATH}")
    exit(1)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS tickets")

cursor.execute("""
CREATE TABLE tickets (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    assignee TEXT,
    category TEXT NOT NULL
)
""")

with open(CSV_PATH, encoding="utf-8") as file:
    reader = csv.DictReader(file)

    rows = []

    for row in reader:
        rows.append((
            row["id"],
            row["title"],
            row["priority"],
            row["status"],
            row["assignee"],
            row["category"]
        ))

cursor.executemany("""
INSERT INTO tickets (
    id,
    title,
    priority,
    status,
    assignee,
    category
)
VALUES (?, ?, ?, ?, ?, ?)
""", rows)

conn.commit()

ticket_count = cursor.execute(
    "SELECT COUNT(*) FROM tickets"
).fetchone()[0]

conn.close()

print(f"Base SQLite générée : {DB_PATH}")
print(f"Tickets importés : {ticket_count}")