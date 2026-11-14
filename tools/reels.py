#!/usr/bin/env python3
"""Macht aus KI-Rohvideos fertige Instagram-Reels (1080x1920) mit Texteinblendung.

Aufruf:  python3 tools/reels.py <ordner-mit-rohvideos> [<schrift-ordner>]

Rohvideos heißen wie der Slug der Leistung (z. B. schuhreparatur.mp4).
Ergebnis: social/instagram/<slug>.mp4 und <slug>-cover.jpg.
Texte kommen aus data/firma.json und der Tabelle REELS unten, es wird nichts erfunden.
Braucht Pillow und ffmpeg. Schrift: Cormorant als TTF (aus assets/fonts/*.woff2 umgewandelt).
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FIRMA = json.loads((ROOT / "data" / "firma.json").read_text(encoding="utf-8"))
ZIEL = ROOT / "social" / "instagram"
B, H = 1080, 1920

PAPIER = (255, 253, 248)
TINTE = (28, 26, 22)
WEICH = (74, 70, 62)
MESSING = (133, 96, 31)
ROT = (161, 42, 30)

# titel/zeile: Einblendung während des Films. schluss: Zeilen der Schlusskarte.
REELS = {
    "schuhreparatur": {
        "titel": "Schuhreparatur",
        "zeile": "Absätze · Sohlen · Nähte · Pflege",
        "schluss_kopf": "Lieblingsschuhe. Wie neu.",
        "schluss": ["im Globus Gensingen", FIRMA["oeffnungszeiten"]["kurz"]],
        "schluss_oben": 240,  # Schlusskarte oben, damit die fertigen Schuhe sichtbar bleiben
    },
    "schluessel": {
        "titel": "Schlüssel nachmachen",
        "zeile": "Original mitbringen. Kopie mitnehmen.",
        "schluss_kopf": "Ihr Schlüsseldienst",
        "schluss": ["im Globus Gensingen", FIRMA["oeffnungszeiten"]["kurz"]],
    },
    "tueroeffnung": {
        "titel": "Ausgesperrt?",
        "zeile": "Wir sind da. Rund um die Uhr.",
        "schluss_kopf": "Türöffnung 24/7",
        "schluss": ["Notdienst " + FIRMA["notdienst"], "Gensingen · Bad Kreuznach · Bingen"],
        "akzent": ROT,
    },
}


def schrift(ordner, name, groesse):
    return ImageFont.truetype(str(ordner / f"{name}.ttf"), groesse)


def gesperrt(d, mitte, y, text, font, farbe, abstand):
    """Versalien mit Laufweite, mittig gesetzt."""
    breite = sum(d.textlength(c, font=font) for c in text) + abstand * (len(text) - 1)
    x = mitte - breite / 2
    for c in text:
        d.text((x, y), c, font=font, fill=farbe)
        x += d.textlength(c, font=font) + abstand


def mittig(d, y, text, font, farbe):
    d.text((B / 2, y), text, font=font, fill=farbe, anchor="ma")


def passend(d, ordner, name, text, groesse, max_breite):
    f = schrift(ordner, name, groesse)
    while d.textlength(text, font=f) > max_breite:
        groesse -= 4
        f = schrift(ordner, name, groesse)
    return f


def tafel(d, oben, unten, akzent):
    d.rounded_rectangle((70, oben, B - 70, unten), radius=6, fill=PAPIER + (238,))
    d.rectangle((70, oben, B - 70, oben + 5), fill=akzent + (255,))


def titelbild(r, fonts):
    """Tafel im oberen sicheren Bereich (unter der Instagram-Kopfzeile)."""
    bild = Image.new("RGBA", (B, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(bild)
    akzent = r.get("akzent", MESSING)
    tafel(d, 250, 560, akzent)
    gesperrt(d, B / 2, 288, FIRMA["name_kurz"].upper(), schrift(fonts, "cormorant-600", 34), akzent, 7)
    mittig(d, 340, r["titel"], passend(d, fonts, "cormorant-600", r["titel"], 116, B - 220), TINTE)
    mittig(d, 482, r["zeile"], passend(d, fonts, "cormorant-500i", r["zeile"], 46, B - 220), WEICH)
    return bild


def schlusskompakt(r, fonts, t):
    """Niedrige Schlusskarte ab Höhe t, wenn das Motiv in der Bildmitte frei bleiben soll."""
    bild = Image.new("RGBA", (B, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(bild)
    akzent = r.get("akzent", MESSING)
    tafel(d, t, t + 500, akzent)
    gesperrt(d, B / 2, t + 36, r["schluss_kopf"].upper(), schrift(fonts, "cormorant-600", 34), akzent, 6)
    name = FIRMA["name_kurz"]
    mittig(d, t + 82, name, passend(d, fonts, "cormorant-600", name, 104, B - 220), TINTE)
    mittig(d, t + 222, r["schluss"][0], passend(d, fonts, "cormorant-600", r["schluss"][0], 66, B - 220), TINTE)
    rest = " · ".join(r["schluss"][1:] + ["yakut-service.de"])
    mittig(d, t + 316, rest, passend(d, fonts, "cormorant-500", rest, 46, B - 220), WEICH)
    mittig(d, t + 418, "Symbolvideo, mit KI erstellt", schrift(fonts, "cormorant-500", 30), (117, 111, 99))
    return bild


def schlussbild(r, fonts):
    """Schlusskarte, bleibt über der Instagram-Fußzeile."""
    bild = Image.new("RGBA", (B, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(bild)
    akzent = r.get("akzent", MESSING)
    if "schluss_oben" in r:
        return schlusskompakt(r, fonts, r["schluss_oben"])
    tafel(d, 760, 1490, akzent)
    gesperrt(d, B / 2, 810, r["schluss_kopf"].upper(), schrift(fonts, "cormorant-600", 36), akzent, 6)
    name = FIRMA["name_kurz"]
    mittig(d, 880, name, passend(d, fonts, "cormorant-600", name, 112, B - 220), TINTE)
    d.rectangle((B / 2 - 60, 1040, B / 2 + 60, 1043), fill=akzent + (255,))
    y = 1085
    for i, zeile in enumerate(r["schluss"]):
        gross = i == 0
        f = passend(d, fonts, "cormorant-600" if gross else "cormorant-500", zeile, 70 if gross else 52, B - 220)
        mittig(d, y, zeile, f, TINTE if gross else WEICH)
        y += 96 if gross else 70
    mittig(d, 1318, "yakut-service.de", schrift(fonts, "cormorant-500i", 44), akzent)
    # Kennzeichnung wie auf der Website: KI-Bilder sind Symbolbilder.
    mittig(d, 1425, "Symbolvideo, mit KI erstellt", schrift(fonts, "cormorant-500", 30), (117, 111, 99))
    return bild


def dauer(datei):
    aus = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(datei)], capture_output=True, text=True, check=True)
    return float(aus.stdout.strip())


def bauen(roh, slug, fonts, tmp):
    r = REELS[slug]
    t = dauer(roh)
    titel, schluss = tmp / f"{slug}-titel.png", tmp / f"{slug}-schluss.png"
    titelbild(r, fonts).save(titel)
    schlussbild(r, fonts).save(schluss)
    s0 = t - 3.0  # Schlusskarte in den letzten 3 Sekunden
    filt = (
        f"[0:v]scale={B}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={B}:{H},"
        f"unsharp=5:5:0.5,setsar=1[v];"
        f"[1:v]format=rgba,fade=in:st=0.5:d=0.6:alpha=1,fade=out:st={s0 - 0.8:.2f}:d=0.5:alpha=1[a];"
        f"[2:v]format=rgba,fade=in:st={s0:.2f}:d=0.6:alpha=1[b];"
        f"[v][a]overlay=0:0[v1];[v1][b]overlay=0:0,format=yuv420p[out]"
    )
    ziel = ZIEL / f"{slug}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(roh),
        "-loop", "1", "-t", f"{t}", "-i", str(titel),
        "-loop", "1", "-t", f"{t}", "-i", str(schluss),
        "-filter_complex", filt, "-map", "[out]", "-map", "0:a?",
        "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-r", "30",
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{t}", str(ziel),
    ], check=True)
    # Titelbild für das Profilraster: Bild aus der Schlusskarte.
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t - 0.6:.2f}", "-i", str(ziel),
                    "-frames:v", "1", "-q:v", "3", str(ZIEL / f"{slug}-cover.jpg")], check=True)
    print(f"  {ziel.relative_to(ROOT)}  ({t:.1f} s)")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    quelle = Path(sys.argv[1])
    fonts = Path(sys.argv[2]) if len(sys.argv) > 2 else quelle / "fonts"
    tmp = quelle / "tmp"
    tmp.mkdir(exist_ok=True)
    ZIEL.mkdir(parents=True, exist_ok=True)
    for slug in REELS:
        roh = quelle / f"{slug}.mp4"
        if roh.exists():
            bauen(roh, slug, fonts, tmp)
        else:
            print(f"  fehlt: {roh}")


if __name__ == "__main__":
    main()
