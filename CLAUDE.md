# Instruksjoner for Claude

- `brreg-filialregistrering.html` (enkeltfil-eksporten) bygges bare når brukeren uttrykkelig ber om det, og da med
  `python verktoy/bygg-eksport.py` (aldri ved å redigere filen for hånd). Filen er i `.gitignore` og skal ikke committes.
- Endringer i `forslag/`, `i18n.js` osv. er ingen grunn i seg selv til å bygge eksporten på nytt.
- Ikke commit direkte til hovedgrenen (`main`/`master`). Lag en egen branch, og opprett en pull request ved behov slik at
  en annen person kan gjennomgå endringene manuelt i GitHub.
