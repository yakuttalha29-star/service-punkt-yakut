# Website veröffentlichen mit Cloudflare Pages (kostenlos)

Entscheidung des Inhabers vom 04.11.2026: **Cloudflare Pages statt IONOS-Hostingpaket.** Die Domain bleibt bei IONOS.

## ⛔ Vorher erfüllt sein muss (sonst nicht live schalten)

Eine gewerbliche Website braucht in Deutschland ein vollständiges **Impressum** und eine **Datenschutzerklärung**. Ohne sie drohen Abmahnungen.

- [ ] Telefon, Notdienstnummer, E-Mail, Straße, Name des Inhabers in `data/firma.json`
- [ ] Impressum (`entwurf/impressum.html`) vollständig und geprüft → als `impressum.html` freigegeben
- [ ] Datenschutzerklärung erstellt und geprüft
- [ ] Freigabe des Inhabers zum Livegang

## Einrichtung (einmalig, ca. 20 Minuten)

1. **Konto anlegen:** auf cloudflare.com kostenlos registrieren (Free-Plan, keine Zahlungsdaten nötig).
2. **Projekt anlegen:** Dashboard → *Workers & Pages* → *Create* → *Pages* → *Connect to Git* → GitHub-Repository `service-punkt-yakut` auswählen.
3. **Build-Einstellungen:**
   - Build command: `python3 tools/build.py`
   - Build output directory: `public`
4. **Testadresse prüfen:** Cloudflare vergibt eine Adresse wie `service-punkt-yakut.pages.dev`. Dort zuerst alles ansehen. Die Seite ist dann zwar öffentlich erreichbar, aber noch nicht unter Ihrer Domain.
5. **Eigene Domain verbinden** (erst nach der Freigabe):
   - In Cloudflare Pages: *Custom domains* → `www.yakut-service.de` hinzufügen. Cloudflare zeigt den nötigen Eintrag an.
   - Bei IONOS: *Domains & SSL* → `yakut-service.de` → *DNS* → für `www` einen **CNAME** auf `service-punkt-yakut.pages.dev` setzen.
   - `yakut-service.de` ohne www bei IONOS auf `www.yakut-service.de` weiterleiten.
   - **MX-Einträge (E-Mail) nicht anfassen.**
   - **Achtung:** Wenn die alte ChatGPT-Seite derzeit unter yakut-service.de läuft, ist sie ab diesem Moment ersetzt. Vorher Texte und Bilder sichern.

## Später: Shop

Bei IONOS einen weiteren CNAME `shop` → `shops.myshopify.com` anlegen (siehe `RECHERCHE-SHOPIFY-HOSTING.md`).

## Kosten

- Cloudflare Pages Free: 0 €
- Laufend nur die IONOS-Domain, wie bisher.
- Falls Cloudflare den Gratis-Tarif einmal ändert, kann die Website ohne Änderungen am Code zu Netlify (ebenfalls gratis) umziehen, da es sich um einfache HTML-Dateien handelt.
