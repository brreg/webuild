"""Sjekker tekstnøkler (i18n.js mot HTML/JS) og ubrukte CSS-klasser i forslag/.

Bruk: python verktoy/sjekk-tekster.py [prosjektrot]
"""
import re, json, sys, pathlib

rot = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent


def les(p):
    return (rot / p).read_text(encoding="utf-8")


js = les("i18n.js")
s = js.index("const NB = ") + 11
nb, _ = json.JSONDecoder().raw_decode(js[s:])
en = set(re.findall(r'"([\w.]+)":', js[js.index("const EN = "):]))
sider = [p.read_text(encoding="utf-8") for p in sorted((rot / "forslag").glob("*.html"))]
kode = "".join(sider) + les("oppslag.js") + les("bilder.js")

brukt = set(re.findall(r'data-i18n="([\w.]+)"', kode))
for attr in re.findall(r'data-i18n-attr="([^"]+)"', kode):
    for par in attr.split(";"):
        brukt.add(par.split("=")[1])
brukt |= set(re.findall(r'data-tekst="([\w.]+)"', kode))
brukt |= set(re.findall(r'T\("([\w.]+)"\)', kode))
dyn = ("c.", "bilde.")
print("NB ubrukt:", sorted(k for k in nb if k not in brukt and not k.startswith(dyn)))
print("brukt, men uten NB og EN:", sorted(k for k in brukt if k not in nb and k not in en))
print("EN ubrukt:", sorted(k for k in en if k not in brukt and not k.startswith(dyn + ("title.",))))

css = re.sub(r"/\*.*?\*/", "", les("forslag/styles.css"), flags=re.S)
klasser = set(re.findall(r"\.([a-zA-Z][\w-]*)", css))
html_klasser = set()
for m in re.findall(r'class="([^"]+)"', kode):
    html_klasser |= set(m.split())
html_klasser |= set(re.findall(r'classList\.\w+\("([\w-]+)"', kode))
html_klasser |= set(re.findall(r'className = "([\w -]+)"', kode))
print("CSS-klasser uten bruk:", sorted(c for c in klasser if c not in html_klasser and c not in kode))
print("debug:", re.findall(r"console\.\w+|debugger", kode))
