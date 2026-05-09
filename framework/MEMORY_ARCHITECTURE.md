# Memory Architecture — Persistent Context Across Sessions

## Het Probleem

AI-agenten hebben geen geheugen tussen sessies. Elke nieuwe sessie begint vanaf nul. Zonder interventie verliest de AI:
- Wie de gebruiker is en wat zijn voorkeuren zijn
- Welke fouten eerder gemaakt zijn en hoe ze gecorrigeerd werden
- De status van lopende projecten
- Architectuurbeslissingen en hun rationale

## De Oplossing: Typed Persistent Memory

### Memory Types

| Type | Doel | Voorbeeld |
|------|------|-----------|
| **user** | Wie is de gebruiker? | "Senior IT Architect, werkt in NL/EN" |
| **feedback** | Wat moet anders? | "Nooit 'path' als variabelenaam in zsh" |
| **project** | Projectcontext | "Merge freeze tot 2026-03-05" |
| **reference** | Waar vind ik info? | "Pipeline bugs in Linear project INGEST" |

### Structuur per Memory File

```markdown
---
name: <naam>
description: <één regel — wordt gebruikt voor relevantie-matching>
type: <user|feedback|project|reference>
---

<inhoud>

**Why:** <waarom is dit belangrijk>
**How to apply:** <wanneer en hoe toepassen>
```

### Memory Index (MEMORY.md)

Centraal indexbestand dat bij elke sessie geladen wordt:
- Één regel per memory, max 150 karakters
- Gesorteerd op categorie (projecten, gebruiker, feedback, referenties)
- Pointer naar het volledige memory bestand

## Opslag Architectuur

```
┌────────────────────────────────┐
│  Claude Code Runtime           │
│  ~/.claude/projects/.../memory/│
│  ├── MEMORY.md (index)         │
│  ├── user_profile.md           │
│  ├── feedback_*.md             │
│  ├── project_*.md              │
│  └── reference_*.md            │
└────────────┬───────────────────┘
             │ sync (bij sessie-einde)
             ▼
┌────────────────────────────────┐
│  Meta_Master (git-tracked)     │
│  claude_memory/                │
│  ├── MEMORY.md                 │
│  ├── user_profile.md           │
│  ├── feedback_*.md             │
│  └── project_*.md              │
└────────────┬───────────────────┘
             │ push → GitHub
             ▼
┌────────────────────────────────┐
│  GitHub (backup + audit trail) │
│  cpaglebbeek/Meta_Master       │
│  └── claude_memory/            │
└────────────────────────────────┘
```

## Cross-Agent Sync

Vier agenten, vier geheugensystemen, één synchronisatiemechanisme:

```
Claude Code ──► meta_master_import.json ──► Gemini CLI
Claude Code ──► meta_master_import.json ──► OpenAI Codex
Gemini CLI  ──► meta_master_export.json ──► Claude Code
```

**Locaties:**
- `~/.gemini/tmp/claude_sync/` — Claude ↔ Gemini
- `~/.codex/tmp/claude_sync/` — Claude ↔ Codex

## Effectiviteit

### Zonder memory systeem:
- Elke sessie: "Ik ben een IT Architect, werk aan PhotoVerify..." (context verloren)
- Herhaalde fouten: dezelfde zsh `path` bug elke sessie opnieuw
- Geen continuïteit: vorige sessie beslissingen onbekend

### Met memory systeem:
- Sessie start: AI weet wie je bent, wat je voorkeuren zijn, welke fouten vermeden moeten worden
- Feedback accumuleert: na 30+ correcties gedraagt de AI zich significant anders
- Projectcontext beschikbaar: lopende taken, deadlines, stakeholders

## Metrics

| Metric | Huidig | Betekenis |
|--------|--------|-----------|
| Totaal memories | 70+ | Opgebouwde kennisbasis |
| Feedback memories | 30+ | Geleerde lessen |
| Project memories | 50+ | Actieve projectcontext |
| Agents met sync | 3 | Claude, Gemini, Codex |
