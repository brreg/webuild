"""Bygger én selvstendig HTML-fil (brreg-filialregistrering.html) fra forslag/, med CSS, JS og bilder innebygd.

Bruk: python verktoy/bygg-eksport.py [prosjektrot] [utfil]
Uten argumenter brukes prosjektmappen og brreg-filialregistrering.html i den.
Kjøres bare manuelt ved behov; utfilen er i .gitignore og skal ikke committes.
Nye sider i forslag/ må legges til i SIDER (og eventuelt MAIN_OF / GROUP_OF) i verktoy/sider.py.
"""
import base64
import json
import pathlib
import re
import sys

from sider import SIDER, MAIN_OF, GROUP_OF

rot = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
ut = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else rot / "brreg-filialregistrering.html"
mappe = rot / "forslag"


def les(p):
    return (mappe / p).read_text(encoding="utf-8")


def datauri(sti):
    b = (rot / sti).read_bytes()
    mime = {".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg"}[pathlib.Path(sti).suffix.lower()]
    return f"data:{mime};base64," + base64.b64encode(b).decode("ascii")


def lenker(html):
    html = re.sub(r'href="([a-z-]+)\.html"', r'href="#\1"', html)
    # interne lenker skal navigere i samme fane
    return re.sub(r'(<a [^>]*href="#[a-z-]+"[^>]*?) target="_blank" rel="noopener"', r"\1", html)


css = les("styles.css").replace('url("../assets/we-build-mal-gul.png")', f'url("{datauri("assets/we-build-mal-gul.png")}")')
bu2 = datauri("assets/bu2.png")

index = les("index.html")
deko = "".join(re.findall(r'<div class="deko [^"]*" aria-hidden="true"></div>\n?', index)).strip()
header = re.search(r'<header class="topp">.*?</header>', index, re.S).group(0)
header = re.sub(r' aria-current="page"', "", header)
footer = re.search(r'<footer class="bunn">.*?</footer>', index, re.S).group(0)
ansvar = re.search(r'<p class="ansvar"[^>]*>.*?</p>', index, re.S).group(0)
skjul = re.search(r"<script>try \{.*?</script>", index).group(0)  # skjuler siden til norsk tekst er satt inn


def undermeny(fil, gruppe):
    m = re.search(r'<nav class="undermeny".*?</nav>', les(fil), re.S).group(0)
    m = re.sub(r' aria-current="page"', "", m)
    return m.replace('<nav class="undermeny"', f'<nav class="undermeny" data-group="{gruppe}" hidden', 1)


under = undermeny("tildele-fullmakt.html", "fullmakter") + "\n" + undermeny("oppslag-testvirksomhet.html", "testdata")

sider, skript, titler = [], [], {}
for p in SIDER:
    src = les(p + ".html")
    titler[p] = re.search(r'<title data-i18n="([^"]+)"', src).group(1)  # nøkkel i i18n.js
    inner = re.search(r'<main class="innhold[^"]*" id="innhold">(.*?)</main>', src, re.S).group(1)
    inner = inner.replace('src="../assets/bu2.png"', f'src="{bu2}"')
    inner = re.sub(r'data-bilde="\.\./(assets/steg/[^"]+)"', lambda m: f'data-bilde="{datauri(m.group(1))}"', inner)
    sider.append(f'<div class="side-innhold" id="page-{p}" hidden>{lenker(inner)}</div>')
    for s in re.findall(r"<script>(.*?)</script>", src[src.index("<body>"):], re.S):  # f.eks. skjema-script
        skript.append(s)

i18n = (rot / "i18n.js").read_text(encoding="utf-8") + "\n" + (rot / "bilder.js").read_text(encoding="utf-8")
data = (rot / "testdata-data.js").read_text(encoding="utf-8")
oppslag = (rot / "oppslag.js").read_text(encoding="utf-8")

router = """
const MAIN_OF = %s, GROUP_OF = %s, TITLES = %s;
let current = "index";
const setTitle = () => { document.title = I18N.t(TITLES[current]); };
function route() {
  if (location.hash === "#innhold") return;
  let p = (location.hash || "#index").slice(1);
  if (!document.getElementById("page-" + p)) p = "index";
  current = p;
  document.querySelectorAll(".side-innhold").forEach(e => e.hidden = e.id !== "page-" + p);
  document.getElementById("innhold").classList.toggle("forside", p === "index");
  setTitle();
  document.querySelectorAll("nav a").forEach(a => {
    const t = (a.getAttribute("href") || "").slice(1);
    const aktiv = a.closest("nav").classList.contains("meny") ? t === MAIN_OF[p] : t === p;
    if (aktiv) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
  });
  document.querySelectorAll("nav.undermeny").forEach(n => n.hidden = n.dataset.group !== GROUP_OF[p]);
  window.scrollTo(0, 0);
}
window.addEventListener("hashchange", route);
document.addEventListener("langchange", setTitle);
route();
""" % (json.dumps(MAIN_OF), json.dumps(GROUP_OF), json.dumps(titler))

html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Brønnøysund Register Centre | Branch registration</title>
  <link rel="icon" href="{datauri("assets/favicon.png")}" type="image/png">
  {skjul}
  <style>
{css}
  </style>
</head>
<body>
  <a class="skip" href="#innhold" style="position:absolute;left:-999px" data-i18n="skip">Skip to content</a>
  <div class="side">
    {deko}
    {lenker(header)}
{lenker(under)}
    <main class="innhold" id="innhold">
{chr(10).join(sider)}
    </main>
    {ansvar}
    {footer}
  </div>
  <script>
{i18n}
{data}
{oppslag}
{chr(10).join(skript)}
{router}
  </script>
</body>
</html>
"""
ut.write_text(html, encoding="utf-8", newline="\n")
print(len(html), "bytes")
