# Framework Overview — iCt Horse AI Architecture

## Het Probleem

De meeste developers die met AI werken volgen een patroon dat we "vibe coding" noemen:
1. Schrijf een prompt
2. Hoop dat de output klopt
3. Fix handmatig wat niet werkt
4. Herhaal

Dit levert onvoorspelbare kwaliteit, inconsistente code, beveiligingsproblemen en geen leercurve — de AI maakt dezelfde fouten steeds opnieuw.

## De iCt Horse Aanpak

Wij behandelen AI als een **junior architect die werkt binnen een strikt kader**. Niet beperkt in creativiteit, maar begrensd in scope, kwaliteit en veiligheid.

### De 7 Pijlers

```
┌─────────────────────────────────────────────────┐
│              AI Architecture Framework           │
├─────────────┬─────────────┬─────────────────────┤
│  CONSTRAINTS │  PROTOCOLS  │  MEMORY             │
│  (wat mag)   │  (hoe werk) │  (wat onthouden)    │
├─────────────┼─────────────┼─────────────────────┤
│  QUALITY     │  MULTI-AGENT│  SECURITY           │
│  (hoe goed)  │  (wie doet) │  (hoe veilig)       │
├─────────────┴─────────────┴─────────────────────┤
│              PRINCIPLES (waarom)                 │
└─────────────────────────────────────────────────┘
```

### 1. Constraint System
Elke repository heeft een `CLAUDE.md` bestand dat definieert:
- Wat de AI mag en niet mag doen
- Welke bestanden beschermd zijn
- Welke variabelenamen verboden zijn (zsh safety)
- Welke protocols verplicht zijn

→ Zie [CONSTRAINT_SYSTEM.md](CONSTRAINT_SYSTEM.md)

### 2. Protocols
Gestandaardiseerde workflows die kwaliteit afdwingen:
- **WhatIf Protocol** — begrip → plan → impact → akkoord VÓÓR elke actie
- **Debug Protocol** — kleur → RCA 3 niveaus → WhatIf vóór fix
- **Build Protocol** — change detection → WhatIf → build → verify
- **Over en Uit** — verplichte sync bij sessie-einde

→ Zie [QUALITY_CONTROLS.md](QUALITY_CONTROLS.md)

### 3. Memory Architecture
Persistent geheugen over sessies en agenten heen:
- Typed memories (user, feedback, project, reference)
- Git-tracked mirror (Claude memory → Meta_Master/claude_memory/)
- Cross-agent sync files (Claude ↔ Gemini ↔ Codex)

→ Zie [MEMORY_ARCHITECTURE.md](MEMORY_ARCHITECTURE.md)

### 4. Quality Controls
Mechanismen die voorkomen dat kwaliteit daalt:
- Verplichte versioning bij elke wijziging
- Kleurgecodeerde severity (groen/oranje/rood)
- Root Cause Analysis op 3 niveaus (functioneel/technisch/architectonisch)
- Thematische codenamen per build

→ Zie [QUALITY_CONTROLS.md](QUALITY_CONTROLS.md)

### 5. Multi-Agent Orchestration
Vier AI-agenten die gecoördineerd samenwerken:
- Claude Code (primair: code, architectuur, analyse)
- Gemini CLI (second opinion, alternatieve aanpak)
- OpenAI Codex (parallelle implementatie)
- ChatGPT (research, brainstorm)

→ Zie [MULTI_AGENT.md](MULTI_AGENT.md)

### 6. Security Practices
Beveiliging als onderdeel van het proces, niet als bijzaak:
- git-crypt voor gevoelige repos
- Shared infrastructure awareness
- Multi-session conflict prevention
- Privacy filters in scanning

→ Zie [SECURITY_PRACTICES.md](SECURITY_PRACTICES.md)

### 7. Architecture Principles
25 principes over 7 Design Areas (Dragon1-structuur):
- Governance, Data & Kennis, Applicatie, Technologie
- Beveiliging, Multi-Agent, Kwaliteit & Mens

→ Zie [PRINCIPLES.md](PRINCIPLES.md)

## Meetbaar Resultaat

Dit is geen theoretisch verhaal. De `tools/repo_scanner.py` scant alle repositories en meet:

| Metric | Wat het meet | Waarom het ertoe doet |
|--------|-------------|----------------------|
| Constraint Coverage | % repos met CLAUDE.md | AI weet wat het mag |
| Memory Density | Memories per project | Context blijft behouden |
| Protocol Adoption | Protocols per repo | Kwaliteit is systematisch |
| Security Posture | git-crypt + infra safety | Beveiliging is ingebakken |
| Agent Diversity | Co-authored commits per agent | Multi-agent is echt |
| Versioning Discipline | % commits met versie-bump | Elke wijziging is traceerbaar |

## Voor Wie

- **Enterprise Architects** die AI willen inzetten zonder controle te verliezen
- **IT Managers** die bewijs nodig hebben dat AI-development beheersbaar is
- **Developers** die hun AI-workflow willen structureren
- **Partners** (Dragon1, Staff) die willen zien wat gestructureerd AI-gebruik oplevert
