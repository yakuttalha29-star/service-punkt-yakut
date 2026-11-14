# Projektstand – Service-Punkt Yakut (05.11.2026)

Übergabe für neue Sitzungen. Zuerst diese Datei lesen, dann `README.md` und `docs/`.

## Erledigt (lokal, NICHT online)
- Website (ursprünglich dunkel im Apple-Stil, seit 13.11.2026 hell, siehe unten): Startseite, 7 Leistungsseiten, Shop-Hinweis, 404. Generator: `python3 tools/build.py` → `public/`
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

## Domain (05.11.2026)
- yakut-service.de: Nameserver bei IONOS auf Cloudflare umgestellt (mark/raina.ns.cloudflare.com), Zone aktiv. Domain-Registrierung bleibt bei IONOS.
- Custom Domains am Worker: `yakut-service.de` und `www.yakut-service.de`.
- Alte IONOS-Einträge A/AAAA für @ sollten gelöscht sein. MX/TXT/CNAME (IONOS-Mail, SPF, DMARC) unverändert gelassen.
- Fotos online: Schuhreparatur, Gravur (Google-Schild), Stempel (alte Festnetznummer 06727/3819957 unkenntlich – NICHT mehr aktuell).

## Google (05.11.2026)
- Google-Unternehmensprofil vom Inhaber aktualisiert (Website, Telefon, Zeiten, Kategorien, Beschreibung).
- Google Search Console: Domain-Property yakut-service.de per Cloudflare bestätigt, Sitemap https://yakut-service.de/sitemap.xml eingereicht.

## KI-Bildwelt (12.11.2026, Branch `claude/blissful-meitner-02d7vf`, noch nicht auf `main`)
- Inhaber wünscht exklusive, fotorealistische KI-Bilder und kurze Videos (heller Luxus-Studio-Stil) für Hero, Kacheln, Unterseiten, Shop.
- In der Cloud-Sitzung gab es keinen Bild-/Videogenerator. Deshalb: fertige Prompts in `docs/KI-BILDER-PROMPTS.md`, noch KEINE KI-Bilder erzeugt.
- Technik steht: Originale nach `fotos/quelle/ki/`, dann `python3 tools/medien.py` und `python3 tools/build.py`. WebP/srcset, Video stumm und nur bei Sichtbarkeit, KI-Kennzeichnung („Symbolbild“ + Hinweis im Fuß).
- Die drei echten Fotos liegen jetzt in `fotos/quelle/echt/` und werden als WebP ausgeliefert.
- Kein KI-Vorher-Nachher (irreführend), dafür echte Fotos.
- Vom Inhaber geliefert und eingebaut (12.11.2026): KI-Bilder `gravur`, `schliessanlagen`, `schuhreparatur`, `schluessel` (je 1402×1122). Entscheidung Inhaber: KI-Bilder ersetzen die echten Fotos. Noch offen: `hero`, `tueroeffnung`, `stempel` (derzeit echtes Foto), `pokale`, `shop`, Videos.

## Neues helles Design (13.11.2026, gleicher Branch, noch nicht auf `main`)
- Inhaber wollte den Dark Mode nicht mehr. Die Seite ist jetzt hell und redaktionell: Elfenbein, Tinte, Messing, Überschriften in Cormorant Garamond (selbst gehostet). Eigenes Design, keine fremde Website kopiert.
- Startseite: Kopf mit Bild-Collage (Schuh, Schlüssel, Gravur), darunter die 7 Leistungen als Zeilen mit Bild und Text im Wechsel. Unterseiten: Text links, Bild rechts.
- Auf dem Handy bleiben alle 7 Leistungen im ersten Bildschirm.
- Animationen (Wunsch Inhaber, 13.11.2026): Kopf fährt beim Laden von oben/links/rechts ein, Bilder werden aufgezogen mit Lichtreflex, Leistungszeilen kommen beim Scrollen abwechselnd von links und rechts, Fortschrittslinie oben. Reines CSS plus `assets/site.js`, keine Bibliothek. Bei „Bewegung reduzieren“ abgeschaltet.
- `tueroeffnung` nutzt vorläufig einen Ausschnitt des Schließzylinder-Bildes. Ohne Bild: `pokale`, `shop` (zeigen ein Emblem). Stock-Bildquellen waren vom Netzwerk blockiert.

## Instagram-Reels (14.11.2026, Branch `claude/werbevideos-instagram-pclu26`)
- Drei Werbevideos im Hochformat (1080 × 1920, 10 s, mit Ton) mit Higgsfield erzeugt (Seedance 2.5, 720p, je 70 Credits): Schuhreparatur, Schlüssel nachmachen, Türöffnung 24/7.
- Texteinblendung in der Website-Schrift mit `tools/reels.py` (Titeltafel, Schlusskarte mit Ort, Zeiten bzw. Notdienstnummer, Hinweis „Symbolvideo, mit KI erstellt“). Nur Angaben aus `firma.json` und `leistungen.json`.
- Die fertigen Videos liegen in der Higgsfield-Mediathek des Inhabers, nicht im Repository. Texte und Hashtags: `social/instagram/README.md`.
- Zweite Fassung (gleicher Tag): alle Reels mit deutscher Sprecherstimme (ElevenLabs über Higgsfield, Stimme „Mark“), animierten Schlagzeilen und Schlusskarte, erzeugt mit `tools/reels_stimme.py`. Neu: Reel „Gravur zu Weihnachten“ (Edelstahl, Glas, Kunststoff, Holz laut Inhaber). Die Stimme „Max“ des Modells Seed Audio hatte einen starken Akzent und wurde verworfen.
- Offen: Die Gravur-Seite der Website nennt Holz, Metall, Kunststoff, Leder. Glas ggf. ergänzen.
- Noch NICHT gepostet. Veröffentlichung macht der Inhaber selbst.
- Instagram-Konto ist `service.punkt` (vom Inhaber per Screenshot bestätigt am 14.11.2026, 177 Follower). `firma.json` stimmt.

## Nächste Schritte
1. Code ins GitHub-Repo pushen (vollständiger Verlauf aus der ZIP-Sicherung)
2. Inhaber gibt Impressum/Datenschutz frei (oder lässt sie über einen Rechtstexte-Dienst prüfen)
3. Cloudflare Pages mit GitHub verbinden: Build `python3 tools/build.py`, Output `public`
4. Auftragsverarbeitungsvertrag (DPA) im Cloudflare-Konto prüfen/annehmen (Datenschutzerklärung nennt Cloudflare als Auftragsverarbeiter)
5. IONOS-DNS: `www` CNAME → `<projekt>.pages.dev`, Root → www weiterleiten, **MX nicht ändern**
6. Echte Fotos einbauen (`assets/img/<slug>.jpg`)
7. Danach: Google-Unternehmensprofil, Ortsseiten, später Shopify
