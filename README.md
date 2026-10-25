# Agents of Instruction: Co-Creating Learning Materials with AI Agents

This page contains resources for the [SIGCSE-Virtual 2026](https://sigcsevirtual2026.acm.org/) workshop "Agents of Instruction: Co-Creating Learning Materials with AI Agents"

This page is created and maintainted by:

* [Lisa Zhang, University of Toronto](https://lisazhang.ca/)
* [Juho Leinonen, Aalto University](https://juholeinonen.com/)
* [Arto Hellas, Aalto University](https://www.aalto.fi/en/people/arto-hellas)
* [Paul Denny, University of Auckland](https://www.cs.auckland.ac.nz/~paul/)

> [!CAUTION]
> This page is a work in progress!

<!-- to get alerts to render on the html page -->
<style>
  .md-alert { padding: .5rem 1rem; margin: 1rem 0; border-left: .25em solid; border-radius: 4px; }
  .md-alert-title { font-weight: 600; margin: 0 0 .25rem; }
  .md-alert-note      { border-color: #0969da; background: #ddf4ff; }
  .md-alert-tip       { border-color: #1a7f37; background: #dafbe1; }
  .md-alert-important { border-color: #8250df; background: #fbefff; }
  .md-alert-warning   { border-color: #9a6700; background: #fff8c5; }
  .md-alert-caution   { border-color: #cf222e; background: #ffebe9; }
</style>
<script>
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("blockquote").forEach(bq => {
    const p = bq.querySelector("p");
    if (!p) return;
    const m = p.innerHTML.match(/^\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(<br\s*\/?>)?\s*/i);
    if (!m) return;
    const type = m[1].toLowerCase();
    p.innerHTML = p.innerHTML.slice(m[0].length);
    if (!p.innerHTML.trim()) p.remove();
    bq.classList.add("md-alert", "md-alert-" + type);
    const title = document.createElement("p");
    title.className = "md-alert-title";
    title.textContent = type[0].toUpperCase() + type.slice(1);
    bq.prepend(title);
  });
});
</script>

## Workshop Abstract

AI agents are increasingly used by professional software developers to support tasks such as planning, coding, debugging, refactoring, and drafting documentation. Unlike basic chat models, AI agents work more autonomously toward a broader goal: breaking tasks into steps, taking actions, using tools, and iterating on their own output. Based on our experiences, similar agent-based workflows can be used to assist educators in generating and refining learning materials. 

In this hands-on tutorial, we will introduce participants to practical ways of using AI agents to support the development of computing education resources, including lecture slides, online textbook materials, programming exercises, explanations, analogies, and visualizations. We will compare different types of tools, including general-purpose AI systems and coding-focused agentic tools, and discuss when each may be useful for educational material generation.  Participants will explore agent-based workflows through hands-on activities in which they create, revise, and adapt learning materials for their own teaching contexts. Throughout the tutorial, we will emphasize both the opportunities and limitations of these tools. We will also discuss ethical and practical issues, including copyright, citations, attribution, transparency, and responsible use. Drawing on the organizers’ experiences, the tutorial will provide participants with concrete workflows, examples, and strategies for incorporating AI agents into the creation of learning materials in computing education.










