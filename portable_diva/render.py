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
