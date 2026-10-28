"""Render a recipe as Markdown."""


def to_markdown(recipe):
    lines = [f"# {recipe['avatar']} → {recipe['game']}", ""]
    if not recipe["verified"]:
        lines += ["> ⚠️ Adattatore non ancora verificato in gioco: nomi delle voci e intervalli "
                  "potrebbero non corrispondere esattamente all'editor.", ""]
    for note in recipe["notes"]:
        lines.append(f"- {note}")
    if recipe["notes"]:
        lines.append("")
    for section in recipe["sections"]:
        lines += [f"## {section['title']}", "", "| Voce | Impostazione | Perché |", "|---|---|---|"]
        for row in section["rows"]:
            lines.append(f"| {_cell(row['label'])} | {_cell(row['setting'])} | {_cell(row['reason'])} |")
        lines.append("")
    return "\n".join(lines)


def _cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


_CHECKS = {
    "slider": "nome nel gioco: ____ · mostra un numero? intervallo: ____ · il predefinito è al centro? sì/no",
    "choice": "nome nel gioco: ____ · numero di opzioni: ____",
    "color": "nome nel gioco: ____ · palette fissa (quanti colori: ____) o selettore libero?",
    "toggle": "nome nel gioco: ____ · è un sì/no o ha un'intensità?",
    "weights": "nome nel gioco: ____ · com'è fatto il controllo (triangolo, slider separati...)?",
    "list": "nome nel gioco: ____ · quali tipi e zone sono disponibili?",
    "note": "nome nel gioco: ____",
}


def to_checklist(adapter):
    """A fill-in sheet to verify an adapter while sitting in the game's editor."""
    lines = [
        f"# Verifica: {adapter['game']}", "",
        "Compila questa scheda con l'editor del gioco aperto. Spunta ogni voce che trovi, correggi i nomi "
        "e scrivi \"non esiste\" dove serve. Le foto dei menu sono benvenute.", "",
        "## Domande generali", "",
        "- [ ] Versione / piattaforma del gioco: ____",
        "- [ ] Gli slider mostrano valori numerici? Se sì, che intervallo hanno? ____",
        "- [ ] Le voci da non poter cambiare dopo la creazione: ____",
        "- [ ] Voci presenti nel gioco ma assenti qui sotto: ____",
        "",
    ]
    for section in adapter["sections"]:
        lines += [f"## {section['title']}", ""]
        for control in section["controls"]:
            lines.append(f"- [ ] **{control['label']}** — {_CHECKS[control['type']]}")
        lines.append("")
    return "\n".join(lines)
