# Recherche: Shopify, Hosting, ChatGPT Sites (Stand 04.11.2026)

> **Wichtig:** Offizielle Seiten (shopify.com, help.openai.com, apps.shopify.com) waren aus der Arbeitsumgebung nicht abrufbar. Alle Angaben stammen aus Suchergebnis-Auszügen und widersprechen sich teilweise. **Vor jeder Buchung die Preise auf der offiziellen Seite prüfen.**

## Shopify – Kosten

| Plan | ca. Preis/Monat | Eignung |
|---|---|---|
| Starter | ~5 $ + **5 % Transaktionsgebühr** | Ungeeignet: kein Theme-Editor, also keine Gravur- und Upload-Felder |
| **Basic** | ~25–29 € jährlich / ~33–39 € monatlich | **Empfohlen** für 10–50 Bestellungen im Monat |
| Grow | ~66–89 € jährlich | erst bei deutlich mehr Umsatz |

- Mit Shopify Payments keine zusätzliche Transaktionsgebühr. Kartengebühr laut Quellen ca. 2,1 % + 0,30 € (Basic).
- Testphase laut Quellen: 3 Tage gratis, danach 3 Monate je 1 € (aktionsabhängig).
- **Gravurtext** geht ohne App (Line-Item-Properties im Theme).
- **Logo-Upload** ohne App ist unzuverlässig, deshalb eine App nutzen:
  - Globo Product Options: Free / 9,90 $ / 19,90 $ (Live-Vorschau ab 19,90 $)
  - Infinite Options: 12,99 $
  - Customily: ~49 $ + Gebühr pro Artikel, beste Live-Vorschau
- **Realistische Startkosten:** Basic jährlich (~25–29 €) + Globo (0–20 $) + Rechtstexte (~10 €) ≈ **35–60 € pro Monat**.

## Integration in die Website

- Website bleibt statisch auf `yakut-service.de` (kostenlos gehostet).
- Shop auf **`shop.yakut-service.de`**: bei IONOS ein CNAME-Eintrag `shop` → `shops.myshopify.com`.
- Gleiches Design über ein angepasstes Shopify-Theme (dunkel, gleiche Farben und Schrift), gegenseitige Navigation.
- Alternative „Buy Button“: einzelne Produkte direkt auf der Website. Das geht in allen Plänen, ist für Gravur und Upload aber weniger geeignet.

## Recht (Shop)

- Impressum nach § 5 DDG.
- Kein Widerrufsrecht für gravierte bzw. individuelle Ware (§ 312g Abs. 2 Nr. 1 BGB), trotzdem Widerrufsbelehrung mit Hinweis darauf.
- Bestell-Button „zahlungspflichtig bestellen“.
- **LUCID-Registrierung + Systembeteiligung** für Versandverpackungen **vor dem ersten Versand** (Registrierung kostenlos, Systembeteiligung kostenpflichtig). Laut Quellen gilt seit 12.08.2026 neues Verpackungsrecht (PPWR/VerpackDG), bei der ZSVR prüfen.
- Die EU-OS-Plattform wurde am 20.07.2025 abgeschaltet. Kein Link mehr nötig, Hinweis nach § 36 VSBG bleibt relevant.
- Rechtstexte-Dienste mit Shopify-Anbindung: IT-Recht Kanzlei oder Händlerbund ab ca. 9,90 €/Monat, eRecht24 ab ca. 15 €/Monat.

## Bisherige Website (ChatGPT Sites)

- `*.chatgpt.site` ist das OpenAI-Produkt „ChatGPT Sites“.
- Eigene Domain ist dort möglich, aber laut Community-Berichten teils fehleranfällig.
- Ein offizieller Code-Export ist nicht dokumentiert.
- **Empfehlung:** nicht dort weiter hosten. Inhalte und Bilder aus dem ChatGPT-Chat sichern und in dieses Projekt übernehmen.

## Hosting für 0 €

- **Cloudflare Pages (empfohlen):** kostenlos, gewerblich nutzbar, eigene Domain, SSL.
- Netlify Free: Alternative.
- Vercel Hobby: **nicht** für Gewerbe erlaubt.
- GitHub Pages: bei privatem Repo nur mit Bezahl-Plan.
- **IONOS-Hostingpaket ist nicht nötig.** Nur die Domain bei IONOS behalten und in der IONOS-DNS-Verwaltung auf Cloudflare Pages zeigen lassen. **E-Mail-Einträge (MX) nicht verändern.**
