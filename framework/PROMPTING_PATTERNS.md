# Prompting Patterns — Catalogus

## Overzicht

Dit document catalogiseert de prompting patronen die iCt Horse gebruikt. Elk patroon is geen theorie — het is geëxtraheerd uit daadwerkelijk gebruik in 50+ repositories.

## Patroon 1: WhatIf Protocol (Pre-Action Validation)

**Wat:** Voordat de AI iets bouwt, moet het eerst:
1. Begrip terugkoppelen (functioneel + technisch)
2. Plan voorleggen (wat ga ik doen?)
3. Impactanalyse (wat verandert er, wat kan breken?)
4. Expliciet akkoord vragen

**Waarom effectief:** Voorkomt dat de AI direct begint te bouwen op basis van een verkeerde interpretatie. De kosten van 30 seconden validatie zijn verwaarloosbaar vergeleken met minuten/uren herwerk.

**Bewijs:** Aanwezig in `CLAUDE.md` van Meta_Master en alle actieve projecten. Afgedwongen als VERPLICHT protocol.

**Analogie:** `-WhatIf` parameter in PowerShell — simuleer vóór je uitvoert.

---

## Patroon 2: Kleurgecodeerde Severity

**Wat:** Elke wijziging krijgt een kleur die de impact bepaalt:
- **Groen:** Minor, code only, geen architectuurimpact → +0.0.1
- **Oranje:** Design impact, logische architectuur stabiel → +0.1.0
- **Rood:** Major, redesign nodig → +1.0.0

**Bugfixes:**
- **Groen:** Snel herstel (fysiek niveau)
- **Geel:** Out-of-physical-box (logische architectuur)
- **Rood:** Out-of-the-box (conceptueel redesign)
- **Loop:** Debug-loop — compleet nieuwe invalshoek nodig

**Waarom effectief:** De AI en de mens spreken dezelfde taal over impact. Geen discussie over "is dit een major of minor change" — het kleurensysteem definieert het.

**Bewijs:** Actief in PhotoVerify, RandomRingtone, BanenzwemmenWidget ecosystemen.

---

## Patroon 3: Root Cause Analysis (3 Niveaus)

**Wat:** Bij elke bugfix MOET de AI de oorzaak benoemen op drie niveaus:
1. **Functioneel** — wat ging er mis voor de gebruiker?
2. **Technisch** — welke code/configuratie is de oorzaak?
3. **Architectonisch** — welk ontwerpbesluit maakte dit mogelijk?

**Waarom effectief:** Voorkomt "pleisters plakken". De AI wordt gedwongen om dieper te kijken dan het symptoom. Het architectonische niveau voorkomt dat dezelfde categorie bug opnieuw optreedt.

**Bewijs:** Verplicht in alle project CLAUDE.md bestanden via Meta_Master protocol.

---

## Patroon 4: Constraint via CLAUDE.md

**Wat:** Elk project heeft een `CLAUDE.md` bestand dat de AI instrueert over:
- Projectcontext en doel
- Verplichte protocols
- Verboden acties (zsh safety, destructieve git operaties)
- Build en deploy procedures
- Versioning regels

**Waarom effectief:** De AI leest CLAUDE.md bij het starten van elke sessie. Het is een persistent, versioneerbaar, reviewbaar instructiebestand — niet een vluchtige prompt die verloren gaat.

**Bewijs:** Aanwezig in alle actieve repositories. Globale CLAUDE.md in homedir + per-project CLAUDE.md.

---

## Patroon 5: Feedback Loop (Memory Type: Feedback)

**Wat:** Wanneer de AI iets fout doet en gecorrigeerd wordt, wordt de correctie opgeslagen als een "feedback" memory:
- Wat was fout
- Waarom het fout was
- Hoe het voorkomen moet worden

**Waarom effectief:** De AI maakt dezelfde fout nooit twee keer. Feedback memories worden geladen bij relevante taken en sturen gedrag bij. Dit is het equivalent van een teamlid dat leert van code reviews.

**Bewijs:** 30+ feedback memories in Claude memory systeem, elk met concrete correctie.

---

## Patroon 6: Aliassen en Shortcuts

**Wat:** Veelgebruikte complexe opdrachten worden gereduceerd tot korte triggers:
- `newp <naam>` → volledig nieuw project protocol
- `over en uit` / `OEU` → verplicht einde-sessie protocol
- `DB` → WerkDierenbescherming project

**Waarom effectief:** Reduceert frictie voor veelgebruikte workflows. De AI kent de volledige procedure achter de alias en voert die volledig uit.

**Bewijs:** Vastgelegd in feedback memories en CLAUDE.md.

---

## Patroon 7: Thematische Codenamen

**Wat:** Elke build krijgt een unieke codenaam uit een thema dat per project is gedefinieerd:
- PhotoVerify Android: Family Guy characters
- PhotoVerify Meta: Simpsons facts
- RandomRingtone: Iconische muzikanten
- Enigma: Beroemde codebreakers

**Waarom effectief:** Builds worden herkenbaar en memorabel. "De Freddie Mercury build" is makkelijker te onthouden dan "v1.4.2". Het dwingt ook uniekheid af — geen twee builds met dezelfde naam.

**Bewijs:** Actief in alle projecten met build-output (Android apps, web deploys).

---

## Patroon 8: Multi-Agent Sync Files

**Wat:** Bij sessie-einde schrijft elke agent sync-bestanden voor de andere agenten:
- `meta_master_import.json` (Claude → Gemini/Codex)
- `meta_master_export.json` (Gemini → Claude)

**Waarom effectief:** Agenten hebben geen gedeeld geheugen. Sync files overbruggen dat gap. Elke agent weet wat de andere heeft gedaan en kan daarop voortbouwen.

**Bewijs:** Sync protocol in Meta_Master/CLAUDE.md, fysieke bestanden in `~/.gemini/tmp/claude_sync/` en `~/.codex/tmp/claude_sync/`.

---

## Patroon 9: Expliciete Vastlegging

**Wat:** Alle elementen, componenten en hun relaties worden expliciet beschreven in de repo:
- ARCHITECTURE.md — componenten, relaties, data flow
- DESIGN_TOKENS.md — kleuren, typografie, spacing
- docs/PRINCIPLES.md — conceptuele principes
- docs/DEPENDENCIES.md — afhankelijkheden

**Waarom effectief:** De AI hoeft niet te raden hoe het systeem in elkaar zit. Expliciete documentatie elimineert aannames en maakt het mogelijk om impact van wijzigingen te voorspellen.

**Bewijs:** Verplicht in Meta_Master/CLAUDE.md voor alle projecten.

---

## Patroon 10: Debug Protocol (STOP → Kleur → RCA → WhatIf)

**Wat:** Bij een bug of error:
1. **STOP** — niet meteen fixen
2. **Kleur bepalen** — groen/geel/rood/loop
3. **RCA** — 3 niveaus analyseren
4. **WhatIf** — plan voorleggen vóór de fix
5. **Na 2 mislukte pogingen** → compleet nieuwe invalshoek (Loop)

**Waarom effectief:** Voorkomt dat de AI in een debug-loop terechtkomt van steeds dezelfde aanpak proberen. Het "Loop" escape mechanisme dwingt lateraal denken af na twee mislukkingen.

**Bewijs:** Vastgelegd als feedback memory en in project CLAUDE.md bestanden.
