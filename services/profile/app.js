import { element, setupServiceSearch } from "/shared/runtime.js";
document.querySelectorAll("[data-kind]").forEach((input) => input.addEventListener("change", () => { if (!input.files.length) return; document.querySelector("#uploads").prepend(element("p", "notice", `${input.dataset.kind}: ${input.files.length} file(s) queued`)); }));
document.querySelector("#save").addEventListener("click", () => document.querySelector("#saved").classList.remove("hidden"));
setupServiceSearch((query) => document.querySelectorAll(".searchable").forEach((item) => item.classList.toggle("hidden", query && !item.textContent.toLowerCase().includes(query))));
