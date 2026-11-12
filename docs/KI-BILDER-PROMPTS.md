# KI-Bildwelt für yakut-service.de – Prompts und Ablauf

Stand: 12.11.2026. In der Entwicklungsumgebung steht kein Bild- oder Videogenerator zur Verfügung.
Diese Datei enthält deshalb fertige Prompts zum Einfügen in ein Bild- bzw. Videomodell.
Die Website ist bereits vorbereitet: fertige Dateien in `fotos/quelle/ki/` ablegen, zwei Befehle ausführen, fertig (siehe Abschnitt 6).

Die Prompts sind auf Englisch, weil Bild- und Videomodelle damit am zuverlässigsten arbeiten.

---

## 1. Ablauf in Kurzform

1. **Stil-Block** (Abschnitt 2) an jeden Prompt anhängen. So sehen alle Bilder aus wie aus einer Serie.
2. Pro Motiv 4 bis 8 Varianten erzeugen und die beste auswählen (Checkliste in Abschnitt 5).
3. Für Videos zuerst das Standbild erzeugen, dann dieses Bild im Videomodell animieren („image to video“). Das hält Bild und Video im selben Stil.
4. Datei mit dem vorgegebenen Dateinamen in `fotos/quelle/ki/` legen.

Geeignet sind alle aktuellen Bildmodelle mit fotorealistischer Ausgabe (z. B. Midjourney, Flux, Imagen, ChatGPT-Bildgenerierung) und Videomodelle mit Bild-zu-Video-Funktion (z. B. Veo, Kling, Runway, Sora). Wichtig ist nur: höchste verfügbare Auflösung, Seitenverhältnis wie angegeben, kommerzielle Nutzung laut Tarif erlaubt.

---

## 2. Stil-Block (an jeden Bild-Prompt anhängen)

```
Style: high-end commercial product photography by a luxury advertising agency. Shot on a medium-format
camera with a 100mm macro lens, f/8, tack-sharp focus on the subject, shallow natural falloff.
Soft cinematic studio lighting: large diffused key light from the upper left, subtle warm rim light,
gentle realistic contact shadows. Seamless bright background in warm ivory and soft cream tones,
surface of honed light travertine stone. Restrained colour palette: ivory, cream, brushed steel,
warm brass and champagne-gold accents, deep cognac leather. Physically accurate materials and
reflections, fine surface micro-detail, natural imperfections. Minimal, calm, generous negative space.
Photorealistic, no illustration, no 3D-render look.
```

**Ausschluss-Block** (als „negative prompt“ bzw. mit `--no`, sonst als Satz „Avoid: …“ anhängen):

```
people, hands, fingers, faces, text, letters, numbers, logos, brand names, watermarks, signatures,
warped or melted metal, impossible key shapes, extra or fused key teeth, floating objects,
distorted reflections, plastic look, oversaturated colours, heavy HDR, lens flares, clutter, dark background
```

Die Markenfarbe der Website ist Gold `#e8c37a` auf Schwarz. Die Messing- und Champagner-Akzente im Stil-Block greifen dieses Gold auf, damit helle Bilder und dunkle Seite zusammenpassen.

---

## 3. Bildmotive

Format: **1:1** für Leistungskacheln und Unterseiten (mindestens 2048 × 2048 px), **16:9** für den Hero (mindestens 3840 × 2160 px). Das Hauptmotiv gehört in die Bildmitte, weil der Hero auf dem Smartphone auf 4:5 beschnitten wird.

### 3.1 Hero der Startseite – `hero.png` (16:9)

```
A refined still life arranged with generous spacing on honed light travertine: a newly cut brass
house key lying flat, a modern brushed-nickel euro profile lock cylinder standing upright, one
hand-welted cognac leather oxford shoe in three-quarter view, and a small brushed stainless-steel
plate with an abstract engraved line ornament. All four objects grouped in the centre third of the
frame, calm empty space left and right. Low camera angle, long soft shadows, a thin warm light
streak across the stone.
```

### 3.2 Schlüssel nachmachen – `schluessel.png` (1:1)

```
Extreme macro of a single freshly cut brass cylinder key resting on brushed steel, a few fine
curled brass shavings beside the cuts, crisp machined edges catching the light. The key has one
simple, plausible row of cuts along one edge and a plain round bow without any marking.
```

### 3.3 Schließanlagen & Zylinder – `schliessanlagen.png` (1:1)

