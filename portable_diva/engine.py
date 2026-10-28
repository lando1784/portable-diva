"""Translate a canonical avatar into a per-game recipe using an adapter file.

An adapter lists the editor's controls grouped in sections. Each control has a
type that tells the engine how to derive a setting from the canonical avatar:

  slider   continuous value -> slider position (percent of travel or min..max)
  choice   pick the closest catalogued option, or describe what to look for
  color    target colour, snapped to the game's palette when one is catalogued
  toggle   on/off from a boolean or a 0..1 trait above a threshold
  weights  blend of body.build (e.g. a triangle/barycentric body control)
  list     copy marks/accessories of the given types
  note     fixed advice
"""

import json
from pathlib import Path

from . import color, model

ADAPTERS_DIR = Path(__file__).resolve().parent.parent / "adapters"
DEFAULT = "lascia il valore predefinito"


def list_adapters():
    return sorted(p.stem for p in ADAPTERS_DIR.glob("*.json"))


def load_adapter(game_id):
    path = ADAPTERS_DIR / f"{game_id}.json"
    if not path.exists():
        raise KeyError(f"nessun adattatore per '{game_id}' (disponibili: {', '.join(list_adapters())})")
    return json.loads(path.read_text(encoding="utf-8"))


def build_recipe(avatar, adapter):
    sections = []
    for section in adapter["sections"]:
        rows = [_CONTROLS[c["type"]](avatar, c) for c in section["controls"]]
        sections.append({"title": section["title"], "rows": rows})
    return {
        "avatar": avatar["name"],
        "game": adapter["game"],
        "verified": adapter.get("verified", False),
        "editor": adapter.get("editor"),
        "notes": adapter.get("notes", []),
        "sections": sections,
    }


def _row(control, setting, reason=""):
    return {"label": control["label"], "setting": setting, "reason": reason}


def _source(avatar, control, key="from"):
    """Resolve the first available path among control[key] (str or list)."""
    paths = control.get(key, [])
    for path in [paths] if isinstance(paths, str) else paths:
        value = model.get(avatar, path)
        if value is not None:
            return path, value
    return None, None


def _transform(value, name):
    if name is None:
        return value
    if name == "darkness":  # colour -> 0 (very light) .. 1 (very dark)
        return 1 - color.lightness(value)
    raise ValueError(f"trasformazione sconosciuta: {name}")


def _slider(avatar, control):
    path, value = _source(avatar, control)
    if value is None:
        return _row(control, DEFAULT, "tratto non specificato")
    if control.get("transform"):
        reason = _describe(avatar, path)
        value = _transform(value, control["transform"])
    else:
        reason = f"{model.label(path)}: {qualitative(value, path)}"
    if control.get("invert"):
        value = 1 - value
    if "min" in control and "max" in control:
        lo, hi = control["min"], control["max"]
        step = control.get("step", 1)
        pos = round((lo + value * (hi - lo)) / step) * step
        return _row(control, f"{pos:g} (scala {lo:g}–{hi:g})", reason)
    pct = round(value * 100)
    side = "centro" if 40 <= pct <= 60 else ("verso sinistra" if pct < 40 else "verso destra")
    return _row(control, f"≈{pct}% della corsa ({side})", reason)


def _choice(avatar, control):
    options = control.get("options", [])
    if options:
        best = min(options, key=lambda o: _option_score(avatar, o.get("match", {})))
        matched = [p for p in best.get("match", {}) if model.get(avatar, p) is not None]
        if matched:
            return _row(control, best["value"], "; ".join(_describe(avatar, p) for p in matched))
    hints = [_describe(avatar, p) for p in control.get("hint", []) if model.get(avatar, p) is not None]
    count = control.get("count")
    setting = f"scegli tra le {count} opzioni" if count else "scegli l'opzione più vicina"
    if not hints:
        return _row(control, DEFAULT if not count else setting, "tratto non specificato")
    return _row(control, setting, "cerca: " + "; ".join(hints))


def _option_score(avatar, match):
    score = 0.0
    for path, target in match.items():
        actual = model.get(avatar, path)
        if actual is None:
            continue
        if isinstance(actual, list):
            # Preference lists (lineage) and tag lists (hair styles): earlier is better.
            score += actual.index(target) / (2 * len(actual)) if target in actual else 1
        elif isinstance(target, (int, float)) and isinstance(actual, (int, float)):
            score += (actual - target) ** 2
        else:
            score += 0 if actual == target else 1
    return score


def _color(avatar, control):
    path, value = _source(avatar, control)
    if value is None:
        return _row(control, DEFAULT, "colore non specificato")
    reason = f"{model.label(path)}: {value} ({color.describe(value)})"
    palette = control.get("palette")
    if palette:
        swatch = color.nearest(value, palette)
        return _row(control, swatch["value"], f"{reason}; ΔE {color.delta_e(value, swatch['hex']):.0f}")
    return _row(control, f"{value} — scegli la tinta più vicina", reason)


def _toggle(avatar, control):
    path, value = _source(avatar, control)
    if value is None:
        return _row(control, DEFAULT, "tratto non specificato")
    on = value if isinstance(value, bool) else value >= control.get("threshold", 0.5)
    reason = model.label(path) + ("" if isinstance(value, bool) else f": {qualitative(value, path)}")
    return _row(control, "sì" if on else "no", reason)


def _weights(avatar, control):
    _, build = _source(avatar, control)
    if not build:
        return _row(control, DEFAULT, "corporatura non specificata")
    total = sum(build.values())
    parts = [f"{control['labels'][k]} {round(100 * build.get(k, 0) / total)}%" for k in control["labels"]]
    return _row(control, ", ".join(parts), "corporatura canonica normalizzata")


def _list(avatar, control):
    types = set(control.get("types", []))
    items = [i for i in avatar.get(control["from"], []) if not types or i.get("type") in types]
    if not items:
        return _row(control, "nessuno")
    return _row(control, "; ".join(f"{i.get('area', '')} {i.get('description', '')}".strip() for i in items),
                "dall'elenco " + model.label(control["from"]))


def _note(avatar, control):
    return _row(control, control["text"])


_CONTROLS = {
    "slider": _slider, "choice": _choice, "color": _color, "toggle": _toggle,
    "weights": _weights, "list": _list, "note": _note,
}


def qualitative(value, path=None):
    words = model.SCALES.get(path, model.AVERAGE_SCALE)
    if value < 0.15:
        return words[0]
    if value < 0.4:
        return words[1]
    if value <= 0.6:
        return words[2]
    if value <= 0.85:
        return words[3]
    return words[4]


def _describe(avatar, path):
    value = model.get(avatar, path)
    name = model.label(path)
    if isinstance(value, bool):
        return f"{name}: {'sì' if value else 'no'}"
    if path == "identity.apparent_age":
        return f"{name}: circa {value:g} anni"
    if isinstance(value, (int, float)):
        return f"{name}: {qualitative(value, path)}"
    if isinstance(value, list):
        return f"{name}: {', '.join(model.enum_label(path, v) for v in value)}"
    if path in model.COLORS:
        return f"{name}: {color.describe(value)}"
    return f"{name}: {model.enum_label(path, value)}"
