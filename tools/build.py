#!/usr/bin/env python3
"""Erzeugt alle HTML-Seiten aus data/firma.json und den Vorlagen in diesem Skript.

Aufruf:  python3 tools/build.py
Fehlende Pflichtangaben (null in firma.json) werden NICHT erfunden, sondern als
sichtbarer Platzhalter ausgegeben und am Ende als Warnung aufgelistet.
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "public"   # nur dieser Ordner wird veröffentlicht (Cloudflare Pages: Ausgabeverzeichnis "public")
FIRMA = json.loads((ROOT / "data" / "firma.json").read_text(encoding="utf-8"))
WARN = set()

def e(s):
    return html.escape(str(s), quote=True)

def val(key, label):
    v = FIRMA.get(key)
    if not v:
        WARN.add(label)
    return v

def tel_link(cls="btn", text="Anrufen", key="telefon"):
    nr = val(key, "Telefon" if key == "telefon" else "Notdienstnummer")
    if not nr:
        return f'<span class="{cls} is-missing" title="Nummer wird nachgereicht">{e(text)} – Nummer folgt</span>'
    return f'<a class="{cls}" href="tel:{e(nr.replace(" ", ""))}">{e(text)}</a>'

def mail_link(cls="btn", text="E-Mail schreiben"):
    m = val("email", "E-Mail")
    if not m:
        return f'<span class="{cls} is-missing">{e(text)} – Adresse folgt</span>'
    return f'<a class="{cls}" href="mailto:{e(m)}">{e(text)}</a>'

def page(path, title, desc, body, depth=0, noindex=False, extra_head=""):
    pre = "../" * depth
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else ""
    canonical = "" if noindex else f'<link rel="canonical" href="{e(FIRMA["website"].rstrip("/") + "/" + path.replace("index.html", ""))}">'
    notdienst_btn = tel_link("emergency-btn", "Jetzt anrufen", key="notdienst")
    doc = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{canonical}{robots}
<meta name="theme-color" content="#0b0b0d">
<link rel="stylesheet" href="{pre}assets/styles.css">
{extra_head}
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<div class="emergency"><span><strong>Ausgesperrt?</strong> Türöffnungs-Notdienst rund um die Uhr</span>{notdienst_btn}</div>
<header class="nav">
  <a href="{pre}index.html" class="brand" aria-label="Startseite">Service‑Punkt <span>Yakut</span></a>
  <nav aria-label="Hauptnavigation">
    <a href="{pre}index.html#leistungen">Leistungen</a>
    <a href="{pre}shop/" class="nav-keep">Shop</a>
    <a href="{pre}index.html#firmen">Firmenkunden</a>
    <a href="{pre}index.html#kontakt" class="nav-keep">Kontakt</a>
  </nav>
</header>
<main id="inhalt">
{body}
</main>
<footer class="foot">
  <p>Einsatzgebiet: {" · ".join(e(o) for o in FIRMA["einzugsgebiet"])}</p>
  <p><a href="{pre}impressum.html">Impressum</a> · <a href="{pre}datenschutz.html">Datenschutz</a></p>
</footer>
</body>
</html>
"""
    out = OUT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")

def standort_html():
    strasse = val("strasse", "Straße & Hausnummer")
    zeile = e(strasse) if strasse else '<span class="is-missing-text">Straße & Hausnummer folgen</span>'
    return (f'{e(FIRMA["name_kurz"])}<br>{e(FIRMA["standort"])}<br>'
            f'{e(FIRMA["standort_detail"])}<br>{zeile}<br>{e(FIRMA["plz"])} {e(FIRMA["ort"])}')

def kontakt_block():
    oz = FIRMA["oeffnungszeiten"]
    return f"""
<section class="contact" id="kontakt">
  <div><h2>Kontakt</h2><p>{standort_html()}</p></div>
  <div><h3>Öffnungszeiten</h3><p>{e(oz["text"])}<br>Notdienst Türöffnung: 24/7</p></div>
  <div class="actions">
    {tel_link()}
    <a class="btn btn-ghost" href="{e(FIRMA["whatsapp_kanal"])}" rel="noopener">WhatsApp-Kanal</a>
    <a class="btn btn-ghost" href="{e(FIRMA["instagram"])}" rel="noopener">Instagram</a>
  </div>
</section>"""

