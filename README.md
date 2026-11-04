# Service-Punkt Yakut – Website

Website von **Service-Punkt Yakut – Schuh- & Schlüsseldienst Yakut** (Globus Gensingen).
Statische Seiten mit dunklem, minimalistischem Design. Sie laufen kostenlos auf jedem statischen Hosting.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `data/firma.json` | **Einzige Quelle** für Firmendaten (Adresse, Telefon, Öffnungszeiten …). `null` = noch nicht geliefert. |
| `data/leistungen.json` | Texte der 7 Leistungen (Startseite + Unterseiten). |
| `tools/build.py` | Erzeugt alle Seiten aus `firma.json` und `leistungen.json`. |
| `assets/img/<slug>.jpg` | Optional: echte Fotos, z. B. `gravur.jpg`. Ersetzen automatisch die Illustration. |
| `public/` | **Erzeugte** Website, nur dieser Ordner wird veröffentlicht. Nicht von Hand bearbeiten, sondern `build.py` ausführen. |
| `entwurf/` | Impressum und Datenschutz als **Entwurf**. Erst veröffentlicht, wenn alle Angaben vollständig sind und in `firma.json` `"rechtstexte_freigegeben": true` steht. |
| `assets/styles.css` | Design im Apple-Stil (Farben als Variablen in `:root`). Nur Systemschriften, keine Google Fonts. |
| `data/shop-katalog.json` | Produktstruktur für den Shopify-Import. **Preise sind Beispiele.** |
| `docs/` | Bestandsaufnahme, Plan, Entscheidungen. |

## Seiten neu erzeugen

```bash
python3 tools/build.py
```

Das Skript listet am Ende alle fehlenden Pflichtangaben auf. Fehlende Werte werden nie erfunden, sondern als „… folgt“ angezeigt und nicht verlinkt.

## Lokal ansehen

```bash
python3 -m http.server 8000 -d public
```

Dann im Browser `http://localhost:8000` öffnen.

## Veröffentlichen

Cloudflare Pages (kostenlos), siehe `docs/VEROEFFENTLICHEN-CLOUDFLARE.md`. Build command `python3 tools/build.py`, Ausgabeordner `public`.

## Regeln

- Keine Passwörter oder API-Schlüssel ins Repository.
- Keine Veröffentlichung ohne Freigabe des Inhabers.
- Impressum und Datenschutz erst live schalten, wenn sie rechtlich geprüft sind.
