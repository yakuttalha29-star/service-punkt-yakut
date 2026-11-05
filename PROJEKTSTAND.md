# Projektstand – Service-Punkt Yakut (05.11.2026)

Übergabe für neue Sitzungen. Zuerst diese Datei lesen, dann `README.md` und `docs/`.

## Erledigt (lokal, NICHT online)
- Website im Apple-Stil (dunkel): Startseite, 7 Leistungsseiten, Shop-Hinweis, 404. Generator: `python3 tools/build.py` → `public/`
- Daten: `data/firma.json` (Firmendaten), `data/leistungen.json` (Texte)
- Impressum + Datenschutz als Entwurf in `entwurf/`. Sie werden erst veröffentlicht, wenn in `firma.json` `"rechtstexte_freigegeben": true` steht.
- Geprüft mit Playwright (iPhone 13 + Desktop): keine kaputten Links, keine JS-Fehler, alle 7 Leistungen im ersten Handy-Bildschirm.

## Entscheidungen des Inhabers (Talha Yakut)
- Hosting: **Cloudflare Pages (kostenlos)**, Domain bleibt bei IONOS. Kein IONOS-Hostingpaket.
- Shopify (Basic): **später**. Zuerst Website online.
- Öffnungszeiten Laden Mo–Sa 09–18 Uhr bestätigt. Schlüssel-Notdienst 24/7, gleiche Nummer.
- **Keine USt-IdNr. vorhanden.** Steuernummer **nicht** veröffentlichen.
- Keine Handwerkskammer-Post erhalten → Kammer-Abschnitt entfällt.
- Keine erfundenen Angaben, keine Veröffentlichung, keine Buchung, keine Kundenkontakte ohne Freigabe.

## Konten
- Cloudflare: Konto angelegt (Free). E-Mail-Bestätigung war ausstehend. Noch kein Projekt anlegen.
- GitHub: Benutzer `yakuttalha29-star`, privates Repo `service-punkt-yakut`. In der ersten Sitzung war kein Zugriff möglich.

## Live (Test-Adresse)
- Seit 05.11.2026 online: https://service-punkt-yakut.service-yakut.workers.dev (Cloudflare Workers mit statischen Dateien, Konfiguration in `wrangler.jsonc`, Build `python3 tools/build.py`, Deploy `npx wrangler deploy`). Jeder Push auf `main` veröffentlicht automatisch.
- Impressum und Datenschutz am 05.11.2026 vom Inhaber freigegeben.

## Nächste Schritte
1. Code ins GitHub-Repo pushen (vollständiger Verlauf aus der ZIP-Sicherung)
2. Inhaber gibt Impressum/Datenschutz frei (oder lässt sie über einen Rechtstexte-Dienst prüfen)
3. Cloudflare Pages mit GitHub verbinden: Build `python3 tools/build.py`, Output `public`
4. Auftragsverarbeitungsvertrag (DPA) im Cloudflare-Konto prüfen/annehmen (Datenschutzerklärung nennt Cloudflare als Auftragsverarbeiter)
5. IONOS-DNS: `www` CNAME → `<projekt>.pages.dev`, Root → www weiterleiten, **MX nicht ändern**
6. Echte Fotos einbauen (`assets/img/<slug>.jpg`)
7. Danach: Google-Unternehmensprofil, Ortsseiten, später Shopify
