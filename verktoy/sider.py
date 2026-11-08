"""Sidene i forslag/ og hvor de hører hjemme i menyen. Brukes av bygg-meny.py og bygg-eksport.py."""

SIDER = ["index", "tildele-fullmakt", "hente-fullmakt", "hente-eucc", "filialregistrering",
         "oppslag-testvirksomhet", "oppslag-testperson", "dokumentasjon", "autentisk-kilde"]
# Hvilket punkt i toppmenyen som er aktivt for hver side
MAIN_OF = {p: p for p in SIDER}
MAIN_OF.update({"hente-fullmakt": "tildele-fullmakt", "oppslag-testperson": "oppslag-testvirksomhet"})
# Hvilken undermeny (data-group i verktoy/meny.html) siden viser
GROUP_OF = {"tildele-fullmakt": "fullmakter", "hente-fullmakt": "fullmakter",
            "oppslag-testvirksomhet": "testdata", "oppslag-testperson": "testdata"}
