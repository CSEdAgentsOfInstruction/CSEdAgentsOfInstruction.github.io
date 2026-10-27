This page contains resources for the [SIGCSE-Virtual 2026](https://sigcsevirtual2026.acm.org/) workshop "Agents of Instruction: Co-Creating Learning Materials with AI Agents"

This page is created and maintained by the workshop facilitators:

* [Lisa Zhang, University of Toronto](https://lisazhang.ca/)
* [Juho Leinonen, Aalto University](https://juholeinonen.com/)
* [Arto Hellas, Aalto University](https://www.aalto.fi/en/people/arto-hellas)
* [Paul Denny, University of Auckland](https://www.cs.auckland.ac.nz/~paul/)

> [!CAUTION]
> This page is a work in progress!

AI agents are increasingly used by professional software developers to support tasks such as planning, coding, debugging, refactoring, and drafting documentation. Unlike basic chat models, AI agents work more autonomously toward a broader goal: breaking tasks into steps, taking actions, using tools, and iterating on their own output. Based on our experiences, similar agent-based workflows can be used to assist educators in generating and refining learning materials. 

In this hands-on tutorial, we will introduce participants to practical ways of using AI agents to support the development of computing education resources, including lecture slides, online textbook materials, programming exercises, explanations, analogies, and visualizations. We will compare different types of tools, including general-purpose AI systems and coding-focused agentic tools, and discuss when each may be useful for educational material generation.  Participants will explore agent-based workflows through hands-on activities in which they create, revise, and adapt learning materials for their own teaching contexts. Throughout the tutorial, we will emphasize both the opportunities and limitations of these tools. We will also discuss ethical and practical issues, including copyright, citations, attribution, transparency, and responsible use. Drawing on the organizers’ experiences, the tutorial will provide participants with concrete workflows, examples, and strategies for incorporating AI agents into the creation of learning materials in computing education.

## Setup Instructions for Attendees

For attendees of the workshop, you will need to prepare three things ahead of time
to get the most out of the workshop:

1. Installation of an AI Coding Assistant of your choice.
   The workshop facilitators each have their own favourite:

    - [Github Copilot Pro](https://github.com/features/copilot) is available for
      University faculty members for free as part of the [Github Education](https://github.com/education)
      program. However, your faculty status will need to be verified manually, which can take some time.
      Paid membership is USD$10/month[^1]
    - [Anthropic Claude Code Pro](https://claude.com/pricing) is USD$23/month,
      and is a good choice if you prefer a terminal-based workflow, or if you
      want to set it up yourself on VSCode.
      Claude Design is included in the free tier if your goal is to create
      visualizations for your courses.
    - [Cursor Pro](https://cursor.com/pricing) also has a free tier for getting started.
      It is a good choice if you don't mind using their IDE (built on top of 
      VS Code), or if your workflow may include making (human) edits on a file
      concurrently with an AI Agent.

2. Access to a machine or virtual machine to install the AI Coding Assistant.

    - It is good practice to install AI Coding Assistants in a virtual machine,
      and avoid [working](https://www.eweek.com/news/replit-ai-coding-assistant-failure/)
      with [sensitive files](https://www.lawcommentary.com/articles/openai-navier-stokes-ai-research-dispute).
      Issues arising from these agents not respecting permissions are rare,
      but [not](https://incidentdatabase.ai/entities/gemini-3-based-antigravity-agent-ide/)
      [unheard](https://rits.shanghai.nyu.edu/ai/metas-alignment-director-lost-control-of-openclaw-it-deleted-her-inbox/)
      [of](https://www.theregister.com/software/2025/05/29/openai-model-modifies-own-shutdown-script-say-researchers/917237).
    - Our [agent sandbox guide](agent-sandbox-guide.md) shows a lighter option: running the agent in a Docker container, where it can only change files you copy into it. Please set it up before the workshop.

3. Source files for you to adapt or work on during the workshop. You will get the most
   out of the workshop by working on instructional materials that you may consider
   actually using in your classroom. Some suggestions of what you could prepare include:

    - Past slides for a CS1 course that you might want to write into a textbook.
    - Descriptions of visualizations that you might want to create for a data structures course.
    - Assignment questions for an upper-level CS course that you want to personalize or adapt based on student interests.

[^1]: as of October 2026.

### Installation of Coding Assistants

#### Github Copilot Setup Instructions

1. [Access Copilot Pro for free as a teacher or open source maintainer](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-teachers-and-os-maintainers)
    You should do this a week prior to the workshop

#### Cursor Setup Instructions

TODO. This could be a reasonable alternative to Github Copilot,
given that the free tier is there.

### VM and Security

The [agent sandbox guide](agent-sandbox-guide.md) has step-by-step instructions for running GitHub Copilot, Claude Code or Codex in a Docker container, and explains what this setup does and doesn't protect against.

### Preparing Source Files

Put our suggested source files here too?

## Workshop Resources

Slides and other materials used for the workshop will be posted here.


<style>
  blockquote.md-alert {
    padding: .5rem 1rem !important;
    margin: 0 0 1rem !important;
    color: inherit !important;
    background: none !important;
    border: 0 !important;
    border-left: .25em solid var(--md-alert-color) !important;
    border-radius: 0 !important;
    font-style: normal !important;
  }
  blockquote.md-alert > :first-child { margin-top: 0; }
  blockquote.md-alert > :last-child  { margin-bottom: 0; }
  blockquote.md-alert .md-alert-title {
    display: flex; align-items: center; gap: .5rem;
    margin-bottom: .5rem !important;
    font-weight: 500; line-height: 1;
    color: var(--md-alert-color) !important;
  }
  blockquote.md-alert .md-alert-title svg { fill: currentColor; flex-shrink: 0; }
  .md-alert-note      { --md-alert-color: #0969da; }
  .md-alert-tip       { --md-alert-color: #1a7f37; }
  .md-alert-important { --md-alert-color: #8250df; }
  .md-alert-warning   { --md-alert-color: #9a6700; }
  .md-alert-caution   { --md-alert-color: #d1242f; }
</style>
<script>
document.addEventListener("DOMContentLoaded", () => {
  const icons = {
    note: 'M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z',
    tip: 'M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8.456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.750 2.5 6.766 2.5 5.25 2.5 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.516-.701 2.5-1.328 3.259-.095.115-.184.22-.268.319-.207.245-.383.453-.541.681-.208.3-.33.565-.37.847a.751.751 0 0 1-1.485-.212c.084-.593.337-1.078.621-1.489.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.679.985-1.32.985-2.304 0-2.060-1.637-3.75-4-3.75ZM5.75 12h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM6 15.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Z',
    important: 'M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v9.5A1.75 1.75 0 0 1 14.25 13H8.06l-2.573 2.573A1.458 1.458 0 0 1 3 14.543V13H1.75A1.75 1.75 0 0 1 0 11.25Zm1.75-.25a.25.25 0 0 0-.25.25v9.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h6.5a.25.25 0 0 0 .25-.25v-9.5a.25.25 0 0 0-.25-.25Zm7 2.25v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 9a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z',
    warning: 'M6.457 1.047c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0 1 14.082 15H1.918a1.75 1.75 0 0 1-1.543-2.575Zm1.763.707a.25.25 0 0 0-.44 0L1.698 13.132a.25.25 0 0 0 .22.368h12.164a.25.25 0 0 0 .22-.368Zm.53 3.996v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z',
    caution: 'M4.47.22A.749.749 0 0 1 5 0h6c.199 0 .389.079.53.22l4.25 4.25c.141.14.22.331.22.53v6a.749.749 0 0 1-.22.53l-4.25 4.25A.749.749 0 0 1 11 16H5a.749.749 0 0 1-.53-.22L.22 11.53A.749.749 0 0 1 0 11V5c0-.199.079-.389.22-.53Zm.84 1.28L1.5 5.31v5.38l3.81 3.81h5.38l3.81-3.81V5.31L10.69 1.5ZM8 4a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 8 4Zm0 8a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z'
  };
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
    title.innerHTML = '<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="' + icons[type] + '"></path></svg>' +
      type[0].toUpperCase() + type.slice(1);
    bq.prepend(title);
  });
});
</script>
