"""Colour helpers: sRGB hex -> CIELAB, perceptual distance and plain-Italian names."""

import math


def hex_to_lab(hex_color):
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    r, g, b = (_linearize(c) for c in (r, g, b))
    # sRGB -> XYZ (D65), normalised by the D65 white point.
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    fx, fy, fz = (_f(t) for t in (x, y, z))
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e(hex_a, hex_b):
    """CIE76 distance: good enough to pick the nearest swatch in a palette."""
    return math.dist(hex_to_lab(hex_a), hex_to_lab(hex_b))


def nearest(hex_color, palette):
    """Return the palette entry ({"value", "hex"}) closest to hex_color."""
    return min(palette, key=lambda entry: delta_e(hex_color, entry["hex"]))


def lightness(hex_color):
    """CIELAB L* rescaled to 0..1."""
    return hex_to_lab(hex_color)[0] / 100


def describe(hex_color):
    l, a, b = hex_to_lab(hex_color)
    if l < 20:
        tone = "molto scuro"
    elif l < 40:
        tone = "scuro"
    elif l < 60:
        tone = "medio"
    elif l < 80:
        tone = "chiaro"
    else:
        tone = "molto chiaro"
    chroma = math.hypot(a, b)
    if chroma < 8:
        return f"{tone}, quasi neutro"
    hue = math.degrees(math.atan2(b, a)) % 360
    for limit, name in ((20, "rosato"), (45, "rossastro"), (70, "aranciato/ramato"),
                        (100, "dorato/giallo"), (160, "verde"), (250, "azzurro/blu"),
                        (320, "viola"), (360, "rosato")):
        if hue < limit:
            return f"{tone}, {name}"
    return tone


def _linearize(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _f(t):
    return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
