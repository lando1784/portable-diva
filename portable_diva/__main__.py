"""Command line: python -m portable_diva {giochi,valida,ricetta} ..."""

import argparse
import json
import sys
from pathlib import Path

from . import engine, model, render


def main(argv=None):
    parser = argparse.ArgumentParser(prog="portable_diva", description="Avatar portabili tra giochi.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("giochi", help="elenca gli adattatori disponibili")
    valida = sub.add_parser("valida", help="controlla un file avatar")
    valida.add_argument("avatar", type=Path)
    ricetta = sub.add_parser("ricetta", help="genera la ricetta per un gioco")
    ricetta.add_argument("avatar", type=Path)
    ricetta.add_argument("--gioco", required=True, help="id dell'adattatore (vedi 'giochi')")
    ricetta.add_argument("-o", "--output", type=Path, help="scrivi la ricetta su file invece che a schermo")
    args = parser.parse_args(argv)

    if args.command == "giochi":
        for game_id in engine.list_adapters():
            adapter = engine.load_adapter(game_id)
            status = "verificato" if adapter.get("verified") else "da verificare"
            print(f"{game_id:24} {adapter['game']} ({status})")
        return 0

    avatar = json.loads(args.avatar.read_text(encoding="utf-8"))
    errors = model.validate(avatar)
    if errors:
        print("Avatar non valido:", *(f"  - {e}" for e in errors), sep="\n", file=sys.stderr)
        return 1
    if args.command == "valida":
        print(f"{avatar['name']}: avatar valido")
        return 0

    try:
        adapter = engine.load_adapter(args.gioco)
    except KeyError as exc:
        print(exc.args[0], file=sys.stderr)
        return 1
    text = render.to_markdown(engine.build_recipe(avatar, adapter))
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