```
A modern euro profile double lock cylinder in brushed nickel, standing upright on light stone,
photographed slightly from the side so the keyway and the cam are visible. One matching plain
key lies next to it. Precise machining marks, soft gradient reflection along the cylinder body.
```

### 3.4 Türöffnung 24/7 – `tueroeffnung.png` (1:1)

```
Close-up of a contemporary front door in matte anthracite with a slim brushed stainless-steel
lever handle and a flush security escutcheon around a profile cylinder. Warm evening light from
the side grazes the door surface, a soft glow suggests a lit hallway behind the door edge.
Architectural, calm, trustworthy.
```

Für dieses Motiv im Stil-Block den Hintergrundsatz weglassen und im Ausschluss-Block „dark background“ streichen. Die Tür selbst ist der Hintergrund.

### 3.5 Schuhreparatur – `schuhreparatur.png` (1:1)

```
A single hand-welted cognac leather oxford shoe on a pale oak workbench, freshly polished with a
deep mirror shine on the toe cap, new leather sole edge neatly trimmed. Beside it a wooden shoe
last, a horsehair brush, a small tin of wax and a spool of waxed thread, arranged with space
between the objects. Visible leather grain and stitch detail.
```

**Kein Vorher-Nachher-Bild per KI.** Ein erzeugtes Vorher-Nachher zeigt ein Ergebnis, das es nie gab, und kann als irreführende Werbung gewertet werden. Für Vorher-Nachher bitte zwei echte Handyfotos einer eigenen Reparatur verwenden (gleicher Winkel, gleiches Licht); die werden dann wie die anderen echten Fotos aufbereitet.

### 3.6 Lasergravur – `gravur.png` (1:1)

```
Macro of a laser engraving in progress on a brushed stainless-steel plate: a fine bright point of
light with a delicate wisp of smoke, half of an elegant abstract line ornament already engraved in
crisp dark contrast. Only the plate and a soft blurred hint of the laser head above it.
```

Ergänzende Motive für die Unterseite (optional, gleiche Machart):

```
A clear crystal glass block with a fine frosted engraved botanical line ornament, standing on
light stone, backlit so the engraving glows softly.
```

```
A slim brushed-brass door nameplate with two blank engraved hairlines as a decorative border,
mounted on a pale plaster wall, soft side light.
```

### 3.7 Stempel & Schilder – `stempel.png` (1:1)

```
A classic company stamp with a turned dark walnut handle and brass ferrule standing next to a
modern black self-inking stamp, on heavy cream cotton paper. In front of them a fresh, sharp stamp
impression made of abstract lines and a simple rectangular frame in deep blue ink.
```

### 3.8 Pokale & Medaillen – `pokale.png` (1:1)

```
An elegant slim gold trophy cup on a black marble base with a blank brushed-gold plaque, standing
on light stone. Beside it a single gold medal on a folded ribbon in deep navy. Clean reflections,
no ornament overload.
```

### 3.9 Onlineshop – `shop.png` (1:1) und Produktbilder

Übersichtsbild für die Shop-Seite:

```
Top-down flat lay on light travertine, evenly spaced: a cognac leather key fob with a brass ring,
a small brushed-aluminium door plate, a gold medal with navy ribbon, a self-inking stamp and a
small oak cutting board. Every engravable surface is blank. Soft even daylight, tidy grid layout.
```

Einzelne Produktbilder (für den späteren Shop, Dateinamen frei wählbar):

```
A cognac full-grain leather key fob with brass ring and blank oval embossing area, on light stone,
45-degree product angle.
```

```
A brushed-aluminium door plate, 150 by 50 millimetres, blank, with two countersunk screw holes,
floating slightly above light stone with a soft shadow.
```

```
A rectangular oak cutting board with a blank engraving area in the lower right corner, leaning
against a pale wall, a linen cloth beside it.
```

**Beschriftung:** Alle gravierbaren Flächen bleiben im KI-Bild leer. Namen und Texte setzen wir danach sauber per Grafik ein. So gibt es keine verzerrten Buchstaben, und derselbe Rohling lässt sich für viele Beispiele nutzen.

---

## 4. Videos

Vorgaben: 16:9, 5 bis 8 Sekunden, ohne Ton, ruhige Kamera, als Schleife geeignet (Anfang und Ende ähnlich). Zuerst das Standbild aus Abschnitt 3 erzeugen und als Startbild hochladen, dann diesen Bewegungs-Prompt verwenden.

### 4.1 Schlüssel wird gefräst – `schluessel.mp4`

