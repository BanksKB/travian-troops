const form = document.querySelector("#filter");
const field = form.elements.namedItem("field");
const query = form.elements.namedItem("q");
const quickFilter = document.querySelector("#quick-filter");
const status = document.querySelector("#status");
const downloads = document.querySelector("#downloads");
const headings = document.querySelector("#units thead tr");
const body = document.querySelector("#units tbody");
let currentRequest;

async function loadUnits(presetField) {
  currentRequest?.abort();
  const request = new AbortController();
  currentRequest = request;
  const parameters = new URLSearchParams(new FormData(form));
  if (presetField) parameters.set("field", presetField);
  status.textContent = "Učitavanje jedinica…";
  downloads.hidden = true;

  try {
    const response = await fetch(`/api/units?${parameters}`, { signal: request.signal });
    if (!response.ok) {
      const problem = await response.json().catch(() => null);
      throw new Error(problem?.error || "Dohvat jedinica nije uspio.");
    }
    const { fields, units } = await response.json();
    if (request.signal.aborted) return;
    const keys = Object.keys(fields);

    if (field.options.length === 1) {
      for (const key of keys) field.add(new Option(fields[key], key));
      if (presetField) field.value = presetField;
      for (const key of keys) {
        const heading = document.createElement("th");
        heading.scope = "col";
        heading.textContent = fields[key];
        headings.append(heading);
      }
    }

    const rows = units.map(unit => {
      const row = document.createElement("tr");
      for (const key of keys) {
        const cell = row.insertCell();
        const value = unit[key];
        cell.textContent = value ?? "—";
        if (typeof value === "number") cell.className = "numeric";
      }
      return row;
    });
    body.replaceChildren(...rows);
    status.textContent = units.length ? `Broj zapisa: ${units.length}` : "Nema rezultata za zadani filtar.";
    for (const format of ["csv", "json"]) {
      parameters.set("format", format);
      document.getElementById(format).href = `/api/units?${parameters}`;
    }
    downloads.hidden = false;
  } catch (error) {
    if (request.signal.aborted) return;
    body.replaceChildren();
    status.textContent = error.message;
  }
}

form.addEventListener("submit", event => {
  event.preventDefault();
  loadUnits();
});
quickFilter.addEventListener("change", () => {
  const option = quickFilter.selectedOptions[0];
  if (option.value === "manual") return;
  query.value = option.value;
  const presetField = option.dataset.field ?? "all";
  if (Array.from(field.options).some(item => item.value === presetField)) {
    field.value = presetField;
  }
  loadUnits(presetField);
});
function showManualFilter() {
  quickFilter.value = query.value.trim() || field.value !== "all" ? "manual" : "";
}
query.addEventListener("input", showManualFilter);
field.addEventListener("change", showManualFilter);
form.addEventListener("reset", () => setTimeout(loadUnits, 0));
loadUnits();

async function loadTrainingLevels() {
  const select = document.querySelector("#training-building");
  const table = document.querySelector("#training-levels");
  const message = document.querySelector("#training-status");
  message.textContent = "Učitavanje razina treninga…";

  try {
    const response = await fetch("/api/training-levels");
    if (!response.ok) {
      const problem = await response.json().catch(() => null);
      throw new Error(problem?.error || "Dohvat razina nije uspio.");
    }
    const levels = await response.json();
    if (!levels.length) throw new Error("Nema razina treninga.");
    const percent = new Intl.NumberFormat("hr-HR", { maximumFractionDigits: 2 });

    function renderLevels() {
      const rows = levels.filter(level => level.zgrada === select.value).map(level => {
        const row = document.createElement("tr");
        row.insertCell().textContent = level.razina;
        row.insertCell().textContent = percent.format(level.trajanje) + " %";
        row.insertCell().textContent = percent.format(level.smanjenje) + " %";
        return row;
      });
      table.tBodies[0].replaceChildren(...rows);
    }

    for (const building of new Set(levels.map(level => level.zgrada))) {
      select.add(new Option(building, building));
    }
    select.addEventListener("change", renderLevels);
    renderLevels();
    select.disabled = false;
    table.hidden = false;
    message.textContent = "";
  } catch (error) {
    message.textContent = error.message;
  }
}

loadTrainingLevels();
