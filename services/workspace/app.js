import { setupServiceSearch } from "/shared/runtime.js";
setupServiceSearch((query) => document.querySelectorAll(".searchable").forEach((card) => card.classList.toggle("hidden", query && !card.textContent.toLowerCase().includes(query))));
