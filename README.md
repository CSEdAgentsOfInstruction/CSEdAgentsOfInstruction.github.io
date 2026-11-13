This page contains resources for the [SIGCSE-Virtual 2026](https://sigcsevirtual2026.acm.org/) workshop "Agents of Instruction: Co-Creating Learning Materials with AI Agents"

This page is created and maintained by the workshop facilitators:

* [Lisa Zhang, University of Toronto](https://lisazhang.ca/)
* [Juho Leinonen, Aalto University](https://juholeinonen.com/)
* [Arto Hellas, Aalto University](https://www.aalto.fi/en/people/arto-hellas)
* [Paul Denny, University of Auckland](https://www.cs.auckland.ac.nz/~paul/)

> **Caution:** This page is a work in progress!

AI agents are increasingly used by professional software developers to support tasks such as planning, coding, debugging, refactoring, and drafting documentation. Unlike basic chat models, AI agents work more autonomously toward a broader goal: breaking tasks into steps, taking actions, using tools, and iterating on their own output. Based on our experiences, similar agent-based workflows can be used to assist educators in generating and refining learning materials. 

In this hands-on tutorial, we will introduce participants to practical ways of using AI agents to support the development of computing education resources, including lecture slides, online textbook materials, programming exercises, explanations, analogies, and visualizations. We will compare different types of tools, including general-purpose AI systems and coding-focused agentic tools, and discuss when each may be useful for educational material generation.  Participants will explore agent-based workflows through hands-on activities in which they create, revise, and adapt learning materials for their own teaching contexts. Throughout the tutorial, we will emphasize both the opportunities and limitations of these tools. We will also discuss ethical and practical issues, including copyright, citations, attribution, transparency, and responsible use. Drawing on the organizers’ experiences, the tutorial will provide participants with concrete workflows, examples, and strategies for incorporating AI agents into the creation of learning materials in computing education.

**Content**

* TOC
{:toc}

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

## Activities

There will be two activities during the tutorial: 

1. Initial creation of educational materials: Set up. Finding base/source materials to use
   (or use the one provided by the facilitators, below), and generating an initial draft of
   a target education materials.
2. "Co-creation". Setting up the feedback loop, interactions with the GenAI tool.
   Creating and revising learning materials with AI agents.

We encourage you to start with some source materials to adapt, so that resources that the
agents generate can be grounded in these materials. We also encourage you to work with your
own materials---though that also depends on your comfort level in having these materials 
sent to external servers, possibly used for training.

Also, these are quite broad instructions, and you can create a range of different kinds
of educational materials! Consider any of the following:

- Generating initial set of slides (e.g., using [Quarto](https://quarto.org/), which requires installation) grounded in readings.
- Generate an initial set of notes based on your existing slides.
- Having the AI Agent "fact check" a set of notes, or suggest ideas to revise these notes.
- Generate or adapt exercises, multiple-choice questions, or Parsons problems.
- Produce an interactive visualization for a specific concept.
- Adapt resources from one format to another (e.g., pull out all the exercises in
  a set of slides/resources into a single webpage).

Since time will be limited during the tutorial, we encourage you to focus on one
small thing: e.g., a small number of slides, a single visualization, or variants to
a single problem. 
It's important to keep your pedagogical rationale forefront in these exercises.

### CS1 Source Files (from Arto & Juho)

If you prefer to start with some ready-to-use materials (instead of your own),
you can use Arto & Juho's **Introduction to Programming workshop edition**,
adapted from parts 1–3 of
[Aalto OpenCS Introduction to Programming](https://opencs.aalto.fi/en/courses/introduction-to-programming):

- [Open the course in your browser](example-materials/python-demo/) — no installation needed.
- [Download the editable source ZIP]([example-materials/python-cs1.zip](https://github.com/CSEdAgentsOfInstruction/CSEdAgentsOfInstruction.github.io/raw/refs/heads/main/example-materials/python-cs1.zip)) — 26 lessons, 70 MCQs, and 73 Python exercises from parts 1–3, with tests and reference solutions.

To work on the materials with your coding agent,
unzip the project and open the `python-cs1` folder in your editor.
You can also clone the repository
`https://github.com/CSEdAgentsOfInstruction/CSEdAgentsOfInstruction.github.io/`, which
contains the materials in the `example-materials/python-cs1` subfolder.
Run your coding agent in this folder, so that it has access to 
the content in the subfolders.

This part is not necessary, but if you would like to run the webpage demo locally 
(like what you see in [here](example-materials/python-demo/), 
you will need to install Node.js LTS (24 or later).
- For Windows, we recommend [nvm-windows](https://nvm-windows.com/)
- For Linux and macOS, we recommend [nvm](https://github.com/nvm-sh/nvm#installing-and-updating). After installing it, run `nvm install --lts` to install the latest LTS version of Node.js.

Then, run `npm ci` followed by `npm run dev` in that folder.
Open the local URL printed in the terminal.
There is a Python interpreter that runs in the browser, so no local Python
installation is needed.
The ZIP includes setup instructions and an authoring guide with example agent prompts.

Here are some activities that you can choose from:

1. **Adapt materials**: Convert the chapter on [Processing Values and Remembering Results](https://github.com/CSEdAgentsOfInstruction/CSEdAgentsOfInstruction.github.io/blob/main/example-materials/python-cs1/content/lessons/part-2/5-processing-and-changing-lists.md) into a set of slides, in either PDF, Quarto markdown, or anther format of your choice.
2. **Add a visualization**: Design a set of visualizations that explains `for` loops, using the same set of base explanations as in part 1. For this, it would be useful to have Node.js set up, or Quarto, or another tool that can display visualizations in the browser.
3. **Revise a lesson**: Suppose you find that students are having challenges understanding
  when to use a `for` loop (covered in [Processing Values and Remembering Results](https://github.com/CSEdAgentsOfInstruction/CSEdAgentsOfInstruction.github.io/blob/main/example-materials/python-cs1/content/lessons/part-2/5-processing-and-changing-lists.md)) and a `while` loop (covered  [Repeating until we decide to stop](https://github.com/CSEdAgentsOfInstruction/CSEdAgentsOfInstruction.github.io/blob/main/example-materials/python-cs1/content/lessons/part-2/6-repeating-until-we-decide-to-stop.md). Identify where this learning objective could fit and revise the lesson, by first writing down a plan for what you would change, and asking the agent to act on your plan.
4. **Improving a MCQ**: Each exercise has a folder under `content/exercises/`. Its `exercise.yml` file contains the title, question, answer choices, and feedback. You can find an exercise by searching for its title in your editor. For example, try “In Part 1, Chapter 6: Making Decisions, improve the MCQ Age statement 1, which asks what `age = 18` does. Add one plausible incorrect answer that targets a different misunderstanding from the existing wrong answer. Write feedback explaining why the new answer is wrong. Keep the existing correct answer and exercise ID.”

### Worked Example (from Arto & Juho)

Suppose that we would like to adopt a Python exercise. Each exercise's folder contains:

- `exercise.yml`: the title and instructions.
- `starter.py`: the learner's initial code, shown as `main.py` in the browser.
- `tests.py`: the automated checks used by **Check**.
- `solution.py`: a reference solution.

When changing what a program should do, ask your agent to update these files together.
The exercises use Python's standard library;
a nearby exercise can serve as a working example.

For example, **Welcome card** in **Part 1, Chapter 3: Talking with a Program** currently asks learners to print `Welcome!` between two rows of asterisks. Try this prompt:

> Change the Welcome card exercise so learners write a program that prints exactly these two lines, with no asterisk border:
>
> ```text
> Welcome to the library!
> Please return books at the front desk.
> ```
>
> Keep it a beginner exercise using `print()`, with no user input. Update the instructions, starter, tests, and reference solution together, and preserve the exercise ID. Check that the new solution passes and that the original welcome card output fails.

Ask your agent to run these checks after making changes:

```sh
npm run validate
npm run test:grading
```

The first checks the content and lesson references.
The second checks the Python exercises.

Then, review the ternedered materials yourself to 
see whether the checks match the instructions and accept other reasonable solutions.
Try the exercise yourself using **Run** and **Check**,
and consider whether the feedback would help your students.

## Workshop Resources

Slides and other materials used for the workshop will be posted here.
