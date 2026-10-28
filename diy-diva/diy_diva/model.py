"""Canonical avatar model: field catalogue, Italian labels and validation.

The canonical avatar describes a character independently from any game.
Continuous traits are normalised to 0..1 where 0.5 is "average"; colours are
sRGB hex strings; discrete traits use the enums below.
"""

import re

SCHEMA_VERSION = "0.1"

# Continuous traits (0..1, 0.5 = average). Path -> Italian label.
CONTINUOUS = {
    "identity.presentation": "presentazione (0 maschile, 1 femminile)",
    "body.height": "altezza",
    "body.weight": "peso",
    "face.face_length": "lunghezza del viso",
    "face.forehead_height": "altezza della fronte",
    "face.brow_height": "altezza delle sopracciglia",
    "face.brow_thickness": "spessore delle sopracciglia",
    "face.lash_length": "lunghezza delle ciglia",
    "face.eye_size": "grandezza degli occhi",
    "face.eye_spacing": "distanza tra gli occhi",
    "face.eye_tilt": "inclinazione degli occhi (0 all'ingiù, 1 all'insù)",
    "face.nose_width": "larghezza del naso",
    "face.nose_length": "lunghezza del naso",
    "face.nose_bridge": "altezza del dorso del naso",
    "face.cheekbone_prominence": "zigomi pronunciati",
    "face.cheek_fullness": "guance piene",
    "face.lip_fullness": "labbra carnose",
    "face.mouth_width": "larghezza della bocca",
    "face.jaw_width": "larghezza della mascella",
    "face.chin_prominence": "mento pronunciato",
    "face.ear_size": "grandezza delle orecchie",
    "skin.freckles": "lentiggini",
    "skin.vitiligo": "vitiligine",
    "skin.dark_circles": "occhiaie",
    "makeup.eyeliner": "eyeliner",
    "makeup.blush": "fard",
    "voice.pitch": "tono della voce (0 grave, 1 acuto)",
}

COLORS = {
    "skin.color": "colore della pelle",
    "eyes.color": "colore degli occhi",
    "eyes.secondary_color": "colore del secondo occhio (eterocromia)",
    "brows.color": "colore delle sopracciglia",
    "hair.color": "colore dei capelli",
    "hair.highlight_color": "colore delle meches",
    "facial_hair.color": "colore di barba e baffi",
    "makeup.lip_color": "colore del rossetto",
}

ENUMS = {
    "face.shape": ["oval", "round", "square", "heart", "long", "diamond"],
    "skin.undertone": ["warm", "neutral", "cool"],
    "hair.length": ["shaved", "very_short", "short", "medium", "long", "very_long"],
    "hair.texture": ["straight", "wavy", "curly", "coily"],
    "facial_hair.style": ["none", "stubble", "mustache", "goatee", "short_beard", "full_beard"],
}

BOOLEANS = {
    "skin.beauty_marks": "nei",
    "hair.bangs": "frangia",
}

ENUM_LABELS = {
    "face.shape": {"oval": "ovale", "round": "tondo", "square": "squadrato", "heart": "a cuore",
                   "long": "allungato", "diamond": "a diamante"},
    "skin.undertone": {"warm": "caldo", "neutral": "neutro", "cool": "freddo"},
    "hair.length": {"shaved": "rasati", "very_short": "cortissimi", "short": "corti",
                    "medium": "media lunghezza", "long": "lunghi", "very_long": "lunghissimi"},
    "hair.texture": {"straight": "lisci", "wavy": "mossi", "curly": "ricci", "coily": "afro"},
    "facial_hair.style": {"none": "nessuna", "stubble": "barba incolta", "mustache": "baffi",
                          "goatee": "pizzetto", "short_beard": "barba corta", "full_beard": "barba lunga"},
    "hair.style_tags": {"ponytail": "coda di cavallo", "bun": "chignon", "braid": "treccia",
                        "undercut": "undercut", "side_part": "riga laterale", "mohawk": "moicana",
                        "dreadlocks": "dreadlock", "buzz_cut": "rasatura"},
    "identity.lineage_preference": {"human": "umano", "elf": "elfo", "dwarf": "nano", "qunari": "qunari"},
}

