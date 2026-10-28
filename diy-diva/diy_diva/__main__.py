"""Command line: python -m diy_diva {giochi,valida,ricetta,verifica} ..."""

import argparse
import json
import sys
from pathlib import Path

from . import engine, model, render


def main(argv=None):
    parser = argparse.ArgumentParser(prog="diy_diva", description="Avatar portabili tra giochi.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("giochi", help="elenca gli adattatori disponibili")
    valida = sub.add_parser("valida", help="controlla un file avatar")
    valida.add_argument("avatar", type=Path)
    ricetta = sub.add_parser("ricetta", help="genera la ricetta per un gioco")
    ricetta.add_argument("avatar", type=Path)
    ricetta.add_argument("--gioco", required=True, help="id dell'adattatore (vedi 'giochi')")
    ricetta.add_argument("-o", "--output", type=Path, help="scrivi la ricetta su file invece che a schermo")
    verifica = sub.add_parser("verifica", help="scheda da compilare per verificare un adattatore in gioco")
    verifica.add_argument("--gioco", required=True, help="id dell'adattatore (vedi 'giochi')")
    verifica.add_argument("-o", "--output", type=Path, help="scrivi la scheda su file invece che a schermo")
    args = parser.parse_args(argv)

    if args.command == "giochi":
        for game_id in engine.list_adapters():
            adapter = engine.load_adapter(game_id)
            status = "verificato" if adapter.get("verified") else "da verificare"
            print(f"{game_id:28} {adapter['game']} ({status})")
        return 0

    if args.command == "verifica":
        try:
            adapter = engine.load_adapter(args.gioco)
        except KeyError as exc:
            print(exc.args[0], file=sys.stderr)
            return 1
        _emit(render.to_checklist(adapter), args.output)
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
    _emit(render.to_markdown(engine.build_recipe(avatar, adapter)), args.output)
    return 0


def _emit(text, output):
    if output:
        output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    sys.exit(main())
