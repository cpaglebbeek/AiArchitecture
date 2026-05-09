# Mail aan Mark Paauwe — AI Governance & Samenwerking

**Onderwerp:** Dat rapport over AI-kwaliteit — en waarom jouw methode de basis is

---

Hi Mark,

Je vroeg gisteren of ik een rapport kon sturen over hoe ik AI "in de tank hou" — minder hallucinaties, voorspelbaardere output. Ik heb er iets beters van gemaakt.

## Wat ik heb gebouwd

Ik heb een scanner geschreven die al mijn 77 repositories analyseert op gestructureerd AI-gebruik. Niet op gevoel, op feiten. De resultaten:

| Metric | Waarde |
|--------|--------|
| Repositories beheerd | 77 |
| AI co-authored commits | 1.196 |
| Constraint coverage (CLAUDE.md) | 76.6% |
| Persistent memories | 114 |
| Feedback loops (geleerde lessen) | 34 |
| WhatIf protocol adoptie | 69.5% |
| Versioning discipline | 62.7% |
| Architectuurprincipes | 25 (over 7 Design Areas) |

De scanner is herhaalbaar — ik kan hem op elk moment opnieuw draaien en de groei over tijd meten.

## Waarom Dragon1 de basis is

Wat me opviel toen ik de resultaten analyseerde: mijn hele aanpak is 85-90% aligned met Dragon1-methodologie. Niet omdat ik het bewust kopieerde, maar omdat het werkt:

- **Principes als causale mechanismen** — niet "we streven naar X" maar "Door [actie] bereiken we [effect] waardoor [resultaat]". Precies zoals jij het uitlegt.
- **Total Concept** — constructief (code), operatief (WhatIf Protocol, Debug Protocol), decoratief (DESIGN_TOKENS.md per project). Vitruvius in de praktijk.
- **Conceptniveaus** — core logic gescheiden van platform. Mijn PhotoVerify ecosysteem doet dat: één Meta engine, drie platforms (Android/iOS/Web).
- **7 Design Areas** — Governance, Data, Applicatie, Technologie, Beveiliging, Multi-Agent, Kwaliteit. Dwars door ArchiMate-lagen heen, net als jouw opzet.

En dan die beschrijvende rendering waar je vandaag mee bezig was — ArchDSL met universes en collections. Dat is precies wat ik doe met SVG en repo-data: architectuur als code, niet als bitmap. Versioneerbaar, diffable, machine-leesbaar.

## Live bewijs — vandaag

Vandaag heb ik 14 iteraties van de EA blauwdruk voor de DB gebouwd (mark7 t/m mark20). Elk een volledige interactieve HTML met bewerkbare repository, failure simulation, impact analyse, fase-management en ArchDSL-generatie.

### AI maakt voorspelbare fouten — en dat is juist de kracht

Vandaag 33 bugs gevangen in development, 0 naar productie. Wat opvalt: AI maakt steeds dezelfde **categorieën** fouten. Ik heb 8 terugkerende patronen geïdentificeerd:

| Patroon | Wat AI fout doet | Hoe vaak |
|---------|-----------------|----------|
| **Feature-verlies** | Genereert nieuwe versie, vergeet features van vorige | 6× |
| **Quote-escaping** | Verwart 3 contexten (HTML/JS/JS-in-HTML) | 3× |
| **SVG innerHTML** | Gebruikt DOM API die stil faalt op SVG namespace | 3× |
| **Refactor-restanten** | Hernoemt maar updatet niet alle referenties | 2× |
| **Brede replace** | Vervangt ALLE voorkomens i.p.v. alleen het doel | 1× |
| **Oneindige recursie** | Maakt wederzijdse functie-aanroepen | 1× |

Dit is wat jij bedoelt met "AI is een copycat" — hij combineert patronen maar begrijpt de onderliggende structuur niet. Het verschil met vibe coding: ik **verwacht** deze fouten en heb een systeem om ze te vangen.

**Elke bug doorloopt:** kleur-classificatie → RCA 3 niveaus → patroon-match → grep-detectie → checklist-item → feedback memory. 33 bugs → 8 patronen → 27-punts checklist → 0 productiefouten.

Dat is het framework in actie. Niet theorie — productie. En het is jouw methodiek (principes als mechanismen, explicitering, conceptniveaus) die het fundament vormt.

## Het interactieve dashboard

Ik heb er een interactief dashboard van gemaakt:
**icthorse.nl/aigovernance**

En een uitgebreid artikel met de Dragon1-link:
**icthorse.nl/aigovernance/article.html**

De broncode is open source:
**github.com/cpaglebbeek/AiArchitecture**

## Over de Library en Templates

Je vroeg of ik Library en Template builder aan de vergelijking wil toevoegen — doe ik. Die universes/collections uitbreiding van ArchDSL is trouwens precies het soort feature waar mijn AModeler ook naartoe beweegt. Complementair, niet concurrerend.

Laat me weten wat je ervan vindt. En of je moeder het beter maakt — dat gaat voor.

Groet,
Christian

---

*iCt Horse — Connecting the dots.*
*KvK 96787112 | icthorse.nl*