# Words for the five bands of a 0..1 trait (see engine.qualitative).
AVERAGE_SCALE = ("molto sotto la media", "sotto la media", "nella media", "sopra la media", "molto sopra la media")
AMOUNT_SCALE = ("assenti o quasi", "leggere", "moderate", "marcate", "intense")
SCALES = {
    "identity.presentation": ("nettamente maschile", "maschile", "androgina", "femminile", "nettamente femminile"),
    "voice.pitch": ("molto grave", "grave", "media", "acuta", "molto acuta"),
    "face.eye_tilt": ("molto all'ingiù", "all'ingiù", "dritti", "all'insù", "molto all'insù"),
    **{path: AMOUNT_SCALE for path in ("skin.freckles", "skin.vitiligo", "skin.dark_circles",
                                        "makeup.eyeliner", "makeup.blush")},
}


def enum_label(path, value):
    return ENUM_LABELS.get(path, {}).get(value, str(value).replace("_", " "))


LABELS = {
    "oval": "ovale", "round": "tondo", "square": "squadrato", "heart": "a cuore",
    "long": "allungato", "diamond": "a diamante",
    "warm": "caldo", "neutral": "neutro", "cool": "freddo",
    "shaved": "rasati", "very_short": "cortissimi", "short": "corti",
    "medium": "media lunghezza", "very_long": "lunghissimi",
    "straight": "lisci", "wavy": "mossi", "curly": "ricci", "coily": "afro",
    "none": "nessuna", "stubble": "barba incolta", "mustache": "baffi",
    "goatee": "pizzetto", "short_beard": "barba corta", "full_beard": "barba lunga",
}

LABELS = {
    **CONTINUOUS, **COLORS, **BOOLEANS,
    "face.shape": "forma del viso",
    "skin.undertone": "sottotono della pelle",
    "hair.length": "lunghezza dei capelli",
    "hair.texture": "tipo di capelli",
    "hair.style_tags": "acconciatura",
    "facial_hair.style": "barba",
    "identity.lineage_preference": "stirpe preferita",
    "identity.apparent_age": "età apparente",
    "body.build": "corporatura",
    "marks": "segni distintivi",
    "accessories": "accessori",
}

BUILD_KEYS = ("lean", "muscular", "heavy")
MARK_TYPES = ("scar", "tattoo", "paint", "cyberware", "piercing", "other")

_HEX = re.compile(r"^#[0-9a-fA-F]{6}$")


def get(avatar, path, default=None):
    """Read a dotted path from the avatar; returns default when missing."""
    node = avatar
    for key in path.split("."):
        if not isinstance(node, dict) or key not in node:
            return default
        node = node[key]
    return node


def label(path):
    return LABELS.get(path, path)


def validate(avatar):
    """Return a list of human-readable problems (empty if the avatar is valid)."""
    errors = []
    if not isinstance(avatar, dict):
        return ["l'avatar deve essere un oggetto JSON"]
    if avatar.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version deve essere \"{SCHEMA_VERSION}\"")
    if not avatar.get("name"):
        errors.append("manca il campo name")

    for path in CONTINUOUS:
        value = get(avatar, path)
        if value is not None and not (_is_number(value) and 0 <= value <= 1):
            errors.append(f"{path} deve essere un numero tra 0 e 1")
    for path in COLORS:
        value = get(avatar, path)
        if value is not None and not (isinstance(value, str) and _HEX.match(value)):
            errors.append(f"{path} deve essere un colore esadecimale come #a0522d")
    for path, allowed in ENUMS.items():
        value = get(avatar, path)
        if value is not None and value not in allowed:
            errors.append(f"{path} deve essere uno tra: {', '.join(allowed)}")
    for path in BOOLEANS:
        value = get(avatar, path)
        if value is not None and not isinstance(value, bool):
            errors.append(f"{path} deve essere true o false")

    build = get(avatar, "body.build")
    if build is not None:
        if not isinstance(build, dict) or set(build) - set(BUILD_KEYS):
            errors.append(f"body.build accetta solo le chiavi {', '.join(BUILD_KEYS)}")
        elif not all(_is_number(v) and v >= 0 for v in build.values()) or sum(build.values()) == 0:
            errors.append("body.build deve contenere pesi non negativi, non tutti zero")

    for i, mark in enumerate(avatar.get("marks", [])):
        if not isinstance(mark, dict) or mark.get("type") not in MARK_TYPES:
            errors.append(f"marks[{i}].type deve essere uno tra: {', '.join(MARK_TYPES)}")
    return errors


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)
