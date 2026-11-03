// Oppslag på testvirksomheter og testpersoner (data fra testdata-data.js).
// Brukes av oppslag-testvirksomhet.html og oppslag-testperson.html; hver side har bare sin egen liste.
// Tekstene hentes fra i18n.js (I18N.t) og tegnes på nytt når språket byttes.
(function () {
  const selV = document.getElementById("velg-virksomhet");
  const selP = document.getElementById("velg-person");
  if ((!selV && !selP) || typeof TESTVIRKSOMHETER === "undefined") return;

  const T = (key) => (window.I18N ? I18N.t(key) : key);
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const navn = (p) => `${p.fornavn} ${p.etternavn}`;
  const lokal = () => (window.I18N && I18N.lang === "nb" ? "nb" : "en");
  const sorter = (a, b) => a.localeCompare(b, lokal());
  // Næringskodens tekst følger språket (engelsk fra SSB KLASS); adresser og navn oversettes ikke
  const naceTekst = (v) => (lokal() === "nb" ? v.naceTekst : v.naceTekstEn || v.naceTekst);

  const perId = {};
  const perFnr = {};
  TESTPERSONER.forEach((p) => { perId[p.id] = p; perFnr[p.fnr] = p; });

  // Tilknytninger: { virksomhet, person, rolle: { type: "ceo" | "sig", detalj } }
  const tilknytninger = [];
  TESTVIRKSOMHETER.forEach((v) => {
    const leder = perFnr[v.dagligLederFnr];
    if (leder) tilknytninger.push({ virksomhet: v, person: leder, rolle: { type: "ceo" } });
    else if (v.dagligLederFnr) tilknytninger.push({ virksomhet: v, person: { ukjent: true, fnr: v.dagligLederFnr }, rolle: { type: "ceo" } });
    (v.signatur.match(/\bN\d+\b/g) || []).forEach((id) => {
      if (perId[id]) tilknytninger.push({ virksomhet: v, person: perId[id], rolle: { type: "sig", detalj: (v.signatur.replace(/\bN\d+\b[,\s]*/g, "").trim() || v.signatur).replace(/^\((.*)\)$/, "$1") } });
    });
  });

  const rolle = (r) => (r.type === "ceo" ? T("r.ceo") : `${T("r.sig")} (${r.detalj})`);

  const options = (liste, verdi, tekst) =>
    `<option value="">${esc(T("sel.choose"))}</option>` + liste.map((x) => `<option value="${esc(verdi(x))}">${esc(tekst(x))}</option>`).join("");

  const personValg = () => options([...TESTPERSONER].sort((a, b) => sorter(navn(a), navn(b))), (p) => p.id, navn);

  const tabell = (kolonner, rader) => rader.length
    ? `<div class="table-wrap"><table><thead><tr>${kolonner.map((k) => `<th>${esc(k)}</th>`).join("")}</tr></thead><tbody>${rader.join("")}</tbody></table></div>`
    : `<p class="hint">${esc(T("r.none"))}</p>`;

  const visVirksomhet = (v) => {
    const knyttet = tilknytninger.filter((t) => t.virksomhet.id === v.id);
    const rader = knyttet.map((t) => t.person.ukjent
      ? `<tr><td><em>${esc(T("r.notinfile"))}</em></td><td>${esc(rolle(t.rolle))}</td><td>–</td><td>${esc(t.person.fnr)}</td></tr>`
      : `<tr><td>${esc(navn(t.person))}</td><td>${esc(rolle(t.rolle))}</td><td>${esc(t.person.fodt)}</td><td>${esc(t.person.fnr)}</td></tr>`);
    return `
      <h2>${esc(v.navn)}</h2>
      <dl class="facts">
        <dt>${esc(T("r.euid"))}</dt><dd>${esc(v.euid)}</dd>
        <dt>${esc(T("r.addr"))}</dt><dd>${esc(v.adresse)}</dd>
        <dt>${esc(T("r.nace"))}</dt><dd>${esc(v.nace)} ${esc(naceTekst(v))}</dd>
        <dt>${esc(T("r.sig"))}</dt><dd>${esc(v.signatur).replace(/\bN\d+\b/g, (id) => (perId[id] ? esc(navn(perId[id])) : id))}</dd>
      </dl>
      <h3 style="margin-top:20px">${esc(T("r.persons"))}</h3>
      ${tabell([T("r.name"), T("r.role"), T("r.dob"), T("r.pid")], rader)}`;
  };

  const visPerson = (p) => {
    const knyttet = tilknytninger.filter((t) => t.person.id === p.id);
    const rader = knyttet.map((t) => `<tr><td>${esc(t.virksomhet.navn)}</td><td>${esc(t.virksomhet.euid)}</td><td>${esc(rolle(t.rolle))}</td></tr>`);
    return `
      <h2>${esc(navn(p))}</h2>
      <dl class="facts">
        <dt>${esc(T("r.dob"))}</dt><dd>${esc(p.fodt)}</dd>
        <dt>${esc(T("p.pob"))}</dt><dd>${esc(p.fodested)}</dd>
        <dt>${esc(T("p.nat"))}</dt><dd>${esc(p.nasjonalitet)}</dd>
        <dt>${esc(T("r.pid"))}</dt><dd>${esc(p.fnr)}</dd>
      </dl>
      <h3 style="margin-top:20px">${esc(T("p.companies"))}</h3>
      ${tabell([T("p.company"), T("r.euid"), T("r.role")], rader)}`;
  };

  // Fyller listen og viser valgt oppføring på nytt (kalles ved oppstart og når språket byttes)
  const koble = (sel, utId, lagListe, finn, vis) => {
    if (!sel) return;
    const ut = document.getElementById(utId);
    const tegn = () => {
      const treff = finn(sel.value);
      ut.hidden = !treff;
      ut.innerHTML = treff ? vis(treff) : "";
    };
    const fyll = () => {
      const valgt = sel.value;
      sel.innerHTML = lagListe();
      sel.value = valgt;
      tegn();
    };
    sel.addEventListener("change", tegn);
    document.addEventListener("langchange", fyll);
    fyll();
  };
  koble(selV, "resultat-virksomhet",
    () => options([...TESTVIRKSOMHETER].sort((a, b) => sorter(a.navn, b.navn)), (v) => v.id, (v) => v.navn),
    (id) => TESTVIRKSOMHETER.find((v) => v.id === id), visVirksomhet);
  koble(selP, "resultat-person", personValg, (id) => perId[id], visPerson);
})();
