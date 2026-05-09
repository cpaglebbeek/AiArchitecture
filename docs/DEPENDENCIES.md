# Dependencies — Relaties met Andere Projecten

## Directe Afhankelijkheden

| Project | Relatie | Type | Richting |
|---------|---------|------|----------|
| Meta_Master | PROJECTS.json als input voor scanner | Data | Read-only |
| Meta_Master | PRINCIPLES.md als bron voor principes | Referentie | Read-only |
| Meta_Master | claude_memory/ als bron voor memory metrics | Data | Read-only |
| Alle repos | Scan-targets voor metrics | Data | Read-only |

## Strategische Relaties

| Project | Relatie | Context |
|---------|---------|---------|
| Dragon1Samenwerking | Doelgroep: Mark Paauwe overtuigen | Business case |
| WerkDierenbescherming | Profilering IT Architect + AI | Professioneel |
| iCt_Horse (website) | Publicatie platform | Distributie |

## Impact Matrix

| Als dit verandert... | Dan moet dit geupdate worden... |
|---------------------|-------------------------------|
| PROJECTS.json (nieuwe repo) | Scanner vindt het automatisch |
| CLAUDE.md template | Framework docs (CONSTRAINT_SYSTEM.md) |
| Memory structuur | Framework docs (MEMORY_ARCHITECTURE.md) |
| Nieuw protocol | Framework docs (QUALITY_CONTROLS.md) |
| Nieuwe agent | Framework docs (MULTI_AGENT.md) |

## Geen Afhankelijkheden Op

Dit project schrijft NOOIT naar andere repos. Het is puur lezend/analyserend.
