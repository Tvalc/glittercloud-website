const KEY = "hazel-board-v1";

const DAYS = [
  { id: "mon", label: "Monday" },
  { id: "tue", label: "Tuesday" },
  { id: "wed", label: "Wednesday" },
  { id: "thu", label: "Thursday" },
  { id: "fri", label: "Friday" },
];

const $ = (sel) => document.querySelector(sel);

let memoryOnly = false;
let state = load();

function uid() {
  return Math.random().toString(36).slice(2, 10);
}

function todayISO() {
  const d = new Date();
  const z = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${z(d.getMonth() + 1)}-${z(d.getDate())}`;
}

function humanitiesBlock(day) {
  return { id: uid(), day, name: "Humanities", time: "", anchor: true };
}

function seed() {
  return {
    choice: "",
    className: "",
    why: "",
    agreedSig: "",
    todayDate: "",
    todayStatus: "",
    blocks: DAYS.map((d) => humanitiesBlock(d.id)),
    safe: [],
  };
}

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return seed();
    const data = JSON.parse(raw);
    if (!data || !Array.isArray(data.blocks) || !Array.isArray(data.safe)) return seed();
    return data;
  } catch {
    memoryOnly = true;
    return seed();
  }
}

function save() {
  if (memoryOnly) return;
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
  } catch {
    memoryOnly = true;
    const note = $("#save-note");
    if (note) note.textContent = "This browser is not keeping a copy. You can still print the schedule.";
  }
}

function signature() {
  return JSON.stringify({
    choice: state.choice,
    className: state.choice === "class" ? state.className.trim() : "",
    blocks: state.blocks.map((b) => ({
      day: b.day,
      name: b.name.trim(),
      time: b.time.trim(),
      anchor: !!b.anchor,
    })),
  });
}

function isAgreed() {
  return !!state.agreedSig && state.agreedSig === signature();
}

function currentToday() {
  if (state.todayDate !== todayISO()) return "";
  return state.todayStatus || "";
}

function dayBlocks(day) {
  return state.blocks.filter((b) => b.day === day);
}

function paintChoice(focusClass) {
  const morning = state.choice === "morning";
  const klass = state.choice === "class";
  $("#pick-morning").setAttribute("aria-pressed", morning ? "true" : "false");
  $("#pick-class").setAttribute("aria-pressed", klass ? "true" : "false");
  const field = $("#class-field");
  field.hidden = !klass;
  $("#class-name").value = state.className || "";
  if (focusClass && klass) $("#class-name").focus();
  updatePrintLine();
}

function updatePrintLine() {
  const el = $("#print-choice");
  if (state.choice === "morning") el.textContent = "Plan: go in the morning.";
  else if (state.choice === "class") {
    const name = state.className.trim();
    el.textContent = name ? `Plan: go to ${name}.` : "Plan: go to the class I pick.";
  } else el.textContent = "Plan: not chosen yet.";
}

function updateAgree() {
  const on = isAgreed();
  $("#agreed").checked = on;
  $("#agree-note").textContent = on ? "Agreed." : "Not agreed yet.";
}

function updateToday() {
  const status = currentToday();
  $("#today-date").textContent = new Date().toLocaleDateString(undefined, {
    weekday: "long",
    month: "long",
    day: "numeric",
  });
  $("#today-with").setAttribute("aria-pressed", status === "with" ? "true" : "false");
  $("#today-home").setAttribute("aria-pressed", status === "home" ? "true" : "false");
  let line = "Today is not marked yet.";
  if (status === "with") line = "Today goes with the schedule.";
  if (status === "home") line = "Home is the plan for today.";
  if (status === "with" && !isAgreed()) line += " The schedule is not agreed yet.";
  $("#today-line").textContent = line;
}

function setToday(status) {
  const current = currentToday();
  state.todayDate = todayISO();
  state.todayStatus = current === status ? "" : status;
  save();
  updateToday();
}

function renderWeek() {
  const week = $("#week");
  week.replaceChildren();
  for (const day of DAYS) {
    const blocks = dayBlocks(day.id);
    const section = document.createElement("section");
    section.className = "day";
    const heading = document.createElement("h3");
    heading.textContent = day.label;
    section.append(heading);

    const list = document.createElement("ul");
    list.className = "slips";
    blocks.forEach((block, index) => {
      list.append(slip(block, day.label, index, blocks.length));
    });
    section.append(list);

    const add = document.createElement("button");
    add.type = "button";
    add.className = "ghost add-class no-print";
    add.textContent = "Add a class";
    add.addEventListener("click", () => addBlock(day.id));
    section.append(add);
    week.append(section);
  }
}

function slip(block, dayLabel, index, count) {
  const item = document.createElement("li");
  item.className = "slip";
  item.dataset.id = block.id;

  const top = document.createElement("div");
  top.className = "slip-top";

  const time = document.createElement("input");
  time.className = "time";
  time.type = "text";
  time.maxLength = 20;
  time.autocomplete = "off";
  time.placeholder = "Time";
  time.setAttribute("aria-label", `Time on ${dayLabel}`);
  time.value = block.time;
  time.addEventListener("input", () => {
    block.time = time.value;
    save();
    updateAgree();
    updateToday();
  });
  top.append(time);

  if (block.anchor) {
    const badge = document.createElement("span");
    badge.className = "badge";
    badge.textContent = "Every day";
    top.append(badge);
  }

  const name = document.createElement("input");
  name.type = "text";
  name.maxLength = 80;
  name.autocomplete = "off";
  name.placeholder = "Class";
  name.setAttribute("aria-label", `Class on ${dayLabel}`);
  name.value = block.name;
  name.addEventListener("input", () => {
    block.name = name.value;
    save();
    updateAgree();
    updateToday();
  });

  const actions = document.createElement("div");
  actions.className = "slip-actions no-print";
  actions.append(
    iconButton("Up", "Move up", index === 0, () => move(block.id, -1)),
    iconButton("Down", "Move down", index === count - 1, () => move(block.id, 1)),
    iconButton("Remove", `Remove ${block.name || "class"}`, false, () => removeBlock(block.id)),
  );

  item.append(top, name, actions);
  return item;
}

function iconButton(label, aria, disabled, onClick) {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = label;
  button.setAttribute("aria-label", aria);
  button.disabled = disabled;
  button.addEventListener("click", onClick);
  return button;
}

function addBlock(day) {
  const block = { id: uid(), day, name: "", time: "", anchor: false };
  state.blocks.push(block);
  save();
  updateAgree();
  renderWeek();
  const field = document.querySelector(`[data-id="${block.id}"] input[placeholder="Class"]`);
  if (field) field.focus();
}

function removeBlock(id) {
  state.blocks = state.blocks.filter((b) => b.id !== id);
  save();
  updateAgree();
  updateToday();
  renderWeek();
}

function move(id, dir) {
  const block = state.blocks.find((b) => b.id === id);
  if (!block) return;
  const siblings = dayBlocks(block.day);
  const index = siblings.findIndex((b) => b.id === id);
  const other = siblings[index + dir];
  if (!other) return;
  const i = state.blocks.indexOf(block);
  const j = state.blocks.indexOf(other);
  [state.blocks[i], state.blocks[j]] = [state.blocks[j], state.blocks[i]];
  save();
  updateAgree();
  renderWeek();
}

function addHumanities() {
  let added = false;
  for (const day of DAYS) {
    if (!state.blocks.some((b) => b.day === day.id && b.anchor)) {
      state.blocks.push(humanitiesBlock(day.id));
      added = true;
    }
  }
  if (!added) {
    $("#add-humanities").textContent = "Humanities is already on every day";
    return;
  }
  $("#add-humanities").textContent = "Put Humanities on every day";
  save();
  updateAgree();
  renderWeek();
}

function renderSafe() {
  const list = $("#safe");
  list.replaceChildren();
  if (state.safe.length === 0) {
    const empty = document.createElement("li");
    empty.className = "empty";
    empty.textContent = "Nothing here yet.";
    list.append(empty);
    return;
  }
  for (const card of state.safe) {
    list.append(safeCard(card));
  }
}

function safeCard(card) {
  const item = document.createElement("li");
  item.className = `safe-card ${card.kind}`;
  item.dataset.id = card.id;

  const kind = document.createElement("p");
  kind.className = "kind";
  kind.textContent = card.kind === "person" ? "Person" : "Place";

  const name = document.createElement("input");
  name.type = "text";
  name.maxLength = 80;
  name.autocomplete = "off";
  name.placeholder = card.kind === "person" ? "Who" : "Where";
  name.setAttribute("aria-label", card.kind === "person" ? "Person" : "Place");
  name.value = card.name;
  name.addEventListener("input", () => {
    card.name = name.value;
    save();
  });

  const note = document.createElement("input");
  note.type = "text";
  note.maxLength = 160;
  note.autocomplete = "off";
  note.placeholder = "Optional note";
  note.setAttribute("aria-label", "Note");
  note.value = card.note;
  note.addEventListener("input", () => {
    card.note = note.value;
    save();
  });

  const remove = document.createElement("button");
  remove.type = "button";
  remove.textContent = "Remove";
  remove.addEventListener("click", () => {
    state.safe = state.safe.filter((s) => s.id !== card.id);
    save();
    renderSafe();
  });

  item.append(kind, name, note, remove);
  return item;
}

function addSafe(kind) {
  const card = { id: uid(), kind, name: "", note: "" };
  state.safe.push(card);
  save();
  renderSafe();
  const field = document.querySelector(`[data-id="${CSS.escape(card.id)}"] input`);
  if (field) field.focus();
}

function bind() {
  $("#pick-morning").addEventListener("click", () => {
    state.choice = state.choice === "morning" ? "" : "morning";
    save();
    paintChoice(false);
    updateAgree();
    updateToday();
  });
  $("#pick-class").addEventListener("click", () => {
    state.choice = state.choice === "class" ? "" : "class";
    save();
    paintChoice(state.choice === "class");
    updateAgree();
    updateToday();
  });
  $("#class-name").addEventListener("input", (event) => {
    state.className = event.target.value;
    save();
    updatePrintLine();
    updateAgree();
    updateToday();
  });
  $("#today-with").addEventListener("click", () => setToday("with"));
  $("#today-home").addEventListener("click", () => setToday("home"));
  $("#agreed").addEventListener("change", (event) => {
    state.agreedSig = event.target.checked ? signature() : "";
    save();
    updateAgree();
    updateToday();
  });
  $("#add-humanities").addEventListener("click", addHumanities);
  $("#add-place").addEventListener("click", () => addSafe("place"));
  $("#add-person").addEventListener("click", () => addSafe("person"));
  $("#why").addEventListener("input", (event) => {
    state.why = event.target.value;
    save();
  });
  $("#print").addEventListener("click", () => window.print());
}

$("#why").value = state.why || "";
if (memoryOnly) {
  $("#save-note").textContent = "This browser is not keeping a copy. You can still print the schedule.";
}
bind();
paintChoice(false);
updateAgree();
updateToday();
renderWeek();
renderSafe();
