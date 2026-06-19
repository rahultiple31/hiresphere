const services = Object.freeze({
  workspace: { label: "Workspace", path: "/workspace/" },
  jobs: { label: "Jobs", path: "/jobs/" },
  projects: { label: "Projects", path: "/projects/" },
  network: { label: "Network", path: "/network/" },
  interview: { label: "Interview", path: "/interview/" },
  profile: { label: "Profile", path: "/profile/" },
  "hr-studio": { label: "HR Studio", path: "/hr-studio/" },
  scale: { label: "Scale", path: "/scale/" }
});

const frame = document.querySelector("#serviceFrame");
const status = document.querySelector("#serviceStatus");
const search = document.querySelector("#globalSearch");

function selectedService() {
  const requested = window.location.hash.slice(1);
  return Object.hasOwn(services, requested) ? requested : "workspace";
}

function navigate() {
  const key = selectedService();
  const service = services[key];
  document.querySelectorAll("[data-service]").forEach((item) => {
    const active = item.dataset.service === key;
    item.classList.toggle("active", active);
    item.setAttribute("aria-current", active ? "page" : "false");
  });
  if (frame.dataset.service !== key) {
    frame.dataset.service = key;
    frame.src = service.path;
  }
  frame.title = `${service.label} service`;
  status.textContent = `${service.label} service`;
  search.value = "";
}

document.querySelector("#navigation").addEventListener("click", (event) => {
  const item = event.target.closest("[data-service]");
  if (item) window.location.hash = item.dataset.service;
});

document.querySelector("#themeToggle").addEventListener("click", () => {
  const dark = document.body.classList.toggle("dark");
  frame.contentWindow?.postMessage({ type: "hiresphere:theme", dark }, window.location.origin);
});

search.addEventListener("input", () => {
  frame.contentWindow?.postMessage({ type: "hiresphere:search", query: search.value }, window.location.origin);
});

frame.addEventListener("load", () => {
  frame.contentWindow?.postMessage({ type: "hiresphere:theme", dark: document.body.classList.contains("dark") }, window.location.origin);
});

window.addEventListener("hashchange", navigate);
navigate();
