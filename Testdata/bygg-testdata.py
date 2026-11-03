"""Leser Excel-filene (norske virksomheter og personer) i denne mappa og skriver ../testdata-data.js.

Bruk (fra prosjektroten):  python Testdata/bygg-testdata.py
Bruker bare standardbiblioteket; .xlsx leses direkte som zip/xml.
"""
import json
import pathlib
import re
import zipfile
import xml.etree.ElementTree as ET

HER = pathlib.Path(__file__).resolve().parent
UT = HER.parent / "testdata-data.js"

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def kolonne(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


def les_ark(sti, arknavn):
    z = zipfile.ZipFile(sti)
    delte = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            delte.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    bok = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    for ark in bok.find("m:sheets", NS):
        if ark.get("name") != arknavn:
            continue
        mål = rels[ark.get("{%s}id" % NS["r"])].lstrip("/")
        mål = mål if mål.startswith("xl/") else "xl/" + mål
        rader = []
        for rad in ET.fromstring(z.read(mål)).find("m:sheetData", NS):
            verdier = {}
            for c in rad:
                v = c.find("m:v", NS)
                if c.get("t") == "s" and v is not None:
                    tekst = delte[int(v.text)]
                elif c.get("t") == "inlineStr":
                    tekst = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                else:
                    tekst = v.text if v is not None else ""
                verdier[kolonne(c.get("r"))] = tekst.strip()
            if verdier:
                rader.append([verdier.get(i, "") for i in range(max(verdier) + 1)])
        return rader
    raise SystemExit(f"Fant ikke arket {arknavn!r} i {sti}")


def rad(r, i):
    return r[i] if i < len(r) else ""


# Engelske navn på næringskodene (SSB KLASS, SN2007); kodene i Excel-filen er norske SN2007-koder med fem sifre
NACE_EN = json.loads((HER / "nace-en.json").read_text(encoding="utf-8"))["koder"]

virksomheter = []
for r in les_ark(HER / "NO_EBWOID_Test_Data_BRC.xlsx", "Test Economic operators")[1:]:
    if not rad(r, 0):
        continue
    virksomheter.append({
        "id": rad(r, 0), "euid": rad(r, 1), "navn": rad(r, 2), "adresse": rad(r, 4),
        "nace": rad(r, 5), "naceTekst": rad(r, 6), "naceTekstEn": NACE_EN.get(rad(r, 5), ""), "signatur": rad(r, 7), "dagligLederFnr": rad(r, 8),
    })

personer = []
for r in les_ark(HER / "NO_PID_Test_Data_Digdir.xlsx", "Test persons")[1:]:
    if not rad(r, 0):
        continue
    personer.append({
        "id": rad(r, 0),
        "etternavn": rad(r, 1), "fornavn": rad(r, 2), "fodt": rad(r, 3),
        "fodested": rad(r, 4), "nasjonalitet": rad(r, 5), "fnr": rad(r, 6),
    })

UT.write_text(
    "// Generert av Testdata/bygg-testdata.py fra NO_EBWOID_Test_Data_BRC.xlsx og NO_PID_Test_Data_Digdir.xlsx.\n"
    "// Ikke rediger for hånd.\n"
    f"const TESTVIRKSOMHETER = {json.dumps(virksomheter, ensure_ascii=False, indent=2)};\n"
    f"const TESTPERSONER = {json.dumps(personer, ensure_ascii=False, indent=2)};\n",
    encoding="utf-8",
)
print(len(virksomheter), "virksomheter,", len(personer), "personer ->", UT.name)
