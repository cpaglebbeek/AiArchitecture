# Security Practices — Beveiliging als Ontwerpprincipe

## Principe

Beveiliging is geen afterthought. Het is ingebakken in het proces, de tooling en de architectuur.

## Beveiligingslagen

### 1. Repository-niveau: git-crypt

Gevoelige repositories worden versleuteld met git-crypt:
- Bestanden zijn versleuteld op disk en in GitHub
- Alleen met de juiste key te ontsleutelen
- Keys worden apart gebackupt (`~/.git-crypt-keys/`)

**Toepassing:** Juridische dossiers, financiële gegevens, persoonlijke data.

**Aantal encrypted repos:** 15+ (gemeten door scanner)

### 2. Infrastructure-niveau: Shared Infrastructure Awareness

Meerdere projecten draaien op dezelfde server (Hetzner HorseCloud55). Eén fout in de configuratie kan alle services breken.

**Protocol:**
- `SHARED_INFRASTRUCTURE.md` documenteert alle services, poorten en afhankelijkheden
- Bij nginx config-wijziging: ALTIJD verifiëren dat ALLE location blocks behouden blijven
- Bij "over en uit": controleren dat alle services draaien

**Projecten op gedeelde infra:**
| Project | Poort | Type |
|---------|-------|------|
| Dashboard | :3980 | Node.js |
| ClaudeWeb | :3000 | Node.js |
| CarriereCV | :3950 | Node.js |
| MacTerminal | :3970 | SSH tunnel |
| PrioMail | :3985 | Node.js |
| CyberNanny | PHP | PHP-FPM |
| RandomRingtone | :3800 | Logger |

### 3. Sessie-niveau: Multi-Session Conflict Prevention

Meerdere agenten kunnen tegelijkertijd aan hetzelfde project werken. Zonder coördinatie gaan wijzigingen verloren.

**6 Conflicttypes:**
1. Simultane bestandswijziging
2. Tegenstrijdige architectuurbeslissingen
3. Versie-conflicten
4. Branch-conflicten
5. Deploy-conflicten
6. Memory/sync-conflicten

**Protocol:** Pull vóór wijziging, merge bij conflict, NOOIT force push.

### 4. Constraint-niveau: Verboden Acties

De AI wordt expliciet beperkt in wat het mag doen:
- Nooit `path` als variabelenaam (zsh safety → breekt hele shell)
- Nooit force push naar main/master
- Nooit credentials committen naar publieke repos
- Nooit bestanden verwijderen zonder akkoord
- Nooit hooks skippen (--no-verify)

### 5. Privacy-niveau: Scanning Filters

De repo scanner (`tools/repo_scanner.py`) heeft ingebouwde privacy filters:
- Private repo content wordt NIET gekopieerd
- Alleen structuur-metrics (heeft CLAUDE.md? ja/nee)
- Geen bestandsinhoud uit encrypted repos
- Publieke output bevat geen persoonsgegevens

## Vergelijking

| Aspect | Typisch AI-project | iCt Horse |
|--------|-------------------|-----------|
| Repo encryptie | Geen | git-crypt voor gevoelige repos |
| Infra awareness | Per project | Gedeeld document, verplichte check |
| Multi-session | Niet geadresseerd | 6-type conflict prevention |
| AI constraints | Geen | Expliciete verboden acties |
| Privacy scanning | Niet van toepassing | Ingebouwde filters |
