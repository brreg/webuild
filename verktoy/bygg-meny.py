"""Skriver toppmenyen og undermenyen fra verktoy/meny.html inn i hver side i forslag/, med aria-current på aktiv side.

Bruk: python verktoy/bygg-meny.py [prosjektrot]
Hvilken side som hører til hvilket menypunkt og hvilken undermeny står i verktoy/sider.py.
"""
import pathlib
import re
import sys

from sider import SIDER, MAIN_OF, GROUP_OF

rot = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
mal = (pathlib.Path(__file__).resolve().parent / "meny.html").read_text(encoding="utf-8")

header = re.search(r'<header class="topp">.*?</header>', mal, re.S).group(0)
under = {m.group(1): m.group(0) for m in re.finditer(r'<nav class="undermeny" data-group="([\w-]+)".*?</nav>', mal, re.S)}


def aktiv(blokk, side):
    return blokk.replace(f'<a href="{side}.html" ', f'<a href="{side}.html" aria-current="page" ', 1)


endret = []
for p in SIDER:
    fil = rot / "forslag" / (p + ".html")
    src = fil.read_text(encoding="utf-8")
    # aria-current bare i hovedmenyen, ikke på logoen og navnet (som også lenker til index.html)
    start, slutt = header.index('<nav class="meny"'), header.index("</nav>")
    h = header[:start] + aktiv(header[start:slutt], MAIN_OF[p]) + header[slutt:]
    if p in GROUP_OF:
        n = aktiv(under[GROUP_OF[p]], p).replace(f' data-group="{GROUP_OF[p]}"', "", 1)
        h += "\n\n    " + n
    ny = re.sub(r'<header class="topp">.*?</header>(\s*<nav class="undermeny".*?</nav>)?', lambda _: h, src, count=1, flags=re.S)
    if ny != src:
        fil.write_text(ny, encoding="utf-8", newline="\n")
        endret.append(p)
print("Endret:", ", ".join(endret) if endret else "ingen")
