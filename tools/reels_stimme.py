#!/usr/bin/env python3
"""Instagram-Reels mit Sprecherstimme und animierten Texten (1080x1920).

Aufruf:  python3 tools/reels_stimme.py <ordner> [slug ...]

Im Ordner liegen je Reel <slug>.mp4 (Rohvideo), <slug>.wav (Sprecher) und
<slug>.json (Wortzeiten der Stimme: [[wort, start, ende], ...], z. B. aus faster-whisper).
Dazu fonts/cormorant-500.ttf, -500i.ttf, -600.ttf und fonts/fett.ttf (fette Grotesk für die Schlagzeilen).
Ergebnis: social/instagram/<slug>.mp4. Texte stehen unten in REELS, Firmendaten in data/firma.json.
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
PAPIER, TINTE, WEICH = (255, 253, 248), (28, 26, 22), (74, 70, 62)
MESSING, GOLD, ROT = (133, 96, 31), (232, 195, 122), (161, 42, 30)
GRAU = (117, 111, 99)
START = 0.35  # Sekunden bis die Stimme einsetzt
ZEITEN = FIRMA["oeffnungszeiten"]["kurz"]

# zeilen: [Schlagzeile (2 Zeilen, zweite in Gold), gesprochener Text dazu].
# Der letzte Satz der Stimme gehört zur Schlusskarte.
REELS = {
    "schuhreparatur": {
        "zeilen": [
            (["LIEBLINGSSCHUHE", "KAPUTT?"], "Lieblingsschuhe kaputt?"),
            (["KEIN", "PROBLEM!"], "Kein Problem!"),
            (["ABSÄTZE · SOHLEN", "NÄHTE · PFLEGE"], "Absätze, Sohlen, Nähte und Pflege"),
            (["WIR MACHEN SIE", "WIEDER FIT"], "wir machen sie wieder fit."),
        ],
        "schluss_text": "Service-Punkt Yakut, im Globus Gensingen!",
        "kopf": "Lieblingsschuhe. Wie neu.",
        "karte": ["im Globus Gensingen", ZEITEN],
        "karte_oben": True,
    },
    "schluessel": {
        "zeilen": [
            (["SCHLÜSSEL", "NACHMACHEN?"], "Schlüssel nachmachen?"),
            (["GANZ", "EINFACH!"], "Ganz einfach!"),
            (["ORIGINAL MITBRINGEN", "KOPIE MITNEHMEN"], "Original mitbringen, Kopie mitnehmen."),
            (["HAUS · WOHNUNG", "BRIEFKASTEN"], "Für Haus, Wohnung und Briefkasten."),
        ],
        "schluss_text": "Service-Punkt Yakut, im Globus Gensingen!",
        "kopf": "Ihr Schlüsseldienst",
        "karte": ["im Globus Gensingen", ZEITEN],
        "karte_oben": True,
    },
    "tueroeffnung": {
        "zeilen": [
            (["AUS-", "GESPERRT?"], "Ausgesperrt?"),
            (["KEINE", "PANIK!"], "Keine Panik!"),
            (["NOTDIENST", "RUND UM DIE UHR"], "Unser Notdienst ist rund um die Uhr für Sie da."),
        ],
        "schluss_text": "Service-Punkt Yakut – jetzt anrufen!",
        "kopf": "Türöffnung 24/7",
        "karte": ["Notdienst " + FIRMA["notdienst"], "Gensingen · Bad Kreuznach · Bingen"],
        "akzent": ROT,
        "karte_oben": True,
    },
    "gravur": {
        "zeilen": [
            (["DAS PERFEKTE", "WEIHNACHTSGESCHENK?"], "Das perfekte Weihnachtsgeschenk?"),
            (["PERSÖNLICH", "GRAVIERT!"], "Persönlich graviert!"),
            (["EDELSTAHL · GLAS", "KUNSTSTOFF · HOLZ"], "Auf Edelstahl, Glas, Kunststoff und Holz."),
        ],
        "schluss_text": "Jetzt bei Service-Punkt Yakut, im Globus Gensingen!",
        "kopf": "Gravur zu Weihnachten",
        "karte": ["im Globus Gensingen", ZEITEN],
        "karte_oben": True,
    },
}


def schrift(fonts, name, groesse):
    return ImageFont.truetype(str(fonts / f"{name}.ttf"), groesse)


def passend(d, fonts, name, text, groesse, max_breite):
    f = schrift(fonts, name, groesse)
    while d.textlength(text, font=f) > max_breite:
        groesse -= 4
        f = schrift(fonts, name, groesse)
    return f


def gesperrt(d, mitte, y, text, font, farbe, abstand):
    breite = sum(d.textlength(c, font=font) for c in text) + abstand * (len(text) - 1)
    x = mitte - breite / 2
    for c in text:
        d.text((x, y), c, font=font, fill=farbe)
        x += d.textlength(c, font=font) + abstand


def schlagzeile(zeilen, fonts):
    """Fette Schlagzeile, zweite Zeile in Gold, mit weichem Schatten. 1080 x 420."""
    bild = Image.new("RGBA", (B, 420), (0, 0, 0, 0))
    d = ImageDraw.Draw(bild)
    y = 40
    for i, z in enumerate(zeilen):
        f = passend(d, fonts, "fett", z, 118, B - 120)
        farbe = GOLD if i == 1 else PAPIER
        d.text((B / 2 + 5, y + 7), z, font=f, fill=(0, 0, 0, 150), anchor="ma",
               stroke_width=10, stroke_fill=(0, 0, 0, 110))
        d.text((B / 2, y), z, font=f, fill=farbe + (255,), anchor="ma",
               stroke_width=7, stroke_fill=TINTE + (255,))
        y += f.size + 34
    return bild


def marke(fonts, akzent):
    """Kleine Markentafel oben. 1080 x 110."""
    bild = Image.new("RGBA", (B, 110), (0, 0, 0, 0))
    d = ImageDraw.Draw(bild)
    f = schrift(fonts, "cormorant-600", 38)
    text = FIRMA["name_kurz"].upper()
    breite = sum(d.textlength(c, font=f) for c in text) + 7 * (len(text) - 1)
    d.rounded_rectangle((B / 2 - breite / 2 - 44, 12, B / 2 + breite / 2 + 44, 98), radius=6, fill=PAPIER + (240,))
    d.rectangle((B / 2 - breite / 2 - 44, 12, B / 2 + breite / 2 + 44, 17), fill=akzent + (255,))
    gesperrt(d, B / 2, 30, text, f, TINTE, 7)
    return bild


def karte(r, fonts):
    """Schlusskarte. Hoch (730) oder flach (500), wenn das Motiv in der Mitte frei bleiben soll."""
    akzent = r.get("akzent", MESSING)
    flach = r.get("karte_oben", False)
    hoch = 500 if flach else 730
    bild = Image.new("RGBA", (B, hoch), (0, 0, 0, 0))
    d = ImageDraw.Draw(bild)
    d.rounded_rectangle((70, 0, B - 70, hoch), radius=6, fill=PAPIER + (242,))
    d.rectangle((70, 0, B - 70, 5), fill=akzent + (255,))
    name = FIRMA["name_kurz"]

    def mittig(y, text, font, farbe):
        d.text((B / 2, y), text, font=font, fill=farbe, anchor="ma")

    if flach:
        gesperrt(d, B / 2, 36, r["kopf"].upper(), schrift(fonts, "cormorant-600", 34), akzent, 6)
        mittig(82, name, passend(d, fonts, "cormorant-600", name, 104, B - 220), TINTE)
        mittig(222, r["karte"][0], passend(d, fonts, "cormorant-600", r["karte"][0], 66, B - 220), TINTE)
        rest = " · ".join(r["karte"][1:] + ["yakut-service.de"])
        mittig(316, rest, passend(d, fonts, "cormorant-500", rest, 46, B - 220), WEICH)
        mittig(418, "Symbolvideo, mit KI erstellt", schrift(fonts, "cormorant-500", 30), GRAU)
    else:
        gesperrt(d, B / 2, 50, r["kopf"].upper(), schrift(fonts, "cormorant-600", 36), akzent, 6)
        mittig(120, name, passend(d, fonts, "cormorant-600", name, 112, B - 220), TINTE)
        d.rectangle((B / 2 - 60, 280, B / 2 + 60, 283), fill=akzent + (255,))
        mittig(325, r["karte"][0], passend(d, fonts, "cormorant-600", r["karte"][0], 70, B - 220), TINTE)
        mittig(421, r["karte"][1], passend(d, fonts, "cormorant-500", r["karte"][1], 52, B - 220), WEICH)
        mittig(558, "yakut-service.de", schrift(fonts, "cormorant-500i", 44), akzent)
        mittig(665, "Symbolvideo, mit KI erstellt", schrift(fonts, "cormorant-500", 30), GRAU)
    return bild, (240 if flach else 760)


def dauer(datei):
    aus = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(datei)], capture_output=True, text=True, check=True)
    return float(aus.stdout.strip())


def satzzeiten(r, woerter, vo_dauer):
    """Startzeit jedes Satzes: Wortzahl im Text anteilig auf die erkannten Wörter umgelegt."""
    saetze = [s for _, s in r["zeilen"]] + [r["schluss_text"]]
    zahl = [len(s.replace("–", " ").split()) for s in saetze]
    gesamt = sum(zahl)
    starts, k = [], 0
    for n in zahl:
        if woerter:
            i = min(len(woerter) - 1, round(k * len(woerter) / gesamt))
            starts.append(0.0 if k == 0 else float(woerter[i][1]))
        else:
            starts.append(vo_dauer * k / gesamt)
        k += n
    return starts


def bauen(quelle, slug, fonts, tmp):
    r = REELS[slug]
    roh, vo = quelle / f"{slug}.mp4", quelle / f"{slug}.wav"
    zeiten = quelle / f"{slug}.json"
    woerter = json.loads(zeiten.read_text(encoding="utf-8")) if zeiten.exists() else []
    t_vid, t_vo = dauer(roh), dauer(vo)
    starts = [START + s for s in satzzeiten(r, woerter, t_vo)]
    t_karte = starts[-1] - 0.15
    t = max(t_vid, START + t_vo + 1.3, t_karte + 3.0)
    akzent = r.get("akzent", MESSING)

    eingaben, filt = [], []
    filt.append(
        f"[0:v]scale={B}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={B}:{H},"
        f"unsharp=5:5:0.5,fps=30,tpad=stop_mode=clone:stop_duration={max(0.0, t - t_vid) + 0.5:.2f},setsar=1[v0]")

    def ebene(bild, name):
        pfad = tmp / f"{slug}-{name}.png"
        bild.save(pfad)
        eingaben.extend(["-loop", "1", "-framerate", "30", "-t", f"{t:.2f}", "-i", str(pfad)])
        return len(eingaben) // 7 + 1  # Eingang 0 = Video, 1 = Stimme

    letzter = "v0"
    # Markentafel fährt von oben ein und verschwindet, wenn die flache Schlusskarte oben erscheint.
    n = ebene(marke(fonts, akzent), "marke")
    aus = f",fade=out:st={t_karte - 0.25:.2f}:d=0.25:alpha=1" if r.get("karte_oben") else ""
    filt.append(f"[{n}:v]format=rgba,fade=in:st=0.15:d=0.3:alpha=1{aus}[m]")
    filt.append(f"[{letzter}][m]overlay=x=0:y='150-90*pow(1-min(1,max(0,t-0.15)/0.35),3)'[vm]")
    letzter = "vm"
    # Schlagzeilen: springen von unten herein, jede bleibt bis zur nächsten.
    for i, (zeilen, _) in enumerate(r["zeilen"]):
        a = starts[i]
        b = starts[i + 1] if i + 1 < len(r["zeilen"]) else t_karte
        n = ebene(schlagzeile(zeilen, fonts), f"z{i}")
        filt.append(f"[{n}:v]format=rgba,fade=in:st={a:.2f}:d=0.12:alpha=1,"
                    f"fade=out:st={b - 0.12:.2f}:d=0.12:alpha=1[c{i}]")
        filt.append(f"[{letzter}][c{i}]overlay=x=0:y='1130+110*pow(1-min(1,max(0,t-{a:.2f})/0.22),3)':"
                    f"enable='between(t,{a:.2f},{b:.2f})'[vc{i}]")
        letzter = f"vc{i}"
    # Schlusskarte fährt hoch.
    bild, y = karte(r, fonts)
    n = ebene(bild, "karte")
    filt.append(f"[{n}:v]format=rgba,fade=in:st={t_karte:.2f}:d=0.3:alpha=1[k]")
    filt.append(f"[{letzter}][k]overlay=x=0:y='{y}+140*pow(1-min(1,max(0,t-{t_karte:.2f})/0.4),3)':"
                f"enable='gte(t,{t_karte:.2f})',format=yuv420p[out]")
    # Ton: Originalton leiser, Stimme darüber.
    filt.append(f"[0:a]volume=0.32,apad[bg];[1:a]adelay={int(START * 1000)}:all=1,volume=1.7,apad[st];"
                f"[bg][st]amix=inputs=2:normalize=0,alimiter=limit=0.95[aout]")

    ziel = ZIEL / f"{slug}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(roh), "-i", str(vo), *eingaben,
                    "-filter_complex", ";".join(filt), "-map", "[out]", "-map", "[aout]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", "30",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
                    "-t", f"{t:.2f}", str(ziel)], check=True)
    print(f"  {ziel.relative_to(ROOT)}  {t:.1f} s  Sätze ab {[round(s, 2) for s in starts]}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    quelle = Path(sys.argv[1])
    fonts, tmp = quelle / "fonts", quelle / "tmp"
    tmp.mkdir(exist_ok=True)
    ZIEL.mkdir(parents=True, exist_ok=True)
    for slug in (sys.argv[2:] or REELS):
        if (quelle / f"{slug}.mp4").exists() and (quelle / f"{slug}.wav").exists():
            bauen(quelle, slug, fonts, tmp)
        else:
            print(f"  fehlt: {slug}.mp4 oder {slug}.wav")


if __name__ == "__main__":
    main()
