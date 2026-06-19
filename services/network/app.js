import { element, setupServiceSearch } from "../shared/runtime.js";
const posts = [
  { name: "Vikram K.", type: "Hiring", body: "Opening 12 cloud-native roles across React, Java, Kafka, and platform security." },
  { name: "Sara P.", type: "Project", body: "Looking for a three-person team to ship a payment reconciliation dashboard." },
  { name: "Rahul M.", type: "Interview", body: "The strongest candidates explain tradeoffs, not just tool names." }
];
const feed = document.querySelector("#feed"); let query = "";
function render() { const visible = posts.filter((post) => `${post.name} ${post.type} ${post.body}`.toLowerCase().includes(query)); feed.replaceChildren(...visible.map((post) => { const card = element("article", "card post"); card.append(element("span", "tag", post.type), element("h2", "", post.name), element("p", "", post.body)); return card; })); }
document.querySelector("#composer").addEventListener("submit", (event) => { event.preventDefault(); const input = document.querySelector("#postText"); const body = input.value.trim(); if (!body) return; posts.unshift({ name: "You", type: document.querySelector("#postType").value, body }); input.value = ""; render(); });
setupServiceSearch((value) => { query = value; render(); }); render();
