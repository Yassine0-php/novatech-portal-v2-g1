
import json
import csv
import re
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


def check_internal_links():
    issues = []
    # Liste des fichiers HTML à scanner dans le dossier web
    html_files = list(WEB_DIR.glob("*.html"))

    # Noms des fichiers existants pour comparaison
    existing_files = [f.name for f in html_files]

    for file_path in html_files:
        content = file_path.read_text(encoding="utf-8")
        # Expression régulière pour trouver les href="page.html"
        links = re.findall(r'href="([^"|#|http][^"]*\.html)"', content)

        for link in links:
            # Nettoyage du chemin (gestion du ./ si présent)
            clean_link = link.replace("./", "")
            if clean_link not in existing_files:
                issues.append(f"Lien cassé dans {file_path.name} : '{link}' (fichier introuvable)")

    return issues

def check_tickets_csv():
    issues = []
    path = DATA_DIR / "tickets.csv"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if not row.get("id") or not row.get("priority"):
                    issues.append(f"Ligne {i + 1} : Donnée manquante dans tickets.csv")
    return issues


def check_report_json():
    issues = []
    path = DATA_DIR / "report.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            for zone in data:
                # Correction demandée : vérifier les valeurs négatives
                if zone.get("needs", 0) < 0:
                    issues.append(f"Zone {zone.get('zone')} : Valeur de besoins négative ({zone.get('needs')})")
    return issues


def check_sensitive_content():
    issues = []
    forbidden_words = ["password", "admin123", "secret"]
    for file in WEB_DIR.glob("*.*"):
        content = file.read_text(encoding="utf-8").lower()
        for word in forbidden_words:
            if word in content:
                issues.append(f"Mot sensible '{word}' trouvé dans {file.name}")
    return issues


def write_audit_report(results):
    with open(AUDIT_PATH, "w", encoding="utf-8") as f:
        f.write("# Rapport d'Audit NovaTech\n\n")
        for category, issues in results.items():
            f.write(f"## {category}\n")
            if not issues:
                f.write(" Aucune anomalie détectée\n")
            else:
                for issue in issues:
                    f.write(f"- {issue}\n")
            f.write("\n")






if __name__ == "__main__":
    main()