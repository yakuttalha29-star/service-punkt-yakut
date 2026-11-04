# Service-Punkt Yakut – Website

Website von **Service-Punkt Yakut – Schuh- & Schlüsseldienst Yakut** (Globus Gensingen).
Statische Seiten mit dunklem, minimalistischem Design. Sie laufen kostenlos auf jedem statischen Hosting.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `data/firma.json` | **Einzige Quelle** für Firmendaten (Adresse, Telefon, Öffnungszeiten …). `null` = noch nicht geliefert. |
| `tools/build.py` | Erzeugt alle Seiten aus `firma.json` und den Leistungstexten (im Skript, Abschnitt `LEISTUNGEN`). |
| `index.html`, `leistungen/*.html`, `shop/index.html` | **Erzeugte** Seiten. Nicht von Hand bearbeiten, sondern `build.py` ausführen. |
| `impressum-entwurf.html` | Impressum-**Entwurf** (`noindex`). Wird erst als `impressum.html` veröffentlicht, wenn alle Angaben vollständig und geprüft sind. |
| `assets/styles.css` | Design (Farben als Variablen in `:root`). |
| `data/shop-katalog.json` | Produktstruktur für den Shopify-Import. **Preise sind Beispiele.** |
| `docs/` | Bestandsaufnahme, Plan, Entscheidungen. |

## Seiten neu erzeugen

```bash
python3 tools/build.py
```

Das Skript listet am Ende alle fehlenden Pflichtangaben auf. Fehlende Werte werden nie erfunden, sondern als „… folgt“ angezeigt und nicht verlinkt.

## Lokal ansehen

```bash
python3 -m http.server 8000
```

Dann im Browser `http://localhost:8000` öffnen.

## Regeln

- Keine Passwörter oder API-Schlüssel ins Repository.
- Keine Veröffentlichung ohne Freigabe des Inhabers.
- Impressum und Datenschutz erst live schalten, wenn sie rechtlich geprüft sind.