# ---------------------------------------------------------------- Leistungen
# Inhalte bewusst ohne Preise, Anfahrtszeiten oder Zertifikate: nur Aussagen,
# die der Inhaber bestätigt hat. Ergänzungen bitte in diesem Abschnitt pflegen.
LEISTUNGEN = [
  {
    "slug": "tueroeffnung", "icon": "🚪", "titel": "Türöffnung 24/7", "kurz": "Schnell vor Ort, beschädigungsarm.",
    "seo_title": "Türöffnung & Schlüsselnotdienst 24/7 – Gensingen, Bad Kreuznach, Bingen",
    "seo_desc": "Ausgesperrt? Türöffnungs-Notdienst rund um die Uhr für Gensingen, Bad Kreuznach, Bingen, Alzey und Umgebung. Service-Punkt Yakut.",
    "h1": "Türöffnung – rund um die Uhr",
    "lead": "Tür zugefallen, Schlüssel verloren oder abgebrochen? Unser Notdienst ist 24 Stunden am Tag, 7 Tage die Woche erreichbar.",
    "punkte": [
      ("Zugefallene Türen", "Öffnung zugefallener Haus- und Wohnungstüren – wenn möglich ohne Beschädigung des Schlosses."),
      ("Abgeschlossene Türen", "Öffnung verschlossener Türen und anschließend auf Wunsch Austausch des Zylinders."),
      ("Abgebrochener Schlüssel", "Entfernen abgebrochener Schlüssel aus dem Zylinder."),
      ("Nach dem Einsatz", "Neuer Schließzylinder oder Schlüsselkopien direkt bei uns im Globus Gensingen."),
    ],
    "faq": [
      ("Was muss ich bei der Türöffnung vorweisen?", "Zu Ihrer Sicherheit öffnen wir nur, wenn Sie Ihre Berechtigung nachweisen können, z. B. mit Personalausweis mit Meldeadresse oder Mietvertrag."),
      ("Was kostet eine Türöffnung?", "Bitte fragen Sie den Preis am Telefon vor dem Einsatz verbindlich an. So gibt es vor Ort keine Überraschungen."),
    ],
    "notfall": True,
  },
  {
    "slug": "schluessel", "icon": "🔑", "titel": "Schlüssel nachmachen", "kurz": "Haus-, Briefkasten-, Autoschlüssel.",
    "seo_title": "Schlüssel nachmachen im Globus Gensingen – Schlüsseldienst Yakut",
    "seo_desc": "Schlüsselkopien für Haus, Wohnung, Briefkasten und mehr – im Globus Gensingen, meist während Sie warten. Service-Punkt Yakut.",
    "h1": "Schlüssel nachmachen",
    "lead": "Bringen Sie einfach Ihren Originalschlüssel mit – wir fertigen die Kopie in unserem Laden im Globus Gensingen.",
    "punkte": [
      ("Haus- & Wohnungsschlüssel", "Kopien gängiger Bart- und Zylinderschlüssel."),
      ("Briefkasten & Möbel", "Kleine Schlüssel für Briefkasten, Schränke und Vorhängeschlösser."),
      ("Autoschlüssel", "Bitte fragen Sie vorab, ob wir Ihr Modell anfertigen können."),
      ("Sicherungskarte", "Für Schlüssel aus Schließanlagen mit Sicherungskarte bringen Sie bitte die Karte mit."),
    ],
    "faq": [
      ("Brauche ich einen Termin?", "Nein, kommen Sie während der Öffnungszeiten vorbei."),
      ("Können Sie jeden Schlüssel kopieren?", "Nicht jeden. Patentgeschützte Schlüssel können oft nur mit Sicherungskarte über den Hersteller nachbestellt werden. Wir beraten Sie gern."),
    ],
  },
  {
    "slug": "schliessanlagen", "icon": "🛡️", "titel": "Schließanlagen & Zylinder", "kurz": "Beratung, Einbau, Sicherheit.",
    "seo_title": "Schließzylinder & Schließanlagen – Beratung und Einbau | Service-Punkt Yakut",
    "seo_desc": "Sicherheitszylinder und Schließanlagen für Privat, Hausverwaltungen und Firmen in Gensingen, Bad Kreuznach, Bingen und Alzey.",
    "h1": "Schließanlagen & Sicherheitszylinder",
    "lead": "Vom einzelnen Zylinder bis zur Schließanlage für Mehrfamilienhaus oder Betrieb – wir beraten Sie und bauen ein.",
    "punkte": [
      ("Zylinder tauschen", "Nach Schlüsselverlust, Einzug oder Einbruch."),
      ("Sicherheitszylinder", "Mit Bohr- und Ziehschutz für mehr Einbruchschutz."),
      ("Schließanlagen", "Ein Schlüssel für die eigenen Türen, ein Generalschlüssel für alle – geplant nach Ihrem Bedarf."),
      ("Hausverwaltungen & Firmen", "Feste Ansprechpartner und Rechnung."),
    ],
    "faq": [
      ("Wie finde ich die richtige Zylinderlänge?", "Bringen Sie den alten Zylinder mit oder messen Sie von der Mitte der Befestigungsschraube nach außen und innen. Wir helfen gern."),
    ],
  },
  {
    "slug": "schuhreparatur", "icon": "👞", "titel": "Schuhreparatur", "kurz": "Absätze, Sohlen, Nähte, Pflege.",
    "seo_title": "Schuhreparatur im Globus Gensingen – Absätze, Sohlen, Nähte",
    "seo_desc": "Schuhreparatur in Gensingen: neue Absätze, Sohlen, Nähte und Schuhpflege. Service-Punkt Yakut im Globus Gensingen.",
    "h1": "Schuhreparatur",
    "lead": "Gute Schuhe verdienen ein zweites Leben. Bringen Sie sie einfach im Globus Gensingen vorbei.",
    "punkte": [
      ("Absätze", "Neue Absätze und Absatzflecken für Damen- und Herrenschuhe."),
      ("Sohlen", "Erneuerung von Laufsohlen."),
      ("Nähte & Kleinreparaturen", "Nähte, Reißverschlüsse und kleinere Schäden."),
      ("Pflege", "Reinigung und Pflege von Lederschuhen."),
    ],
    "faq": [
      ("Wie lange dauert eine Reparatur?", "Kleine Arbeiten oft sofort, größere nach Absprache. Fragen Sie bei der Abgabe nach dem Abholtermin."),
    ],
  },
  {
    "slug": "gravur", "icon": "✨", "titel": "Lasergravur & Geschenke", "kurz": "Personalisiert, auch Einzelstücke.",
    "seo_title": "Lasergravur & personalisierte Geschenke – Gensingen | Service-Punkt Yakut",
    "seo_desc": "Lasergravur auf Holz, Metall, Kunststoff und Leder: Geschenke, Schlüsselanhänger, Schilder und Firmenlogos – auch Einzelstücke.",
    "h1": "Lasergravur & personalisierte Geschenke",
    "lead": "Namen, Daten, Logos oder Fotos – wir gravieren Einzelstücke und Serien für Privat- und Firmenkunden.",
    "punkte": [
      ("Geschenke", "Personalisierte Geschenke zu Geburtstag, Hochzeit, Jubiläum."),
      ("Schlüsselanhänger", "Mit Namen, Datum oder Logo."),
      ("Gravurschilder", "Türschilder, Klingelschilder, Firmenschilder aus Kunststoff, Messing und Edelstahl."),
      ("Firmenlogos", "Werbeartikel und Mitarbeitergeschenke in Serie."),
    ],
    "faq": [
      ("In welchem Format soll ich mein Logo schicken?", "Am besten als Vektordatei (SVG, PDF, EPS). Gut aufgelöste PNG-Dateien gehen oft auch."),
    ],
  },
  {
    "slug": "stempel", "icon": "🏷️", "titel": "Stempel & Schilder", "kurz": "Firmenstempel, Gravurschilder.",
    "seo_title": "Firmenstempel & Gravurschilder – Gensingen | Service-Punkt Yakut",
    "seo_desc": "Firmenstempel, Adressstempel und Gravurschilder aus Kunststoff, Messing und Edelstahl – im Globus Gensingen und bald im Onlineshop.",
    "h1": "Firmenstempel & Gravurschilder",
    "lead": "Stempel mit Ihrem Text oder Logo und Schilder in Kunststoff, Messing oder Edelstahl.",
    "punkte": [
      ("Firmenstempel", "Selbstfärbende Stempel mit Text und Logo."),
      ("Adress- & Privatstempel", "Für Briefe, Vereine und Praxen."),
      ("Kunststoffschilder", "Türschilder, Hinweisschilder, Namensschilder."),
      ("Messing & Edelstahl", "Hochwertige Praxis-, Kanzlei- und Firmenschilder."),
    ],
    "faq": [
      ("Kann ich online bestellen?", "Der Onlineshop ist in Vorbereitung. Bis dahin bestellen Sie bitte direkt im Laden."),
    ],
  },
  {
    "slug": "pokale", "icon": "🏆", "titel": "Pokale & Medaillen", "kurz": "Für Vereine und Firmen.",
    "seo_title": "Pokale & Medaillen mit Gravur – für Vereine | Service-Punkt Yakut Gensingen",
    "seo_desc": "Pokale, Medaillen und Ehrenpreise mit Gravur für Vereine, Turniere und Firmen in Gensingen, Bad Kreuznach, Bingen und Alzey.",
    "h1": "Pokale & Medaillen",
    "lead": "Für Turniere, Vereinsfeiern und Firmenevents – inklusive Gravur.",
    "punkte": [
      ("Pokale", "Mit gravierter Plakette."),
      ("Medaillen", "Gold, Silber, Bronze – mit individuellem Emblem."),
      ("Ehrenpreise & Plaketten", "Für Jubiläen und Ehrungen."),
      ("Vereine", "Frühzeitig anfragen – auch größere Stückzahlen."),
    ],
    "faq": [
      ("Wie früh sollte ich bestellen?", "Je nach Menge – sprechen Sie uns am besten ein bis zwei Wochen vor dem Termin an."),
    ],
  },
]

