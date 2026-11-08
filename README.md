# Filialregistrering med lommebok og bevis (WE BUILD-demo)

Statisk demo fra Brønnøysundregistrene, basert på WE BUILD-piloten **BU2 «Create Company Branch»**
(EUDI-lommebok, EU PoA, EUCC, PID og European Business Wallet). All data er fiktive testdata.
Ingen backend, ingen byggesteg for å kjøre siden: ren HTML, CSS og JavaScript uten avhengigheter.

## Kjøre lokalt

```bash
python -m http.server 8080
```

Åpne deretter <http://localhost:8080/forslag/index.html>. (`.claude/launch.json` har samme oppsett som «static-site».)

## To løsninger

| Løsning | Brukes av | Sider |
|---|---|---|
| Norsk selskap registrerer filial i utlandet | Norsk virksomhet | Tildele fullmakt (EU PoA), Hente fullmakt (EU PoA), Hente EUCC |
| Utenlandsk virksomhet registrerer filial i Norge | Utenlandsk virksomhet | Filialregistrering |

I tillegg: **For QTSP-er** (dokumentasjon av autentisk kilde-API-et), **Testdata** (oppslag på testvirksomhet og testperson)
og **Dokumentasjon** (begreper og lenker).

## Mappestruktur

```
forslag/                 WE BUILD-løsningen (dette er den gjeldende versjonen)
  index.html             forside med de to løsningene
  tildele-fullmakt.html  steg 1 for norsk selskap
  hente-fullmakt.html    steg 2
  hente-eucc.html        steg 3
  filialregistrering.html  utenlandsk virksomhet registrerer filial i Norge
  oppslag-testvirksomhet.html, oppslag-testperson.html  testdata
  dokumentasjon.html     begreper og referanser
  autentisk-kilde.html   dokumentasjon av autentisk kilde-API-et (ETSI TS 119 478)
  styles.css             felles stilark
i18n.js                  språkvelger og alle tekster (NB-ordbok + EN for tekster som bare brukes fra JS)
bilder.js                skjermbilder som dialog ved steg
oppslag.js               oppslag på testvirksomheter og testpersoner
testdata-data.js         GENERERT fra Excel-filene i Testdata/ (ikke rediger for hånd)
Testdata/                Excel-kildene (norske virksomheter og personer), nace-en.json og bygg-testdata.py
assets/                  bu2.png, we-build-mal-gul.png, favicon.png og apple-touch-icon.png (WE BUILD-logoen) og steg/ med skjermbilder
verktoy/                 meny.html (felles meny), sider.py (sideliste), bygg-meny.py, bygg-eksport.py og sjekk-tekster.py
brreg-filialregistrering.html   GENERERT enkeltfil-eksport av forslag/, bygges bare ved behov (ikke i git)
```

`index.html` i roten sender bare videre til `forslag/index.html`. Den eldre versjonen av demoen (sider i rotmappen) er fjernet, men finnes i git-historikken.

## Språk

Engelsk er forhåndsvalgt, norsk velges øverst til høyre (valget huskes i nettleseren, `localStorage`-nøkkel `sprak`).
Når norsk er valgt, skjuler et lite skript i `<head>` siden til `i18n.js` har satt inn de norske tekstene, så den engelske
teksten ikke blinker forbi. Skriptet må med i `<head>` på alle sidene.

- Den engelske teksten står i HTML-en, markert med `data-i18n="nøkkel"` (innholdet byttes) eller
  `data-i18n-attr="attributt=nøkkel;..."` (attributter).
- Den norske teksten står i `NB` i [i18n.js](i18n.js). `EN` i samme fil inneholder bare tekster som brukes fra JavaScript
  (sidetitler, oppslag, bildetekster).
- Nye tekster må inn både i HTML-en og i `NB`. Kjør `python verktoy/sjekk-tekster.py` for å finne manglende eller ubrukte nøkler
  og ubrukte CSS-klasser.

## Skjermbilder ved steg

Et steg kan ha et ikon som åpner et bilde i en dialog (se [bilder.js](bilder.js)):

```html
<button type="button" class="bilde" data-bilde="../assets/steg/fil.png" data-tekst="bilde.nøkkel">…ikon…</button>
```

Legg bildet i `assets/steg/` og bildeteksten (`bilde.nøkkel`) i både `EN` og `NB` i `i18n.js`.

## Testdata

Excel-filene i `Testdata/` er kilden. Etter endringer:

```bash
python Testdata/bygg-testdata.py
```

Dette skriver `testdata-data.js` (`TESTVIRKSOMHETER`, `TESTPERSONER`). Skriptet bruker bare standardbiblioteket.

Næringskodene i Excel-filen er norske SN2007-koder med norsk tekst. De engelske tekstene ligger i `Testdata/nace-en.json`
(hentet fra SSB KLASS, engelsk versjon av SN2007) og vises når språket er engelsk. Nye koder må legges til i den filen.
Adresser og navn oversettes ikke.

## Enkeltfil-eksport

`brreg-filialregistrering.html` samler alle sidene i `forslag/` i én fil (hash-ruting, innebygd CSS, JS og bilder):

```bash
python verktoy/bygg-eksport.py
```

Eksporten bygges bare manuelt når det trengs en enkeltfil å dele, og den er ikke en del av den vanlige arbeidsflyten.
Filen står i `.gitignore` og skal ikke committes. Claude Code bygger den bare når du ber om det, og spør om lov først
(se `CLAUDE.md` og `.claude/settings.json`). Skriptet tar med sidene som står i `SIDER` i `verktoy/sider.py`.

## Meny

Toppmenyen og undermenyene står én gang i `verktoy/meny.html` og skrives inn i alle sidene i `forslag/` med

```bash
python verktoy/bygg-meny.py
```

Skriptet setter `aria-current="page"` ut fra `MAIN_OF` og `GROUP_OF` i `verktoy/sider.py`. Ikke rediger menyen direkte
i sidene; endringene blir overskrevet neste gang skriptet kjøres.

## Legge til en ny side

1. Kopier en eksisterende side i `forslag/` (f.eks. `dokumentasjon.html`) og endre innholdet. Behold favicon-lenkene i
   `<head>` og ansvarsteksten (`<p class="ansvar">`) over `<footer>`; de skal være på alle sidene.
2. Legg siden til i `SIDER` (og `MAIN_OF` / `GROUP_OF`) i `verktoy/sider.py`, og menypunktet
   (`<li><a href="ny.html" data-i18n="nav.ny">…</a></li>`) i `verktoy/meny.html`. Tekstene legges i `i18n.js`.
3. Kjør `python verktoy/bygg-meny.py`.

## Miljøvariabler og API

Ingen. Siden er statisk og har ingen backend eller API-endepunkter.

## Lisens

- Kildekoden er lisensiert under [EUPL-1.2](LICENSE).
- Dokumentasjon og egne tekster er lisensiert under [CC BY 4.0](LICENSE-docs).
- **Unntak:** WE BUILD-logoen, EU-emblemet og merket «Co-funded by the European Union», andre logoer og varemerker,
  skjermbilder av tredjepartstjenester (`assets/steg/`) og testdataene i `Testdata/` er ikke omfattet av lisensene.
  Se [NOTICE](NOTICE) for detaljer.

Prosjektet er medfinansiert av Den europeiske union. Synspunktene som uttrykkes, er utelukkende forfatterens og
gjenspeiler ikke nødvendigvis synspunktene til Den europeiske union eller den bevilgende myndigheten.
