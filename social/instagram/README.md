# Instagram-Reels – Service-Punkt Yakut

Stand: 14.11.2026. Drei Werbevideos im Hochformat (1080 × 1920, 10 Sekunden, mit Ton).
Erzeugt mit Higgsfield (Modell Seedance 2.5), Texteinblendung mit `tools/reels.py`.

Die fertigen Videos liegen im Higgsfield-Konto des Inhabers (Mediathek), nicht in diesem Repository.

| Reel | Einblendung | Schlusskarte |
|---|---|---|
| Schuhreparatur | Schuhreparatur – Absätze · Sohlen · Nähte · Pflege | im Globus Gensingen, Mo–Sa 09–18 Uhr |
| Schlüssel nachmachen | Original mitbringen. Kopie mitnehmen. | im Globus Gensingen, Mo–Sa 09–18 Uhr |
| Türöffnung 24/7 | Ausgesperrt? Wir sind da. Rund um die Uhr. | Notdienst 0179 5056633 |

Alle Angaben stammen aus `data/firma.json` und `data/leistungen.json`. Keine Preise, keine Zeitversprechen.

## Zweite Fassung mit Sprecherstimme (14.11.2026)

Auf Wunsch des Inhabers gibt es alle Reels zusätzlich mit deutscher Sprecherstimme (Higgsfield, ElevenLabs, Stimme „Mark“),
fetten animierten Schlagzeilen und einfahrender Schlusskarte. Erzeugt mit `tools/reels_stimme.py`.
Neu dazu: **Gravur zu Weihnachten** (Edelstahl, Glas, Kunststoff, Holz – Materialien laut Inhaber vom 14.11.2026).

| Reel | Sprechertext |
|---|---|
| Schuhreparatur | Lieblingsschuhe kaputt? Kein Problem! Absätze, Sohlen, Nähte und Pflege – wir machen sie wieder fit. Service-Punkt Yakut, im Globus Gensingen! |
| Schlüssel nachmachen | Schlüssel nachmachen? Ganz einfach! Original mitbringen, Kopie mitnehmen. Für Haus, Wohnung und Briefkasten. Service-Punkt Yakut, im Globus Gensingen! |
| Türöffnung 24/7 | Ausgesperrt? Keine Panik! Unser Notdienst ist rund um die Uhr für Sie da. Service-Punkt Yakut – jetzt anrufen! |
| Gravur zu Weihnachten | Das perfekte Weihnachtsgeschenk? Persönlich graviert! Auf Edelstahl, Glas, Kunststoff und Holz. Jetzt bei Service-Punkt Yakut, im Globus Gensingen! |

Hinweis: Die Website nennt bei der Gravur bisher Holz, Metall, Kunststoff und Leder. Glas fehlt dort noch.

## Texte zum Einfügen

**Gravur zu Weihnachten**

> Das perfekte Weihnachtsgeschenk? Persönlich graviert! 🎁
> Namen, Daten oder Motive auf Edelstahl, Glas, Kunststoff und Holz – bei uns im Globus Gensingen.
> Mo–Sa 09–18 Uhr · yakut-service.de
>
> #gravur #lasergravur #weihnachtsgeschenk #personalisiert #geschenkidee #gensingen #globusgensingen #badkreuznach #bingen

**Schuhreparatur**

> Gute Schuhe verdienen ein zweites Leben. 👞
> Absätze, Sohlen, Nähte und Pflege – direkt im Globus Gensingen, an der Information beim Hintereingang.
> Mo–Sa 09–18 Uhr · yakut-service.de
>
> #schuhreparatur #schuster #schuhpflege #gensingen #globusgensingen #badkreuznach #bingen #handwerk

**Schlüssel nachmachen**

> Original mitbringen. Kopie mitnehmen. 🔑
> Schlüssel für Haus, Wohnung und Briefkasten – bei uns im Globus Gensingen.
> Mo–Sa 09–18 Uhr · yakut-service.de
>
> #schlüsseldienst #schlüsselnachmachen #schlüssel #gensingen #globusgensingen #badkreuznach #bingen

**Türöffnung 24/7**

> Ausgesperrt? Wir sind da. Rund um die Uhr. 🚪
> Türöffnungs-Notdienst für Gensingen, Bad Kreuznach, Bingen und Umgebung.
> Notdienst: 0179 5056633 – bitte den Preis vorab am Telefon erfragen.
>
> #schlüsselnotdienst #türöffnung #schlüsseldienst #gensingen #badkreuznach #bingen #alzey #notdienst

## Beim Hochladen beachten

- In Instagram den Schalter **„KI-Label hinzufügen“** einschalten. Die Videos sind fotorealistisch und mit KI erstellt.
  Auf der Schlusskarte steht zusätzlich „Symbolvideo, mit KI erstellt“.
- Titelbild: das Bild der Schlusskarte wählen (Name und Ort sind dann im Profilraster lesbar).
- Die Texttafeln liegen im sicheren Bereich und werden von den Instagram-Schaltflächen nicht verdeckt.

## Neu erzeugen

Rohvideos als `schuhreparatur.mp4`, `schluessel.mp4`, `tueroeffnung.mp4` in einen Ordner legen,
dazu die Schrift Cormorant als TTF in den Unterordner `fonts/`
(`cormorant-500.ttf`, `cormorant-500i.ttf`, `cormorant-600.ttf`), dann:

```bash
python3 tools/reels.py <ordner>
```

Texte ändern: Tabelle `REELS` in `tools/reels.py`.