def leistung_seite(l):
    punkte = "".join(f'<div class="card"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in l["punkte"])
    faq = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in l["faq"])
    cta = tel_link("btn btn-urgent" if l.get("notfall") else "btn",
                   "Notdienst anrufen" if l.get("notfall") else "Anrufen",
                   key="notdienst" if l.get("notfall") else "telefon")
    andere = "".join(f'<a href="{x["slug"]}.html">{e(x["titel"])}</a>' for x in LEISTUNGEN if x is not l)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in l["faq"]]},
        ensure_ascii=False)
    body = f"""
<nav class="crumbs" aria-label="Brotkrumen"><a href="../index.html">Start</a> › {e(l["titel"])}</nav>
<section class="page-hero">
  <span class="ico" aria-hidden="true">{l["icon"]}</span>
  <h1>{e(l["h1"])}</h1>
  <p class="lead">{e(l["lead"])}</p>
  <div class="actions center">{cta}<a class="btn btn-ghost" href="../index.html#kontakt">Anfahrt & Öffnungszeiten</a></div>
</section>
<section class="cards">{punkte}</section>
<section class="faq"><h2>Häufige Fragen</h2>{faq}</section>
<section class="more"><h2>Weitere Leistungen</h2><div class="chips">{andere}</div></section>
{kontakt_block()}"""
    page(f'leistungen/{l["slug"]}.html', l["seo_title"], l["seo_desc"], body, depth=1,
         extra_head=f'<script type="application/ld+json">{faq_ld}</script>')

