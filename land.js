// Forsiden: kortet «Branch registration in the other country» viser flagg for landene med nasjonal løsning.
// Et klikk på et flagg spør først om den nasjonale løsningen skal åpnes i en ny fane.
// Markup: button.land-valg[data-url][data-sporsmal] (se forslag/index.html); data-sporsmal er nøkkelen til spørsmålet i dialogen.
(function () {
  const T = (key) => I18N.t(key);
  let dlg, tekst, adresse, apne, avbryt, valgt;

  const bygg = () => {
    dlg = document.createElement("dialog");
    dlg.className = "valgdialog";
    dlg.innerHTML = '<p class="sporsmal"></p><p class="adresse"></p><div class="knapper"><button type="button" class="apne"></button><button type="button" class="avbryt"></button></div>';
    tekst = dlg.querySelector(".sporsmal");
    adresse = dlg.querySelector(".adresse");
    apne = dlg.querySelector(".apne");
    avbryt = dlg.querySelector(".avbryt");
    avbryt.addEventListener("click", () => dlg.close());
    apne.addEventListener("click", () => {
      window.open(valgt.dataset.url, "_blank", "noopener");
      dlg.close();
    });
    dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
    document.body.appendChild(dlg);
  };

  const tekster = () => {
    tekst.textContent = T(valgt.dataset.sporsmal).replace("{land}", valgt.textContent.trim());
    adresse.textContent = valgt.dataset.url;
    apne.textContent = T("land.apne");
    avbryt.textContent = T("land.avbryt");
    dlg.setAttribute("aria-label", tekst.textContent);
  };

  document.addEventListener("click", (e) => {
    const valg = e.target.closest("button.land-valg");
    if (!valg) return;
    if (!dlg) bygg();
    valgt = valg;
    tekster();
    dlg.showModal();
    apne.focus();
  });
  document.addEventListener("langchange", () => { if (dlg && dlg.open && valgt) tekster(); });
})();
