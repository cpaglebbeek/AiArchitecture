# Multi-Agent Orchestration — Vier AI's, Eén Architectuur

## Overzicht

iCt Horse werkt niet met één AI-agent maar orkestreert vier:

| Agent | Primaire Rol | Sterkte |
|-------|-------------|---------|
| **Claude Code** | Primair: code, architectuur, analyse, memory | Diep begrip, lange context, tool-integratie |
| **Gemini CLI** | Second opinion, alternatieve aanpak | Snelheid, Google-integratie |
| **OpenAI Codex** | Parallelle implementatie | Code completion, batch operaties |
| **ChatGPT** | Research, brainstorm, schrijven | Conversationeel, breed kennisbereik |

## Coördinatiemechanisme

### Probleem
Vier agenten die ongecoördineerd aan hetzelfde project werken = gegarandeerde conflicten.

### Oplossing: Sync Protocol

```
┌──────────┐     sync files      ┌──────────┐
│  Claude  │ ◄──────────────────► │  Gemini  │
│  Code    │                      │  CLI     │
└────┬─────┘                      └──────────┘
     │
     │ sync files
     ▼
┌──────────┐
│  OpenAI  │
│  Codex   │
└──────────┘
```

### Sync Files

| Bestand | Schrijver | Lezer | Locatie |
|---------|-----------|-------|---------|
| meta_master_import.json | Claude | Gemini | ~/.gemini/tmp/claude_sync/ |
| meta_master_export.json | Gemini | Claude | ~/.gemini/tmp/claude_sync/ |
| meta_master_import.json | Claude | Codex | ~/.codex/tmp/claude_sync/ |

### Conflict Prevention

Bij sessiestart controleert elke agent:
1. `git pull` — altijd vóór eerste wijziging
2. `git log --oneline -5` — recente commits van andere agenten?
3. `git status` — uncommitted changes van een andere sessie?

Bij conflict: **pull + merge, NOOIT force push.** Bij architecturale tegenstrijdigheid: STOP, vraag de gebruiker.

## Meta_Master als Centraal Brein

Alle agenten gebruiken dezelfde bron van waarheid:

```
Meta_Master/
├── PROJECTS.json      ← Welke projecten bestaan?
├── ECOSYSTEMS.md      ← Hoe hangen ze samen?
├── STATUS.md          ← Wat is de huidige status?
├── PRINCIPLES.md      ← Welke principes gelden?
├── CLAUDE.md          ← Welke protocols gelden?
└── claude_memory/     ← Wat is er geleerd?
```

Dit zorgt ervoor dat het niet uitmaakt welke agent een sessie opent — de context is altijd beschikbaar.

## Rolverdeling in de Praktijk

### Scenario: Nieuwe Feature
1. **ChatGPT** — brainstorm over aanpak, research alternatieven
2. **Claude Code** — WhatIf, implementatie, tests, memory update
3. **Gemini CLI** — review, alternatieve implementatie vergelijken
4. **Codex** — parallelle implementatie voor benchmark

### Scenario: Bug in Productie
1. **Claude Code** — Debug Protocol, RCA, fix implementatie
2. **Gemini CLI** — Second opinion op root cause
3. **Claude Code** — Fix deployen, versioning, commit

### Scenario: Architectuurbeslissing
1. **ChatGPT** — Research, voor/tegen analyse
2. **Claude Code** — Impact op bestaande code, WhatIf
3. **Gemini CLI** — Alternatief perspectief
4. **Beslissing** door de mens → vastleggen in ARCHITECTURE.md