def startseite():
    tiles = "".join(
        f'<a class="tile{" tile-urgent" if l.get("notfall") else ""}" href="leistungen/{l["slug"]}.html">'
        f'<span class="ico" aria-hidden="true">{l["icon"]}</span><h2>{e(l["titel"])}</h2><p>{e(l["kurz"])}</p></a>'
        for l in LEISTUNGEN)
    ld = {
        "@context": "https://schema.org", "@type": "Locksmith", "name": FIRMA["name"], "url": FIRMA["website"],
        "address": {"@type": "PostalAddress", "addressLocality": FIRMA["ort"], "postalCode": FIRMA["plz"],
                    "addressRegion": "Rheinland-Pfalz", "addressCountry": "DE"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": FIRMA["oeffnungszeiten"]["von"], "closes": FIRMA["oeffnungszeiten"]["bis"]}],
        "areaServed": FIRMA["einzugsgebiet"], "sameAs": [FIRMA["instagram"]],
    }
    if FIRMA.get("telefon"): ld["telephone"] = FIRMA["telefon"]
    if FIRMA.get("strasse"): ld["address"]["streetAddress"] = FIRMA["strasse"]
    body = f"""
<section class="hero">
  <p class="eyebrow">Im Globus Gensingen · {e(FIRMA["oeffnungszeiten"]["kurz"])}</p>
  <h1>Schlüssel, Schuhe, Gravuren. <br><span>Sofort erledigt.</span></h1>
  <p class="lead">Ihr Fachgeschäft für Schlüsseldienst, Schuhreparatur und Lasergravur – für Gensingen, Bad Kreuznach, Bingen, Alzey und Umgebung.</p>
</section>
<section id="leistungen" class="tiles" aria-label="Leistungen">{tiles}</section>
<section class="band" id="firmen">
  <div><h2>Für Firmen, Vereine & Hausverwaltungen</h2>
  <p>Schließanlagen, Firmenstempel, Türschilder und Pokale – mit festem Ansprechpartner und Rechnung.</p></div>
  {mail_link("btn", "Firmenangebot anfragen")}
</section>
{kontakt_block()}"""
    page("index.html", "Schlüsseldienst & Schuhreparatur Gensingen | Service-Punkt Yakut",
         "Schlüssel nachmachen, Türöffnung 24/7, Schuhreparatur, Lasergravur, Firmenstempel und Pokale – Service-Punkt Yakut im Globus Gensingen.",
         body, extra_head=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')

def impressum_entwurf():
    """ENTWURF – noindex, wird nicht als impressum.html veröffentlicht, bis alle Felder bestätigt sind."""
    def feld(key, label):
        v = val(key, label)
        return e(v) if v else f'<mark class="missing">[{e(label)} fehlt]</mark>'
    # kammer: false = laut Inhaber keine Kammer-Eintragung -> Abschnitt entfällt
    kammer_abschnitt = "" if FIRMA.get("kammer") is False else (
        f'<h2>Handwerksrolle / Kammer</h2><p>{feld("kammer", "Zuständige Handwerkskammer bzw. IHK und ggf. Eintragung")}</p>')
    body = f"""
<section class="legal">
  <p class="draft-banner">ENTWURF – nicht veröffentlichen. Fehlende Angaben sind markiert. Vor Veröffentlichung rechtlich prüfen lassen (z. B. über einen Rechtstexte-Dienst).</p>
  <h1>Impressum</h1>
  <h2>Angaben gemäß § 5 DDG</h2>
  <p>{e(FIRMA["name"])}<br>
     Inhaber: {feld("inhaber", "Vor- und Nachname des Inhabers")}<br>
     {feld("strasse", "Straße & Hausnummer")}<br>
     {e(FIRMA["plz"])} {e(FIRMA["ort"])}<br>
     ({e(FIRMA["standort"])}, {e(FIRMA["standort_detail"])})</p>
  <h2>Kontakt</h2>
  <p>Telefon: {feld("telefon", "Telefon")}<br>E-Mail: {feld("email", "E-Mail")}</p>
  <h2>Umsatzsteuer</h2>
  <p>Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG: {feld("ust_id", "USt-IdNr. (falls vorhanden – sonst Zeile entfernen; bei Kleinunternehmer klären)")}</p>
  {kammer_abschnitt}
  <h2>Verbraucherstreitbeilegung</h2>
  <p>{feld("streitbeilegung", "Erklärung nach § 36 VSBG – Formulierung mit Rechtstexte-Dienst abstimmen")}</p>
</section>"""
    # Bewusst AUSSERHALB von public/: wird nie mit veröffentlicht.
    page("../entwurf/impressum.html", "Impressum (ENTWURF) | Service-Punkt Yakut", "Entwurf", body, depth=1, noindex=True)

def shop_platzhalter():
    """Bis der Shopify-Shop steht: ehrliche Hinweisseite statt totem Link."""
    body = f"""
<section class="page-hero">
  <span class="ico" aria-hidden="true">🛍️</span>
  <h1>Onlineshop in Vorbereitung</h1>
  <p class="lead">Bald bestellen Sie Firmenstempel, Gravurschilder, Schlüsselanhänger, Pokale und personalisierte Geschenke deutschlandweit online – mit eigenem Text und Logo.</p>
  <p class="lead">Bis dahin beraten wir Sie gern persönlich im Globus Gensingen.</p>
  <div class="actions center"><a class="btn" href="../leistungen/stempel.html">Stempel & Schilder</a><a class="btn btn-ghost" href="../leistungen/gravur.html">Lasergravur</a></div>
</section>
{kontakt_block()}"""
    page("shop/index.html", "Onlineshop – bald verfügbar | Service-Punkt Yakut",
         "Personalisierte Stempel, Schilder, Gravuren und Pokale – der Onlineshop von Service-Punkt Yakut ist in Vorbereitung.",
         body, depth=1, noindex=True)

HEADERS = """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
/assets/*
  Cache-Control: public, max-age=86400
"""

def statische_dateien():
    import shutil
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "assets" / "styles.css", OUT / "assets" / "styles.css")
    (OUT / "_headers").write_text(HEADERS, encoding="utf-8")
    (OUT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: " + FIRMA["website"].rstrip("/") + "/sitemap.xml\n",
        encoding="utf-8")
    seiten = ["", *[f"leistungen/{l['slug']}.html" for l in LEISTUNGEN]]
    base = FIRMA["website"].rstrip("/") + "/"
    urls = "".join(f"<url><loc>{e(base + s)}</loc></url>" for s in seiten)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',
        encoding="utf-8")

if __name__ == "__main__":
    statische_dateien()
    startseite()
    for l in LEISTUNGEN:
        leistung_seite(l)
    impressum_entwurf()
    shop_platzhalter()
    print(f"OK: index.html, {len(LEISTUNGEN)} Leistungsseiten, entwurf/impressum.html (nicht veröffentlicht)")
    if WARN:
        print("FEHLENDE ANGABEN (in data/firma.json eintragen):", ", ".join(sorted(WARN)))
