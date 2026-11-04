#!/usr/bin/env python3
"""Erzeugt die komplette Website in public/ aus data/firma.json und data/leistungen.json.

Aufruf:  python3 tools/build.py

Regeln:
- Fehlende Angaben (null in firma.json) werden NIE erfunden, sondern als „folgt“ angezeigt
  und am Ende als Warnung gelistet.
- Rechtstexte (Impressum, Datenschutz) entstehen als Entwurf in entwurf/ – also AUSSERHALB
  von public/. Sie werden erst veröffentlicht, wenn firma.json "rechtstexte_freigegeben": true
  enthält UND keine Pflichtangabe mehr fehlt.
- Keine externen Skripte, Schriften oder Tracker: nichts, was Daten an Dritte sendet.
- Fotos: liegt assets/img/<slug>.jpg vor, wird es statt der Illustration gezeigt.
"""
import html
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "public"
ENTWURF = ROOT / "entwurf"
FIRMA = json.loads((ROOT / "data" / "firma.json").read_text(encoding="utf-8"))
LEISTUNGEN = json.loads((ROOT / "data" / "leistungen.json").read_text(encoding="utf-8"))["leistungen"]
WARN = set()

def e(s):
    return html.escape(str(s), quote=True)

def val(key, label):
    v = FIRMA.get(key)
    if not v:
        WARN.add(label)
    return v

# ------------------------------------------------------------------ Icons (eigene SVGs, kein Fremdinhalt)
ICONS = {
    "door":   '<path d="M6 21V4.5A1.5 1.5 0 0 1 7.5 3h9A1.5 1.5 0 0 1 18 4.5V21"/><path d="M3 21h18"/><circle cx="15" cy="12.5" r=".9" fill="currentColor"/>',
    "key":    '<circle cx="7.5" cy="15.5" r="4"/><path d="M10.4 12.6 20 3"/><path d="M16.5 6.5l3 3"/><path d="M14 9l2 2"/>',
    "shield": '<path d="M12 3l7.5 3v5.2c0 4.6-3.1 8.5-7.5 9.8-4.4-1.3-7.5-5.2-7.5-9.8V6z"/><circle cx="12" cy="10.5" r="1.8"/><path d="M12 12.3V15"/>',
    "shoe":   '<path d="M2.5 17.5V9.5l3.5-1 2 2.2c2.4 2 5 2.6 7.6 2.9l3.4.5c1.6.3 2.5 1.5 2.5 3v.4z"/><path d="M2.5 17.5V20h19v-2.5"/><path d="M9 12.4l1.2-1.6M11.6 13.4l1-1.6"/>',
    "laser":  '<path d="M12 2.5v5M12 16.5v5M2.5 12h5M16.5 12h5"/><path d="M5.3 5.3l2.8 2.8M15.9 15.9l2.8 2.8M5.3 18.7l2.8-2.8M15.9 8.1l2.8-2.8"/><circle cx="12" cy="12" r="1.6"/>',
    "stamp":  '<path d="M9.5 3h5v4.5l-1 3.5h-3l-1-3.5z"/><path d="M5 11h14v4H5z"/><path d="M4 18.5h16"/><path d="M7 21h10"/>',
    "trophy": '<path d="M8 3.5h8v5.5a4 4 0 0 1-8 0z"/><path d="M16 5h3v1.5a3 3 0 0 1-3 3"/><path d="M8 5H5v1.5a3 3 0 0 0 3 3"/><path d="M12 13v3.5"/><path d="M8.5 16.5h7V21h-7z"/>',
    "phone":  '<path d="M5 3.5h3.5l1.8 4.5-2.3 1.4a11 11 0 0 0 6.6 6.6l1.4-2.3 4.5 1.8V19a1.5 1.5 0 0 1-1.6 1.5C10.6 20 4 13.4 3.5 5.1A1.5 1.5 0 0 1 5 3.5z"/>',
    "pin":    '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
    "clock":  '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "cart":   '<path d="M3 4h2.5l2.2 11h10.6l2-8H6.6"/><circle cx="9.5" cy="19" r="1.3"/><circle cx="17" cy="19" r="1.3"/>',
    "building": '<path d="M4 21V5.5L12 3v18"/><path d="M12 9h8v12"/><path d="M2.5 21h19"/><path d="M7 8h2M7 12h2M7 16h2M15 13h2M15 17h2"/>',
    "menu":   '<path d="M4 8h16M4 16h16"/>',
}

