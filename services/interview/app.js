import { element, setupServiceSearch } from "../shared/runtime.js";
const duration = 20 * 60; let remaining = duration; let handle = null;
const timer = document.querySelector("#timer"); const recording = document.querySelector("#recording");
function display() { timer.textContent = `${String(Math.floor(remaining / 60)).padStart(2, "0")}:${String(remaining % 60).padStart(2, "0")}`; }
function stop(message) { clearInterval(handle); handle = null; recording.textContent = message; }
document.querySelector("#start").addEventListener("click", () => { if (handle) return; if (remaining <= 0 || recording.textContent === "Saved") remaining = duration; display(); recording.textContent = "Recording"; handle = setInterval(() => { remaining = Math.max(0, remaining - 1); display(); if (!remaining) stop("Saved automatically"); }, 1000); });
document.querySelector("#end").addEventListener("click", () => stop("Saved"));
for (const id of ["camera", "microphone"]) document.querySelector(`#${id}`).addEventListener("click", (event) => { const on = event.currentTarget.textContent.endsWith("on"); event.currentTarget.textContent = `${id === "camera" ? "Camera" : "Mic"} ${on ? "off" : "on"}`; });
document.querySelector("#chat").addEventListener("submit", (event) => { event.preventDefault(); const input = document.querySelector("#message"); const message = input.value.trim(); if (!message) return; document.querySelector("#messages").append(element("p", "notice", `You: ${message}`)); input.value = ""; });
document.querySelector("#score").addEventListener("input", (event) => { document.querySelector("#scoreOutput").value = event.target.value; }); setupServiceSearch(() => {}); display();
