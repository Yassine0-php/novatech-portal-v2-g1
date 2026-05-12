from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"
DATA_DIR = BASE_DIR / "data"
AUDIT_PATH = BASE_DIR / "audit.md"

REQUIRED_HTML_FILES = [
    "index.html",
    "methodology.html",
    "tickets.html",
    "report.html",
]

REQUIRED_DATA_FILES = [
    "tickets.csv",
    "report.json",
]

def check_required_files():
    issues = []

    for filename in REQUIRED_HTML_FILES:
        path = WEB_DIR / filename

        if not path.exists():
            issues.append(f"Fichier HTML manquant : web/{filename}")

    for filename in REQUIRED_DATA_FILES:
        path = DATA_DIR / filename

        if not path.exists():
            issues.append(f"Fichier data manquant : data/{filename}")

    return issues 


def main():
    results = {
        "Fichiers requis": check_required_files(),
        "Liens internes": check_internal_links(),
        "CSV tickets": check_tickets_csv(),
        "JSON rapport": check_report_json(),
        "Contenus sensibles": check_sensitive_content(),
    }

    write_audit_report(results)

    print(f"Audit terminé : {AUDIT_PATH}")


if __name__ == "__main__":
    main()