def icon(name, cls="i"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')

# ------------------------------------------------------------------ Bausteine
def tel_href():
    nr = val("telefon", "Telefon")
    return f'tel:{nr.replace(" ", "")}' if nr else None

def notdienst_href():
    nr = val("notdienst", "Notdienstnummer")
    return f'tel:{nr.replace(" ", "")}' if nr else None

def link(href, text, cls="link"):
    if not href:
        return f'<span class="{cls} is-missing">{e(text)} – folgt</span>'
    return f'<a class="{cls}" href="{e(href)}">{e(text)}</a>'

def maps_href():
    q = f'{FIRMA["name_kurz"]} Globus {FIRMA.get("strasse") or ""} {FIRMA["plz"]} {FIRMA["ort"]}'
    return "https://www.google.com/maps/search/?api=1&query=" + "+".join(q.split())

def foto_oder_bild(l, cls="art"):
    """Echtes Foto, falls vorhanden – sonst Illustration (Icon mit Lichtschein)."""
    foto = ROOT / "assets" / "img" / f'{l["slug"]}.jpg'
    if foto.exists():
        return f'<img class="{cls} photo" src="/assets/img/{l["slug"]}.jpg" alt="{e(l["titel"])} bei Service-Punkt Yakut" loading="lazy" decoding="async">'
    return f'<div class="{cls} glow t-{l["thema"]}">{icon(l["icon"], "art-icon")}</div>'

def page(path, title, desc, body, noindex=False, extra_head="", ziel=None):
    robots = '<meta name="robots" content="noindex,nofollow">\n' if noindex else ""
    url = FIRMA["website"].rstrip("/") + "/" + path.replace("index.html", "")
    canonical = "" if noindex else f'<link rel="canonical" href="{e(url)}">\n'
    nd = notdienst_href()
    leiste = (f'<a class="ribbon" href="{e(nd)}">Ausgesperrt? Türöffnung 24/7 – jetzt anrufen ›</a>' if nd
              else '<p class="ribbon">Türöffnungs-Notdienst 24/7</p>')
    nav_links = "".join(f'<a href="/leistungen/{l["slug"]}.html">{e(l["titel"])}</a>' for l in LEISTUNGEN)
    tel = tel_href()
    call = f'<a class="nav-call" href="{e(tel)}">{icon("phone")}<span>Anrufen</span></a>' if tel else ""
    fuss_leistungen = "".join(f'<li><a href="/leistungen/{l["slug"]}.html">{e(l["titel"])}</a></li>' for l in LEISTUNGEN)
    rechtliches = ('<li><a href="/impressum.html">Impressum</a></li><li><a href="/datenschutz.html">Datenschutz</a></li>'
                   if rechtstexte_live() else '<li><span class="muted">Impressum & Datenschutz in Vorbereitung</span></li>')
    doc = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{canonical}{robots}<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta name="theme-color" content="#000000">
<meta name="color-scheme" content="dark">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/styles.css">
<script src="/assets/site.js" defer></script>
{extra_head}
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<header class="gnav">
  <div class="gnav-in">
    <a href="/" class="brand" aria-label="Service-Punkt Yakut – Startseite"><span class="brand-mark">{icon("key")}</span>Service‑Punkt Yakut</a>
    <nav class="gnav-links" aria-label="Hauptnavigation">
      <a href="/#leistungen">Leistungen</a>
      <a href="/#firmen">Firmenkunden</a>
      <a href="/shop/">Shop</a>
      <a href="/#besuch">Besuch</a>
    </nav>
    {call}
    <details class="gnav-menu">
      <summary aria-label="Menü öffnen">{icon("menu")}</summary>
      <div class="gnav-sheet">
        <p class="sheet-label">Leistungen</p>{nav_links}
        <p class="sheet-label">Mehr</p><a href="/#firmen">Firmenkunden</a><a href="/shop/">Shop</a><a href="/#besuch">Besuch & Kontakt</a>
      </div>
    </details>
  </div>
</header>
{leiste}
<main id="inhalt">
{body}
</main>
<footer class="foot">
  <div class="foot-in">
    <div class="foot-cols">
      <div><h3>Leistungen</h3><ul>{fuss_leistungen}</ul></div>
      <div><h3>Besuch</h3><ul>
        <li>{e(FIRMA["name_kurz"])}</li><li>{e(FIRMA["standort"])}</li><li>{e(FIRMA.get("strasse") or "")}</li><li>{e(FIRMA["plz"])} {e(FIRMA["ort"])}</li>
        <li>{e(FIRMA["oeffnungszeiten"]["kurz"])} · Notdienst 24/7</li></ul></div>
      <div><h3>Kontakt</h3><ul>
        <li>{link(tel, FIRMA.get("telefon") or "Telefon", "")}</li>
        <li>{link("mailto:" + FIRMA["email"] if FIRMA.get("email") else None, FIRMA.get("email") or "E-Mail", "")}</li>
        <li><a href="{e(FIRMA["instagram"])}" rel="noopener">Instagram</a></li>
        <li><a href="{e(FIRMA["whatsapp_kanal"])}" rel="noopener">WhatsApp-Kanal</a></li></ul></div>
      <div><h3>Rechtliches</h3><ul>{rechtliches}</ul></div>
    </div>
    <p class="fine">Einsatzgebiet: {" · ".join(e(o) for o in FIRMA["einzugsgebiet"])}</p>
    <p class="fine">© {e(FIRMA["name"])}</p>
  </div>
</footer>
</body>
</html>
"""
    out = (ziel or OUT) / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")

def besuch_block():
    oz = FIRMA["oeffnungszeiten"]
    tel = tel_href()
    mail = f'mailto:{FIRMA["email"]}' if FIRMA.get("email") else None
    return f"""
<section class="visit reveal" id="besuch">
  <h2 class="section-title">Besuchen Sie uns.</h2>
  <p class="section-sub">Mitten im Globus Gensingen – erledigen Sie Ihren Einkauf, wir erledigen den Rest.</p>
  <div class="visit-grid">
    <div class="visit-card">{icon("pin")}<h3>Standort</h3>
      <p>{e(FIRMA["standort"][:1].upper() + FIRMA["standort"][1:])}<br>{e(FIRMA["standort_detail"])}<br>{e(FIRMA.get("strasse") or "")}<br>{e(FIRMA["plz"])} {e(FIRMA["ort"])}</p>
      <a class="link" href="{e(maps_href())}" rel="noopener">Route planen ›</a></div>
    <div class="visit-card">{icon("clock")}<h3>Öffnungszeiten</h3>
      <p>{e(oz["text"])}<br><strong>Schlüssel-Notdienst: 24/7</strong></p></div>
    <div class="visit-card">{icon("phone")}<h3>Kontakt</h3>
      <p>{e(FIRMA.get("telefon") or "Telefon folgt")}<br>{e(FIRMA.get("email") or "")}</p>
      {link(tel, "Anrufen ›")} {link(mail, "E-Mail schreiben ›")}</div>
  </div>
</section>"""

# ------------------------------------------------------------------ Startseite
def startseite():
    by = {l["slug"]: l for l in LEISTUNGEN}
    chips = "".join(
        f'<a class="chip" href="/leistungen/{l["slug"]}.html">{icon(l["icon"], "chip-icon t-" + l["thema"])}<span>{e(l["titel"])}</span></a>'
        for l in LEISTUNGEN)

    def panel(l, gross=True):
        nd = notdienst_href() if l.get("notfall") else tel_href()
        cta = link(nd, "Jetzt anrufen ›" if l.get("notfall") else "Anrufen ›")
        return f"""
<article class="panel {'panel-xl' if gross else 'panel-half'} reveal">
  <div class="panel-copy">
    <p class="panel-kicker">{e(l["titel"])}</p>
    <h2>{e(l["panel_titel"])}</h2>
    <p class="panel-text">{e(l["panel_text"])}</p>
    <p class="panel-links"><a class="link" href="/leistungen/{l["slug"]}.html">Mehr erfahren ›</a>{cta}</p>
  </div>
  {foto_oder_bild(l)}
</article>"""

    ld = {
        "@context": "https://schema.org", "@type": "Locksmith", "name": FIRMA["name"], "url": FIRMA["website"],
        "address": {"@type": "PostalAddress", "addressLocality": FIRMA["ort"], "postalCode": FIRMA["plz"],
                    "addressRegion": "Rheinland-Pfalz", "addressCountry": "DE"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": FIRMA["oeffnungszeiten"]["von"], "closes": FIRMA["oeffnungszeiten"]["bis"]}],
        "areaServed": FIRMA["einzugsgebiet"], "sameAs": [FIRMA["instagram"]],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": l["titel"]}} for l in LEISTUNGEN],
    }
    if FIRMA.get("telefon"): ld["telephone"] = FIRMA["telefon"]
    if FIRMA.get("email"): ld["email"] = FIRMA["email"]
    if FIRMA.get("strasse"): ld["address"]["streetAddress"] = FIRMA["strasse"]

    tel = tel_href()
    body = f"""
<section class="hero">
  <p class="hero-kicker">Service‑Punkt Yakut · Globus Gensingen</p>
  <h1>Schlüssel. Schuhe.<br><span class="grad">Gravur.</span></h1>
  <p class="hero-sub">Alles an einem Ort. Gemacht mit Präzision – mitten im Globus Gensingen.</p>
  <p class="hero-ctas"><a class="btn" href="#leistungen">Leistungen ansehen</a>{link(tel, "Anrufen", "btn btn-ghost")}</p>
</section>

<nav class="chips" id="leistungen" aria-label="Alle Leistungen">{chips}</nav>

{panel(by["tueroeffnung"])}
{panel(by["schluessel"])}
<div class="duo">{panel(by["schuhreparatur"], False)}{panel(by["gravur"], False)}</div>
<div class="duo">{panel(by["stempel"], False)}{panel(by["pokale"], False)}</div>
{panel(by["schliessanlagen"])}

<section class="values reveal">
  <h2 class="section-title">Warum Service‑Punkt Yakut.</h2>
  <div class="values-grid">
    <div><p class="v-big">24/7</p><p>Schlüssel-Notdienst, Tag und Nacht.</p></div>
    <div><p class="v-big">7</p><p>Leistungen unter einem Dach – vom Schlüssel bis zum Pokal.</p></div>
    <div><p class="v-big">Mo–Sa</p><p>09–18 Uhr im Globus Gensingen. Ohne Termin.</p></div>
  </div>
</section>

<section class="b2b reveal" id="firmen">
  <div class="b2b-copy">
    {icon("building", "b2b-icon")}
    <h2>Für Firmen, Vereine<br>und Hausverwaltungen.</h2>
    <p>Schließanlagen, Firmenstempel, Türschilder, Pokale und Werbeartikel mit Logo – mit festem Ansprechpartner und auf Rechnung.</p>
    <p class="panel-links">{link("mailto:" + FIRMA["email"] + "?subject=Firmenanfrage" if FIRMA.get("email") else None, "Angebot anfordern ›")}{link(tel, "Anrufen ›")}</p>
  </div>
</section>

<section class="shop-teaser reveal">
  {icon("cart", "shop-icon")}
  <h2>Bald auch online.</h2>
  <p>Firmenstempel, Gravurschilder und personalisierte Geschenke – deutschlandweit bestellen.</p>
  <a class="link" href="/shop/">Mehr erfahren ›</a>
</section>

{besuch_block()}"""
    page("index.html", "Schlüsseldienst, Schuhreparatur & Gravur in Gensingen | Service-Punkt Yakut",
         "Schlüssel nachmachen, Türöffnung 24/7, Schuhreparatur, Lasergravur, Firmenstempel und Pokale – Service-Punkt Yakut im Globus Gensingen. Für Bad Kreuznach, Bingen, Alzey und Umgebung.",
         body, extra_head=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')

# ------------------------------------------------------------------ Leistungsseiten
def leistung_seite(l):
    punkte = "".join(f'<div class="card reveal"><h3>{e(p["titel"])}</h3><p>{e(p["text"])}</p></div>' for p in l["punkte"])
    faq = "".join(f'<details class="faq-item"><summary>{e(f["frage"])}</summary><p>{e(f["antwort"])}</p></details>' for f in l["faq"])
    nd = notdienst_href() if l.get("notfall") else tel_href()
    andere = "".join(
        f'<a class="chip" href="/leistungen/{x["slug"]}.html">{icon(x["icon"], "chip-icon t-" + x["thema"])}<span>{e(x["titel"])}</span></a>'
        for x in LEISTUNGEN if x is not l)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f["frage"], "acceptedAnswer": {"@type": "Answer", "text": f["antwort"]}} for f in l["faq"]]},
        ensure_ascii=False)
    crumbs = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Start", "item": FIRMA["website"]},
        {"@type": "ListItem", "position": 2, "name": l["titel"], "item": FIRMA["website"].rstrip("/") + f'/leistungen/{l["slug"]}.html'}]},
        ensure_ascii=False)
    body = f"""
<section class="sub-hero">
  <nav class="crumbs" aria-label="Brotkrumen"><a href="/">Start</a> › {e(l["titel"])}</nav>
  {foto_oder_bild(l, "sub-art")}
  <p class="hero-kicker">{e(l["titel"])}</p>
  <h1>{e(l["h1"])}</h1>
  <p class="hero-sub">{e(l["lead"])}</p>
  <p class="hero-ctas">{link(nd, "Notdienst anrufen" if l.get("notfall") else "Anrufen", "btn btn-urgent" if l.get("notfall") else "btn")}<a class="btn btn-ghost" href="/#besuch">Anfahrt & Zeiten</a></p>
</section>
<section class="cards">{punkte}</section>
<section class="faq reveal"><h2 class="section-title">Häufige Fragen.</h2>{faq}</section>
<section class="more reveal"><h2 class="section-title">Weitere Leistungen.</h2><nav class="chips chips-left">{andere}</nav></section>
{besuch_block()}"""
    page(f'leistungen/{l["slug"]}.html', l["seo_title"], l["seo_desc"], body,
         extra_head=f'<script type="application/ld+json">{faq_ld}</script>\n<script type="application/ld+json">{crumbs}</script>')

def shop_platzhalter():
    body = f"""
<section class="sub-hero">
  <div class="sub-art glow t-gold">{icon("cart", "art-icon")}</div>
  <p class="hero-kicker">Onlineshop</p>
  <h1>Bald auch online.</h1>
  <p class="hero-sub">Firmenstempel, Gravurschilder, Schlüsselanhänger, Pokale und personalisierte Geschenke – mit Ihrem Text und Logo, deutschlandweit geliefert.</p>
  <p class="hero-sub">Bis dahin beraten wir Sie gern persönlich im Globus Gensingen.</p>
  <p class="hero-ctas"><a class="btn" href="/leistungen/stempel.html">Stempel & Schilder</a><a class="btn btn-ghost" href="/leistungen/gravur.html">Lasergravur</a></p>
</section>
{besuch_block()}"""
    page("shop/index.html", "Onlineshop – bald verfügbar | Service-Punkt Yakut",
         "Personalisierte Stempel, Schilder, Gravuren und Pokale – der Onlineshop von Service-Punkt Yakut ist in Vorbereitung.",
         body, noindex=True)

def nicht_gefunden():
    body = """
<section class="sub-hero">
  <p class="hero-kicker">Fehler 404</p>
  <h1>Diese Seite gibt es nicht.</h1>
  <p class="hero-sub">Vielleicht finden Sie hier, was Sie suchen:</p>
  <p class="hero-ctas"><a class="btn" href="/">Zur Startseite</a><a class="btn btn-ghost" href="/#leistungen">Alle Leistungen</a></p>
</section>"""
    page("404.html", "Seite nicht gefunden | Service-Punkt Yakut", "Seite nicht gefunden.", body, noindex=True)

# ------------------------------------------------------------------ Rechtstexte (Entwurf)
def feld(key, label):
    v = val(key, label)
    return e(v) if v else f'<mark class="missing">[{e(label)} fehlt]</mark>'

def rechtstexte_vollstaendig():
    return all(FIRMA.get(k) for k in ("inhaber", "strasse", "telefon", "email")) and (
        FIRMA.get("ust_id") or FIRMA.get("ust_id") is False)

def rechtstexte_live():
    return FIRMA.get("rechtstexte_freigegeben") is True and rechtstexte_vollstaendig()

BANNER = ('<p class="draft-banner">ENTWURF – nicht veröffentlicht. Vor dem Livegang vom Inhaber bestätigen und '
          'rechtlich prüfen lassen (z. B. Rechtstexte-Dienst). Fehlende Angaben sind rot markiert.</p>')

def impressum(live):
    ust = "" if FIRMA.get("ust_id") is False else (
        f'<h2>Umsatzsteuer</h2><p>Umsatzsteuer-Identifikationsnummer gemäß § 27a Umsatzsteuergesetz:<br>{feld("ust_id", "USt-IdNr.")}</p>')
    kammer = "" if FIRMA.get("kammer") is False else (
        f'<h2>Kammer</h2><p>{feld("kammer", "Zuständige Kammer und Eintragung")}</p>')
    body = f"""
<section class="legal">
  {"" if live else BANNER}
  <h1>Impressum</h1>
  <h2>Angaben gemäß § 5 DDG</h2>
  <p>{e(FIRMA["name"])}<br>Inhaber: {feld("inhaber", "Inhaber")}<br>{feld("strasse", "Straße & Hausnummer")}<br>{e(FIRMA["plz"])} {e(FIRMA["ort"])}</p>
  <h2>Kontakt</h2>
  <p>Telefon: {feld("telefon", "Telefon")}<br>E-Mail: {feld("email", "E-Mail")}</p>
  {ust}{kammer}
  <h2>Verbraucherstreitbeilegung</h2>
  <p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
</section>"""
    if live:
        page("impressum.html", "Impressum | Service-Punkt Yakut", "Impressum von Service-Punkt Yakut.", body, noindex=True)
    else:
        page("impressum.html", "Impressum (ENTWURF) | Service-Punkt Yakut", "Entwurf", body, noindex=True, ziel=ENTWURF)

def datenschutz(live):
    body = f"""
<section class="legal">
  {"" if live else BANNER}
  <h1>Datenschutzerklärung</h1>
  <h2>1. Verantwortlicher</h2>
  <p>{e(FIRMA["name"])}, Inhaber {feld("inhaber", "Inhaber")}, {feld("strasse", "Straße & Hausnummer")}, {e(FIRMA["plz"])} {e(FIRMA["ort"])}<br>
     Telefon: {feld("telefon", "Telefon")} · E-Mail: {feld("email", "E-Mail")}</p>
  <h2>2. Keine Cookies, kein Tracking</h2>
  <p>Diese Website verwendet keine Cookies, keine Analyse- oder Werbedienste und lädt keine Schriften, Karten oder Videos von Drittanbietern.</p>
  <h2>3. Hosting und Server-Logdateien</h2>
  <p>Die Website wird bei Cloudflare, Inc., 101 Townsend St., San Francisco, CA 94107, USA, gehostet. Beim Aufruf verarbeitet der Hoster technisch notwendige Daten (u. a. IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Browsertyp), um die Website sicher und stabil auszuliefern. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einem sicheren Betrieb). Eine Übermittlung in die USA erfolgt auf Grundlage des EU-US Data Privacy Framework bzw. von Standardvertragsklauseln.
  <mark class="missing">[Vor Livegang prüfen: Auftragsverarbeitungsvertrag mit Cloudflare abschließen, Zertifizierung prüfen]</mark></p>
  <h2>4. Kontakt per Telefon, E-Mail oder WhatsApp</h2>
  <p>Wenn Sie uns kontaktieren, verarbeiten wir Ihre Angaben zur Bearbeitung Ihrer Anfrage (Art. 6 Abs. 1 lit. b DSGVO bei vertragsbezogenen Anfragen, sonst lit. f). Die Daten werden gelöscht, sobald sie nicht mehr benötigt werden und keine gesetzlichen Aufbewahrungspflichten bestehen.</p>
  <h2>5. Links zu Instagram, WhatsApp und Google Maps</h2>
  <p>Wir verlinken auf unsere Profile bei Instagram und WhatsApp (Meta Platforms Ireland Ltd.) sowie auf Google Maps (Google Ireland Ltd.). Es handelt sich um einfache Links: Erst wenn Sie einen Link anklicken, werden Daten an den jeweiligen Anbieter übertragen. Es gelten dann dessen Datenschutzbestimmungen.</p>
  <h2>6. Ihre Rechte</h2>
  <p>Sie haben das Recht auf Auskunft (Art. 15), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch (Art. 21 DSGVO). Sie können sich außerdem bei einer Aufsichtsbehörde beschweren, z. B. beim Landesbeauftragten für den Datenschutz und die Informationsfreiheit Rheinland-Pfalz.</p>
  <p class="muted">Stand: {e(FIRMA.get("rechtstexte_stand") or "Entwurf")}</p>
