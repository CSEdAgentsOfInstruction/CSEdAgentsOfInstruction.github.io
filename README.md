This page contains resources for the [SIGCSE-Virtual 2026](https://sigcsevirtual2026.acm.org/) workshop "Agents of Instruction: Co-Creating Learning Materials with AI Agents"

This page is created and maintained by the workshop facilitators:

* [Lisa Zhang, University of Toronto](https://lisazhang.ca/)
* [Juho Leinonen, Aalto University](https://juholeinonen.com/)
* [Arto Hellas, Aalto University](https://www.aalto.fi/en/people/arto-hellas)
* [Paul Denny, University of Auckland](https://www.cs.auckland.ac.nz/~paul/)

> **Caution:** This page is a work in progress!

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
    - [Cursor](https://cursor.com/pricing) also has a free plan for getting started.
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

You will need a GitHub account. Complete these steps before the workshop:

1. Choose a plan:
    - Teachers and open source maintainers may be eligible for [Copilot Pro at no cost](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-teachers-and-os-maintainers). Apply at least a week before the workshop, as verification can take time.
    - Alternatively, [sign up for GitHub Copilot](https://github.com/github-copilot/free_signup) on the free plan.
2. Choose how you will use Copilot:
    - For the recommended Docker sandbox setup, install VS Code and the [GitHub Copilot extension](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/set-up-copilot/install-copilot-extension?tool=vscode).
    - For a terminal-based workflow, [install the Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli).
    You only need one of these options unless you would like to use both.
3. Sign in to GitHub in your chosen tool and confirm that Copilot responds to a test prompt.

If you are using the Docker sandbox, follow the [agent sandbox guide](agent-sandbox-guide.md) to complete the remaining setup.

Of course, you are welcome to set up a different AI Agent.
[Cursor](https://cursor.com/pricing) also has a free tier that requires no credit card,
however you may exceed usage limits during the workshop.
For the Cursor editor, download the app from [cursor.com/download](https://cursor.com/download)
For a terminal-based workflow, [install the Cursor CLI](https://cursor.com/docs/cli/installation) and start it with `agent`.
You only need one of these options.

### VM and Security

The [agent sandbox guide](agent-sandbox-guide.md) has step-by-step instructions for running GitHub Copilot, Claude Code or Codex in a Docker container, and explains what this setup does and doesn't protect against. Cursor is a separate application, so the guide does not cover it.

### Preparing Source Files

If you would like ready-to-use materials, use our **Introduction to Programming workshop edition**, adapted from parts 1–3 of [Aalto OpenCS Introduction to Programming](https://opencs.aalto.fi/en/courses/introduction-to-programming):

- [Open the course in your browser](example-materials/python-demo/) — no installation needed.
- [Download the editable source ZIP](example-materials/python-cs1.zip) — 26 lessons, 70 MCQs, and 73 Python exercises from parts 1–3, with tests and reference solutions.

To work on the materials with your coding agent, unzip the project and open the `python-cs1` folder in your editor. Install Node.js LTS (24 or later), then run `npm ci` followed by `npm run dev` in that folder. Open the local URL printed in the terminal. Python runs in the browser; no local Python installation or course platform is needed. The ZIP includes setup instructions and an authoring guide with example agent prompts.

## Workshop Resources

Slides and other materials used for the workshop will be posted here.
