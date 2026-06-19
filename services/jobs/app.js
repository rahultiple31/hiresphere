import { element, setupServiceSearch } from "/shared/runtime.js";
const jobs = [
  { id: 1, title: "Senior React + Spring Boot Engineer", company: "CloudNova Systems", location: "Remote", salary: 42, skills: ["React", "Spring Boot", "Kafka"], match: 96 },
  { id: 2, title: "DevOps Platform Lead", company: "FinGrid Labs", location: "Bengaluru", salary: 58, skills: ["Kubernetes", "Terraform", "AWS"], match: 91 },
  { id: 3, title: "AI Resume Matching Engineer", company: "TalentWorks AI", location: "Pune", salary: 30, skills: ["Python", "NLP", "Search"], match: 89 },
  { id: 4, title: "Full Stack Marketplace Developer", company: "ScaleBridge", location: "Hyderabad", salary: 18, skills: ["Node.js", "React", "Payments"], match: 78 }
];
const state = { saved: new Set(), applied: new Set() };
const results = document.querySelector("#results");
function render() {
  const local = document.querySelector("#keyword").value.toLowerCase();
  const location = document.querySelector("#location").value;
  const salary = Number(document.querySelector("#salary").value || 0);
  const filtered = jobs.filter((job) => `${job.title} ${job.company} ${job.location} ${job.skills.join(" ")}`.toLowerCase().includes(local) && (!location || job.location === location) && job.salary >= salary);
  results.replaceChildren(...filtered.map((job) => {
    const card = element("article", "card");
    const header = element("header"); header.append(element("h2", "", job.title), element("span", "status", `${job.match}% match`));
    card.append(header, element("p", "muted", `${job.company} · ${job.location} · ${job.salary} LPA`));
    const tags = element("div", "tags"); job.skills.forEach((skill) => tags.append(element("span", "tag", skill))); card.append(tags);
    const actions = element("div", "actions");
    [["apply", state.applied, "Apply", "Applied"], ["save", state.saved, "Save", "Saved"]].forEach(([action, set, idle, done]) => { const button = element("button", action === "save" ? "secondary" : "", set.has(job.id) ? done : idle); button.addEventListener("click", () => { set.add(job.id); render(); }); actions.append(button); });
    card.append(actions); return card;
  }));
  if (!filtered.length) results.append(element("p", "notice", "No jobs match these filters."));
}
document.querySelectorAll("#keyword,#location,#salary").forEach((input) => input.addEventListener("input", render));
setupServiceSearch((query) => { document.querySelector("#keyword").value = query; render(); }); render();
