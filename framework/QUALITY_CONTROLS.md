# Quality Controls — Voorspelbare Kwaliteit

## Principe

Kwaliteit is geen toeval. Het is het resultaat van systematische controles die op elk punt in het proces afdwingen dat de output aan standaarden voldoet.

## De Kwaliteitsketen

```
Vraag/Opdracht
    │
    ▼
┌─────────────┐
│  WhatIf     │ ← Begrip valideren vóór actie
│  Protocol   │
└──────┬──────┘
       │ Akkoord
       ▼
┌─────────────┐
│  Kleur      │ ← Impact inschatten (groen/oranje/rood)
│  Bepalen    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Uitvoering │ ← Code schrijven / wijzigen
│             │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Versioning │ ← Versie-bump VÓÓR commit
│  Mandate    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Build &    │ ← Change detection, WhatIf, verify
│  Test       │
└──────┬──────┘
       │ Bij fout ──► Debug Protocol
       ▼
┌─────────────┐
│  Commit &   │ ← Beschrijvende message, co-authored-by
│  Push       │
└─────────────┘
```

## Versioning Mandate

**Regel:** Elke functionele of technische wijziging → versienummer verhogen VÓÓR build of commit.

| Impact | Versie-bump | Voorbeeld |
|--------|-------------|-----------|
| Groen (minor) | +0.0.1 | Bugfix, kleine UI tweak |
| Oranje (design) | +0.1.0 | Nieuwe feature, layout wijziging |
| Rood (major) | +1.0.0 | Redesign, breaking change |

**Waarom:** Geen twee builds mogen dezelfde versie hebben. Dit maakt elke wijziging traceerbaar en rollback mogelijk.

## Debug Protocol

Bij een bug of error — NIET meteen fixen. Volg het protocol:

### Stap 1: STOP
Pauzeer. Geen impulsieve fix.

### Stap 2: Kleur Bepalen
- **Groen:** Snel herstel, fysiek niveau
- **Geel:** Logische architectuur geraakt
- **Rood:** Conceptueel redesign nodig
- **Loop:** Na 2 mislukte pogingen → compleet nieuwe invalshoek

### Stap 3: Root Cause Analysis (3 niveaus)
1. **Functioneel:** Wat ging er mis voor de gebruiker?
2. **Technisch:** Welke code/configuratie is de oorzaak?
3. **Architectonisch:** Welk ontwerpbesluit maakte dit mogelijk?

### Stap 4: WhatIf
Plan de fix, leg impact uit, vraag akkoord.

### Stap 5: Fix + Verify
Implementeer de fix, verifieer dat het probleem is opgelost.

### Loop Escape
Na 2 mislukte fix-pogingen: **STOP**, neem afstand, probeer een compleet andere invalshoek. Dit voorkomt dat de AI (of de mens) vastloopt in dezelfde denkrichting.

## Build Protocol

1. **Change Detection:** `git status` — zijn er wijzigingen?
2. **WhatIf:** Stap-voor-stap analyse van het build-proces
3. **Akkoord:** Gebruiker bevestigt
4. **Build:** Compileren/bouwen
5. **Verify:** Output controleren
6. **Delivery:** APK → Downloads + Google Drive upload

## Thematische Codenamen

Elke build krijgt een unieke codenaam. Dit is geen gimmick — het dient drie doelen:
1. **Herkenbaarheid:** "De Freddie Mercury build" vs "v1.4.2"
2. **Uniekheid:** Geen twee builds met dezelfde naam
3. **Communicatie:** Makkelijker refereren in gesprekken

| Project | Thema |
|---------|-------|
| PhotoVerify Meta | The Simpsons |
| PhotoVerify Android | Family Guy |
| RandomRingtone | Iconische muzikanten |
| Enigma | Beroemde codebreakers |
| FormTracer | Beroemde detectives |
| ClaudeWeb | Internetpioniers |
| Dashboard | Beroemde ontdekkingsreizigers |
