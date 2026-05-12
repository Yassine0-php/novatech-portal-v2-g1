import html
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "novatech.db"
OUTPUT_PATH = BASE_DIR / "web" / "tickets-data.html"


def get_tickets():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, priority, status, assignee, category
        FROM tickets
        ORDER BY category, priority, id
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def generate_html(rows):
    lines = []

    for ticket_id, title, priority, status, assignee, category in rows:
        assignee = assignee or "Non assigné"

        lines.append("          <article class=\"ticket-card\">")
        lines.append("            <div class=\"ticket-header\">")
        lines.append(f"              <span class=\"ticket-id\">{html.escape(ticket_id)}</span>")
        lines.append(f"              <span class=\"ticket-priority\">{html.escape(priority)}</span>")
        lines.append("            </div>")
        lines.append(f"            <h3>{html.escape(title)}</h3>")
        lines.append(f"            <p>Catégorie : {html.escape(category)}</p>")
        lines.append("            <div class=\"ticket-footer\">")
        lines.append(f"              <span>{html.escape(status)}</span>")
        lines.append(f"              <span>{html.escape(assignee)}</span>")
        lines.append("            </div>")
        lines.append("          </article>")

    return "\n".join(lines)


def main():
    if not DB_PATH.exists():
        print(f"Erreur : base introuvable : {DB_PATH}")
        print("Lancez d'abord : python scripts/init_db.py")
        return

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = get_tickets()
    html_content = generate_html(rows)

    OUTPUT_PATH.write_text(html_content, encoding="utf-8")

    print(f"Export terminé : {OUTPUT_PATH}")
    print(f"Tickets exportés : {len(rows)}")


if __name__ == "__main__":
    main()