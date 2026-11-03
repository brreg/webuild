// Skjermbilder ved steg: et ikon (button.bilde) åpner bildet i en dialogboks.
// Markup: <button type="button" class="bilde" data-bilde="bildefil" data-tekst="nøkkel i i18n.js">…</button>
// Bildet lastes først når ikonet klikkes. Dialogen lukkes med Esc, lukkeknappen eller klikk utenfor bildet.
(function () {
  const T = (key) => (window.I18N ? I18N.t(key) : key);
  let dlg, img, tekst, lukk, aktiv;

  const bygg = () => {
    dlg = document.createElement("dialog");
    dlg.className = "bildedialog";
    dlg.innerHTML = '<figure><img alt=""><figcaption></figcaption></figure><button type="button" class="lukk">×</button>';
    img = dlg.querySelector("img");
    tekst = dlg.querySelector("figcaption");
    lukk = dlg.querySelector(".lukk");
    lukk.addEventListener("click", () => dlg.close());
    dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener("close", () => { if (!dlg.open) { img.removeAttribute("src"); aktiv = null; } });
    document.body.appendChild(dlg);
  };

  const tekster = () => {
    const t = T(aktiv.dataset.tekst);
    img.alt = t;
    tekst.textContent = t;
    dlg.setAttribute("aria-label", t);
    lukk.setAttribute("aria-label", T("bilde.lukk"));
  };

  document.addEventListener("click", (e) => {
    const knapp = e.target.closest("button.bilde");
    if (!knapp) return;
    if (!dlg) bygg();
    aktiv = knapp;
    img.src = knapp.dataset.bilde;
    tekster();
    dlg.showModal();
  });
  document.addEventListener("langchange", () => { if (dlg && dlg.open && aktiv) tekster(); });
})();