```
Slow-motion macro. A rotating steel cutter moves steadily along the edge of a brass key blank
clamped in a vice, cutting a clean row of notches. Fine brass chips fly off and catch the light.
Locked-off camera, shallow depth of field, 120 fps look. No hands, no text.
```

### 4.2 Schuhreparatur – `schuhreparatur.mp4`

```
Slow, smooth dolly move along a cognac leather oxford shoe on a pale oak workbench. A horsehair
brush mounted on a slowly turning polishing wheel glides over the toe cap and the shine deepens.
Dust motes in warm side light. No people, no hands, no text.
```

### 4.3 Laser graviert ein Metallschild – `gravur.mp4`

```
Macro. A bright laser point travels in smooth lines across a brushed stainless-steel plate and
leaves a crisp dark abstract line ornament behind it. A thin wisp of smoke rises and drifts away.
Camera slowly pushes in. No text, no letters.
```

### 4.4 Schließzylinder – `schliessanlagen.mp4`

```
Cinematic product reveal. A brushed-nickel euro profile lock cylinder stands on light stone and
rotates slowly a quarter turn while a soft light sweep travels along its body. A plain key slides
into the keyway and turns once. Seamless bright background. No hands, no text.
```

### 4.5 Hero – `hero.mp4` (optional)

```
Very slow lateral camera glide across the still life. A warm light streak moves gently over the
stone, reflections shift on the brass key and the nickel cylinder. Nothing else moves. Loopable.
```

Menschen und Hände sind bewusst ausgeschlossen. Sie sind die häufigste Fehlerquelle in KI-Videos und würden außerdem wie Aufnahmen aus der eigenen Werkstatt wirken.

---

## 5. Auswahl-Checkliste

Ein Bild kommt nur auf die Website, wenn alle Punkte stimmen:

- Schlüssel: genau eine Reihe Einschnitte, gerader Schaft, kein verschmolzenes oder doppeltes Profil
- Zylinder: Schlüsselkanal und Schließnase an der richtigen Stelle, keine zusätzlichen Öffnungen
- Maschinen und Werkzeuge: nur im Anschnitt oder unscharf, nichts technisch Unsinniges im Fokus
- keine Hände, Personen, Schriftzeichen, Logos oder Markennamen (auch keine angedeuteten)
- Schatten und Spiegelungen passen zur Lichtrichtung von links oben
- Farben und Hintergrund passen zu den übrigen Bildern der Serie
- Motiv sitzt mittig genug für den Zuschnitt auf dem Smartphone

---

## 6. Einbau in die Website

| Datei in `fotos/quelle/ki/` | erscheint |
|---|---|
| `hero.png` oder `hero.mp4` | Startseite, große Fläche unter der Leistungsübersicht |
| `tueroeffnung`, `schluessel`, `schliessanlagen`, `schuhreparatur`, `gravur`, `stempel`, `pokale` | Kachel auf der Startseite und Kopf der jeweiligen Leistungsseite |
| `shop.png` | Shop-Seite |

Liegt zu einem Namen ein Video vor, wird das Video gezeigt und das gleichnamige Bild als Vorschaubild verwendet.

```bash
python3 tools/medien.py   # erzeugt WebP in mehreren Größen, JPEG-Rückfall, komprimiertes MP4
python3 tools/build.py    # baut die Seiten neu
```

Was automatisch passiert:

- **Ladezeit:** WebP in 480 bis 2400 px Breite, der Browser lädt nur die passende Größe. Bilder laden erst beim Scrollen. Videos sind stumm, auf 1280 px begrenzt und starten erst, wenn sie sichtbar sind.
- **Smartphone:** feste Seitenverhältnisse, kein Verrutschen des Layouts beim Laden.
- **SEO:** beschreibende Alternativtexte aus `data/medien.json`, feste Breiten- und Höhenangaben.
- **Kennzeichnung:** Bilder aus `ki/` bekommen den Zusatz „(Symbolbild)“ im Alternativtext, und im Seitenfuß erscheint ein Hinweis, dass KI-Symbolbilder keine Aufnahmen aus dem Laden und keine Kundenarbeiten zeigen.
- **Barrierefreiheit:** Bei der Systemeinstellung „Bewegung reduzieren“ starten Videos nicht von selbst.

Ein KI-Bild ersetzt das echte Foto gleichen Namens aus `fotos/quelle/echt/`. Das echte Foto bleibt im Ordner erhalten.
