# Fotos und Videos

- `fotos/quelle/echt/<name>.jpg` → echte Fotos aus dem Laden.
- `fotos/quelle/ki/<name>.png|jpg|mp4` → KI-generierte Symbolbilder und Videos. Sie werden auf der Website als Symbolbild gekennzeichnet und ersetzen das echte Foto gleichen Namens.
- `<name>` = Slug der Leistungsseite (z. B. `gravur`, `stempel`, `schuhreparatur`), `hero` (Startseite) oder `shop`.
- Nach jeder Änderung: `python3 tools/medien.py`, dann `python3 tools/build.py`. Die Dateien in `assets/img/` und `assets/video/` nicht von Hand bearbeiten.
- Prompts für die KI-Bilder: `docs/KI-BILDER-PROMPTS.md`.
- `fotos/wartet-auf-freigabe/` → bearbeitete Fotos, die noch NICHT veröffentlicht werden dürfen (z. B. fremde Marken ohne Erlaubnis).
  - `gravur-parfum.jpg`: Flakons „NOUR by Babrak Music“ (Marke eines Kollegen). Erst nach dessen Erlaubnis nach `fotos/quelle/echt/gravur.jpg` verschieben.
- Keine Fotos mit Namen von Privatpersonen oder Prominenten veröffentlichen.
- Kein Vorher-Nachher per KI. Dafür nur echte Fotos eigener Arbeiten verwenden.
