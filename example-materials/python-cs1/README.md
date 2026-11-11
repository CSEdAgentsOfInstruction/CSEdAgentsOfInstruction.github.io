# Introduction to Programming · workshop edition

A set of example materials adapted from parts 1–3 of [Aalto OpenCS Introduction to Programming](https://opencs.aalto.fi/en/courses/introduction-to-programming) for **Agents of Instruction: Co-Creating Learning Materials with AI Agents**, SIGCSE Virtual 2026.

The materials include 26 lessons, 70 multiple-choice questions, 73 Python exercises, and runnable examples. Use the hosted course linked from the tutorial page to try them, or follow the steps below to edit them with your AI agent.

## Start locally

Install a supported **Node.js LTS version, 24 or later**. Unzip this project, open its folder in your editor, and run:

```sh
npm ci
npm run dev
```

Open the local URL printed in the terminal. Keep the terminal running while you work; press Ctrl+C to stop. To start again, use `npm run dev`. The first `npm ci` needs internet access.

Use that web address to open the course. Double-clicking `index.html` will not start it, because the browser needs to load the app through a web server.

Python and the exercise checks run in your browser, so you do not need to install Python. Your chosen AI coding agent runs separately from this app.

## Use the exercises

- **Run** executes the code in the editor. If it calls `input()`, put the answers in **Program input**, one answer per line, before running. Blank lines are meaningful. An exhausted input box produces an end-of-input error; add the missing lines and try again.
- **Check** runs the exercise's automated tests, with their own inputs. Read the feedback, edit, and retry.
- **Stop** ends execution. Runs and checks also stop automatically after ten seconds, excluding the time needed to load Python.
- **Reset** restores the current starter. Reference solutions can be revealed explicitly.

Drafts and completion are saved in this browser only. If you edit a source starter using your agent, the app offers a choice between keeping your browser draft and loading the updated starter.

## Adapt the materials with an agent

Start with [AUTHORING.md](AUTHORING.md). Lessons are Markdown files, exercise descriptions and choices are YAML, and starter code, tests, and reference solutions are Python files. Changes reload the preview.

Try: “Change the Welcome card exercise so the program prints `Welcome to the library!` on the first line and `Please return books at the front desk.` on the second, with no asterisk border. Update the instructions, starter, tests, and reference solution together, preserve its ID, and run the content validator.”

## Check your changes

After adapting the materials, check that the content is valid and the Python exercises still work:

```sh
npm run validate
npm run test:grading
```

The first command checks lesson references and exercise metadata. The second checks that reference solutions pass, unfinished starters fail, and Python execution works correctly. Neither requires a local Python installation. Also try your changes in the browser and review the instructions and feedback.

See [NOTICE.md](NOTICE.md) for attribution and information about reusing the materials.
