#!/usr/bin/env python3
"""Bereitet Bilder und Videos für die Website auf (schnelle Ladezeiten, Smartphone, SEO).

Aufruf:  python3 tools/medien.py        (danach: python3 tools/build.py)

Quelle (Originale in voller Auflösung):
  fotos/quelle/echt/<name>.jpg|png|webp   echte Fotos aus dem Laden
  fotos/quelle/ki/<name>.jpg|png|webp     KI-generierte Symbolbilder
  fotos/quelle/ki/<name>.mp4|mov|webm     KI-generierte Videos (ebenso in echt/ möglich)

<name> = Slug der Leistungsseite (z. B. schluessel, gravur), "hero" (Startseite) oder "shop".
Liegt ein Name in beiden Ordnern, gewinnt ki/.

Ergebnis (wird ins Repository übernommen, der Website-Build braucht dann nur Python ohne Zusatzpakete):
  assets/img/<name>-<breite>.webp   mehrere Größen für srcset
  assets/img/<name>.jpg             Rückfall für alte Browser, Vorschaubild für Videos
  assets/video/<name>.mp4           H.264, ohne Ton, max. 1280 px breit
  assets/img/medien.json            Maße, Größen, Herkunft (ki: true/false)

Benötigt lokal: Pillow (pip install pillow) und für Videos ffmpeg.
"""
import json
import pathlib
import shutil
import subprocess
import sys

from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUELLE = ROOT / "fotos" / "quelle"
IMG = ROOT / "assets" / "img"
VIDEO = ROOT / "assets" / "video"
BREITEN = (480, 800, 1200, 1600, 2400)
BILD_ENDUNGEN = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_ENDUNGEN = {".mp4", ".mov", ".webm"}


def bild(name, pfad, ki):
    im = ImageOps.exif_transpose(Image.open(pfad)).convert("RGB")  # Metadaten (EXIF, GPS) fallen weg
    w, h = im.size
    breiten = [b for b in BREITEN if b < w] + [min(w, BREITEN[-1])]
    for b in breiten:
        im.resize((b, round(h * b / w)), Image.LANCZOS).save(IMG / f"{name}-{b}.webp", "WEBP", quality=80, method=6)
    fb = min(w, 1200)
    im.resize((fb, round(h * fb / w)), Image.LANCZOS).save(
        IMG / f"{name}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
    return {"w": w, "h": h, "breiten": breiten, "ki": ki}


def video(name, pfad):
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg fehlt – wird für Videos benötigt.")
    VIDEO.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(pfad), "-an",
         "-vf", "scale='min(1280,iw)':-2,fps=30", "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-crf", "27", "-preset", "slow", "-movflags", "+faststart", str(VIDEO / f"{name}.mp4")], check=True)
    standbild = IMG / f".{name}-standbild.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(pfad), "-frames:v", "1", str(standbild)], check=True)
    return standbild


def main():
    # Alte Ergebnisse entfernen, damit gelöschte Quellen nicht online bleiben
    if IMG.exists():
        shutil.rmtree(IMG)
    if VIDEO.exists():
        shutil.rmtree(VIDEO)
    IMG.mkdir(parents=True)
    manifest = {}
    for ordner, ki in (("echt", False), ("ki", True)):  # ki/ zuletzt: überschreibt echt/
        dateien = sorted((QUELLE / ordner).glob("*")) if (QUELLE / ordner).exists() else []
        for pfad in (p for p in dateien if p.suffix.lower() in BILD_ENDUNGEN):
            manifest[pfad.stem] = bild(pfad.stem, pfad, ki)
        for pfad in (p for p in dateien if p.suffix.lower() in VIDEO_ENDUNGEN):
            standbild = video(pfad.stem, pfad)
            hat_bild = any((QUELLE / ordner / (pfad.stem + x)).exists() for x in BILD_ENDUNGEN)
            if not hat_bild:  # kein eigenes Vorschaubild → erstes Videobild
                manifest[pfad.stem] = bild(pfad.stem, standbild, ki)
            standbild.unlink()
            manifest[pfad.stem]["video"] = True
            manifest[pfad.stem]["ki"] = ki
    (IMG / "medien.json").write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    for name, m in sorted(manifest.items()):
        kb = sum(f.stat().st_size for f in IMG.glob(f"{name}*")) // 1024
        vid = f', Video {(VIDEO / (name + ".mp4")).stat().st_size // 1024} KB' if m.get("video") else ""
        print(f'{name}: {m["w"]}×{m["h"]}, {"KI-Symbolbild" if m["ki"] else "echtes Foto"}, Bilder {kb} KB{vid}')
    if not manifest:
        print("Keine Quellen in fotos/quelle/ gefunden.")


if __name__ == "__main__":
    main()
