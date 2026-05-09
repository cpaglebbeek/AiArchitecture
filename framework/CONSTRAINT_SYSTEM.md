# Constraint System — Kadering van AI-gedrag

## Principe

Een AI zonder constraints is als een architect zonder bouwbesluit: het kan alles bouwen, maar niets is gegarandeerd veilig, consistent of onderhoudbaar.

iCt Horse gebruikt een gelaagd constraint systeem dat AI-gedrag kadert op drie niveaus.

## De Drie Lagen

```
┌─────────────────────────────────────┐
│  Laag 1: Globale CLAUDE.md         │  ← Geldt voor ALLES
│  (~/.claude/CLAUDE.md)             │
│  • Meta_Master pad                  │
│  • Sessie-startprotocol             │
│  • Over en uit protocol             │
│  • ZSH safety regels                │
├─────────────────────────────────────┤
│  Laag 2: Ecosysteem CLAUDE.md      │  ← Geldt per ecosysteem
│  (Gemini_Projects/CLAUDE.md)       │
│  • Shared infrastructure awareness  │
│  • Multi-session conflict prevention│
│  • Feature/bugfix kleurcodering     │
│  • Build & testing mandaat          │
├─────────────────────────────────────┤
│  Laag 3: Project CLAUDE.md         │  ← Geldt per project
│  (<project>/CLAUDE.md)             │
│  • Projectspecifieke regels          │
│  • Codenaam-thema                   │
│  • Deploy procedures                │
│  • Versioning mandate               │
└─────────────────────────────────────┘
```

## Constraint Categorieën

### 1. Verboden Acties
Expliciete lijst van dingen die de AI NIET mag doen:
- `path` als variabelenaam gebruiken (zsh safety)
- Force push naar main/master
- Credentials committen
- Bestanden verwijderen zonder akkoord
- Nginx config overschrijven (shared infrastructure)

### 2. Verplichte Protocols
Acties die de AI ALTIJD moet uitvoeren:
- WhatIf vóór elke niet-triviale actie
- Versie-bump bij elke wijziging
- RCA bij elke bugfix
- Memory sync bij sessie-einde
- PROJECTS.json bijwerken bij nieuwe repos

### 3. Conditionele Regels
Regels die alleen gelden in specifieke contexten:
- Hetzner-projecten: lees SHARED_INFRASTRUCTURE.md
- Android builds: kopieer APK naar Downloads + Drive upload
- Private repos: git-crypt unlock vóór bewerking
- Merge freeze periodes: geen non-critical merges

## Feedback als Dynamische Constraints

Het constraint systeem is niet statisch. Feedback memories fungeren als dynamisch toegevoegde regels:

```
Gebruiker: "stop met samenvatten aan het einde van elke response"
    ↓
Feedback memory: "geen trailing summaries"
    ↓
Constraint: bij ELKE response, geen samenvattend blok aan het einde
```

Dit maakt het systeem zelf-lerend: elke correctie wordt een permanente constraint.

## Verschil met "Vibe Coding"

| Aspect | Vibe Coding | Constraint-Driven |
|--------|------------|-------------------|
| Instructie | "Maak een login pagina" | CLAUDE.md: context, regels, protocols |
| Kwaliteitsborging | Hopen dat het werkt | WhatIf + RCA + versioning verplicht |
| Geheugen | Elke sessie opnieuw | Persistent memory + feedback loop |
| Fouten | Herhaald | Eenmalig, dan feedback memory |
| Veiligheid | Ad hoc | git-crypt + infra safety + privacy filters |
| Traceerbaarheid | Geen | Sessiedocumentatie + commit history |