</section>"""
    if live:
        page("datenschutz.html", "Datenschutz | Service-Punkt Yakut", "Datenschutzerklärung von Service-Punkt Yakut.", body, noindex=True)
    else:
        page("datenschutz.html", "Datenschutz (ENTWURF) | Service-Punkt Yakut", "Entwurf", body, noindex=True, ziel=ENTWURF)

# ------------------------------------------------------------------ Statische Dateien
HEADERS = """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'
/assets/*
  Cache-Control: public, max-age=604800
"""

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#000"/>'
           '<g fill="none" stroke="#e8c37a" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="20" r="5"/>'
           '<path d="M14.6 16.4 26 5M22 9l3 3M19 12l2 2"/></g></svg>')

def statische_dateien():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for f in ("styles.css", "site.js"):
        shutil.copy2(ROOT / "assets" / f, OUT / "assets" / f)
    if (ROOT / "assets" / "img").exists():
        shutil.copytree(ROOT / "assets" / "img", OUT / "assets" / "img")
    (OUT / "assets" / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    # JSON-LD-Blöcke werden nicht ausgeführt und fallen nicht unter script-src.
    (OUT / "_headers").write_text(HEADERS, encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f'User-agent: *\nAllow: /\nSitemap: {FIRMA["website"].rstrip("/")}/sitemap.xml\n', encoding="utf-8")
    base = FIRMA["website"].rstrip("/") + "/"
    seiten = ["", *[f"leistungen/{l['slug']}.html" for l in LEISTUNGEN]]
    urls = "".join(f"<url><loc>{e(base + s)}</loc></url>" for s in seiten)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',
        encoding="utf-8")

if __name__ == "__main__":
    statische_dateien()
    startseite()
    for l in LEISTUNGEN:
        leistung_seite(l)
    shop_platzhalter()
    nicht_gefunden()
    live = rechtstexte_live()
    if ENTWURF.exists():
        shutil.rmtree(ENTWURF)
    impressum(live)
    datenschutz(live)
    if ENTWURF.exists():
        shutil.copytree(OUT / "assets", ENTWURF / "assets")
    print(f"OK: Startseite, {len(LEISTUNGEN)} Leistungsseiten, Shop-Hinweis, 404")
    print("Rechtstexte:", "VERÖFFENTLICHT in public/" if live else "nur Entwurf in entwurf/ (nicht veröffentlicht)")
    if WARN:
        print("FEHLENDE ANGABEN (in data/firma.json eintragen):", ", ".join(sorted(WARN)))
