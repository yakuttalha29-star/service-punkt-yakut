# Service-Punkt Yakut – Bestandsaufnahme & Plan (Stand 04.11.2026)

## 1. Was tatsächlich verfügbar ist (geprüft)

| Bereich | Ergebnis |
|---|---|
| Projektdateien | Keine. Das Arbeitsverzeichnis der Sitzung war leer. |
| GitHub-Repositories | Keine verbunden. `gh` hat kein gültiges Token. |
| yakut-service.de | Nicht erreichbar: Das Netzwerk der Sitzung blockiert die Domain, der Fetch-Dienst kann sie nicht per DNS auflösen. |
| Alte ChatGPT-Site | Nicht erreichbar (gleicher Grund). |
| Google-Unternehmensprofil, Instagram, Shop, Zahlungsanbieter | Keine Zugänge vorhanden. |
| Telefon, E-Mail, Straße, WhatsApp | Nicht bekannt. Im Code als `TODO` / `data-todo` markiert. |

**Folge:** Die bestehende Website konnte **nicht** analysiert werden. Alles unten basiert auf den Angaben aus dem Auftrag.

## 2. Fünf Prioritäten

1. **Zugang zum Quellcode bzw. Hosting klären.** Womit ist yakut-service.de gebaut, wo gehostet, wer hat Zugriff? Ohne diese Information kann nichts veröffentlicht werden. *(Entscheidung/Info vom Inhaber)*
2. **Google-Unternehmensprofil vervollständigen.** Das ist der größte Hebel für „Schlüsseldienst Gensingen“ usw.: Kategorien (Schlüsseldienst, Schuhmacher, Graveur), Fotos, Leistungen, Öffnungszeiten, Bewertungen aktiv anfragen (QR-Code an der Theke). Kostenlos, wirkt schneller als jede Website-Änderung. *(Musti)*
3. **Neue Startseite live bringen**, mobil optimiert, mit 7 Leistungskacheln, Anruf-Button und LocalBusiness-Strukturdaten (Prototyp liegt vor), danach **eine Unterseite pro Leistung** und **Ortsseiten** (Bad Kreuznach, Bingen, Alzey …) mit echtem, einzigartigem Inhalt. *(Cihan, Musti)*
4. **Shop-Plattform entscheiden und mit 10–15 Produkten starten**, zuerst Firmenstempel und Gravurschilder (hohe Marge, gut versendbar, B2B-tauglich). Rechtstexte (Impressum, Datenschutz, AGB, Widerruf; Hinweis, dass für personalisierte Ware kein Widerrufsrecht gilt, § 312g Abs. 2 Nr. 1 BGB) über einen Rechtstexte-Dienst. *(Cihan, Samet; kostenpflichtig → Freigabe nötig)*
5. **B2B-Liste aufbauen und ein Firmenangebot formulieren:** Hausverwaltungen, Autohäuser und Vereine im Umkreis von 30 km, Paket aus Schließanlagen, Schlüsselverwaltung, Stempeln, Türschildern und Pokalen. E-Mail-Entwürfe werden nur nach Freigabe versendet. *(Böcek)*

## 3. Architektur-Empfehlung

```
                 ┌──────────────────────────────┐
  Kunden ───────▶│ Website (statisch, schnell)  │  yakut-service.de
                 │ Startseite, Leistungs- und   │  Hosting z. B. Netlify/Cloudflare Pages (gratis)
                 │ Ortsseiten, Kontakt          │
                 └──────────┬───────────────────┘
                            │ Link „Shop“
                 ┌──────────▼───────────────────┐
                 │ Shop-System (gehostet)       │  shop.yakut-service.de
                 │ Produkte, Varianten,         │  Option A: Shopify + Personalisierungs-App
                 │ Gravurtext, Logo-Upload,     │  Option B: WooCommerce (günstiger, mehr Pflege)
                 │ Warenkorb, Checkout, Versand │
                 └──────────┬───────────────────┘
                            │ API (Bestellungen, Umsatz)
                 ┌──────────▼───────────────────┐
                 │ Geschäfts-Dashboard          │  Phase 1: Aufgaben/Entscheidungen manuell gepflegt
                 │ Bestellungen, Anfragen, B2B, │  Phase 2: Shop-API, Google-Profil, Instagram anbinden
                 │ Marketing, Agenten-Aufgaben  │  Beispieldaten immer gekennzeichnet
                 └──────────────────────────────┘
```

**Warum kein selbst programmierter Checkout:** Zahlungsabwicklung, Steuern, Rechnungen und Rechtssicherheit selbst zu bauen ist für einen Einzelbetrieb teurer und riskanter als ein bewährtes Shopsystem. Eigene Entwicklung lohnt sich dort, wo sie Wettbewerbsvorteile bringt: Gravur-Live-Vorschau, Website, Dashboard.

**Shop-Entscheidung (Inhaber):**
- **Shopify:** ab ca. 30–40 €/Monat plus App für Personalisierung; am wenigsten technischer Aufwand.
- **WooCommerce:** Hosting ca. 5–15 €/Monat, Plugins teils kostenpflichtig, Updates und Sicherheit sind Daueraufwand.
- Empfehlung: **Shopify**, weil der Inhaber im Laden arbeitet und keine Server pflegen soll. Preise vor Buchung tagesaktuell prüfen.

## 4. Was bereits umgesetzt ist (lokal, nicht veröffentlicht)

- `index.html` + `assets/styles.css`: neue Startseite, dunkles Design, 7 Kacheln, Notdienst-Leiste, Anruf-Button, Schema.org-Daten (`Locksmith`).
  Geprüft mit Chromium: iPhone 13 → alle 7 Kacheln im ersten Bildschirm, kein horizontales Scrollen; Desktop 1280 px → alle Kacheln sichtbar.
- `data/shop-katalog.json`: Struktur für Kategorien, Varianten, Gravurtext, Logo-Upload, Staffelpreise. **Alle Preise sind Beispieldaten.**

**Noch offen:** Unterseiten (`leistungen/*.html`, `shop/`, Impressum, Datenschutz, AGB) existieren noch nicht. Die Links führen ins Leere.

## 5. Vom Inhaber benötigt

1. Telefonnummer, Notdienstnummer, WhatsApp, E-Mail, genaue Adresse
2. Wer betreut yakut-service.de, mit welchem System? Zugang zum Code oder Hosting?
3. Netzwerkfreigabe dieser Umgebung für `yakut-service.de` (damit die Seite analysiert werden kann)
4. Ein GitHub-Repository, damit die Arbeit dauerhaft gespeichert wird
5. Echte Fotos (Laden, Gravurbeispiele, Schuhreparaturen)
6. Shop-Entscheidung: Shopify oder WooCommerce
