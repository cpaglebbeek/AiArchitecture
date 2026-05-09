# ARCHITECTURE.md — AiArchitecture

## Overzicht

AiArchitecture is een meta-project dat de AI-samenwerkingspraktijken van iCt Horse analyseert, documenteert en meetbaar maakt. Het project scant alle repositories en extraheert bewijs van gestructureerd AI-gebruik.

## Componenten

### 1. Framework (`framework/`)
Documentatie van de methodiek — HOE en WAAROM de aanpak werkt.

| Component | Beschrijving | Relatie |
|-----------|-------------|---------|
| OVERVIEW.md | Totaaloverzicht methodiek | Verwijst naar alle andere framework docs |
| PROMPTING_PATTERNS.md | Catalogus prompting patronen | Bewijst: Meta_Master/CLAUDE.md patronen |
| MEMORY_ARCHITECTURE.md | Memory systeem design | Bewijst: ~/.claude/memory/ structuur |
| CONSTRAINT_SYSTEM.md | Constraints en protocols | Bewijst: CLAUDE.md files in alle repos |
| QUALITY_CONTROLS.md | Kwaliteitsborging | Bewijst: versioning, RCA, debug protocols |
| MULTI_AGENT.md | Multi-agent orkestratie | Bewijst: sync files, agent co-authoring |
| SECURITY_PRACTICES.md | Beveiligingspraktijken | Bewijst: git-crypt, infra safety |
| PRINCIPLES.md | Architectuurprincipes | Link naar Meta_Master/PRINCIPLES.md |

### 2. Evidence (`evidence/`)
Bewijsmateriaal uit echte projecten.

| Component | Beschrijving | Bron |
|-----------|-------------|------|
| metrics/ | Harde cijfers uit scans | repo_scanner.py output |
| case_studies/ | Concrete projectvoorbeelden | Handmatig geschreven |
| before_after/ | Voor/na vergelijkingen | Handmatig + scan data |

### 3. Tools (`tools/`)
Scanning en rapportage tooling.

| Component | Beschrijving | Input | Output |
|-----------|-------------|-------|--------|
| repo_scanner.py | Scant alle repos op AI-praktijken | PROJECTS.json | evidence/metrics/ |
| metrics_collector.py | Aggregeert metrics | evidence/metrics/ | reports/ |
| report_generator.py | Genereert rapporten | evidence/ + framework/ | reports/ |

### 4. Reports (`reports/`)
Gegenereerde output voor verschillende doelgroepen.

## Data Flow

```
PROJECTS.json (Meta_Master)
        │
        ▼
  repo_scanner.py ──► evidence/metrics/*.json
        │
        ▼
  metrics_collector.py ──► geaggregeerde metrics
        │
        ▼
  report_generator.py ──► reports/latest_scan.md
                      ──► reports/linkedin/
```

## Relaties met andere projecten

| Project | Relatie | Type |
|---------|---------|------|
| Meta_Master | Bron: PROJECTS.json, PRINCIPLES.md | Input (read-only) |
| Alle repos | Scan-targets voor metrics | Input (read-only) |
| Dragon1Samenwerking | Context: waarom dit project bestaat | Strategisch |
| WerkDierenbescherming | Context: IT Architect profiel | Strategisch |
| iCt_Horse | Ecosysteem: capability showcase | Eigenaar |

## Privacy-architectuur

```
┌─────────────────────────────────────┐
│  Private repos (git-crypt)          │
│  ┌──────────────────────────┐       │
│  │ Content: NIET toegankelijk│       │
│  │ Structuur: WEL scanbaar  │       │
│  │ → Heeft CLAUDE.md? ✓/✗   │       │
│  │ → Heeft memory? ✓/✗      │       │
│  │ → Versioning? ✓/✗        │       │
│  └──────────────────────────┘       │
└─────────────────────────────────────┘
              │
              ▼ (alleen structuur-metrics)
┌─────────────────────────────────────┐
│  AiArchitecture (PUBLIC)            │
│  → Patronen, geen data              │
│  → Aantallen, geen inhoud           │
│  → Structuren, geen secrets         │
└─────────────────────────────────────┘
```
