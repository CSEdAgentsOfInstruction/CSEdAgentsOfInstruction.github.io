# Adapt the materials with your AI agent

Choose a lesson or exercise you would like to adapt for your students. Open the project in your editor, keep `npm run dev` running, and describe the change to your agent. Review the result in the browser as you work.

Tell your agent the intended audience, learning objective, and what you want to change. The examples below are starting points you can customize.

## Revise a lesson

Lesson text is in Markdown files under `content/lessons/part-1/`, `part-2/`, and `part-3/`. You can ask your agent to rewrite an explanation, add a worked example, or adapt the examples to a topic your students know.

Try: “In Part 1, Chapter 4: Values, Variables, and Types, rewrite the section Assignment Changes State for students learning reassignment for the first time. Explain how `count = count + 1` uses the old value of `count` to calculate its new value. Add a short worked example and a question asking students to predict the output, with an answer and explanation.”

If you want to link two lessons, ask your agent to add a link to the relevant chapter or heading, then follow it in the preview to check that it takes you to the intended place.

## Improve an MCQ

Each exercise has a folder under `content/exercises/`. Its `exercise.yml` file contains the title, question, answer choices, and feedback. You can find an exercise by searching for its title in your editor.

Try: “In Part 1, Chapter 6: Making Decisions, improve the MCQ Age statement 1, which asks what `age = 18` does. Add one plausible incorrect answer that targets a different misunderstanding from the existing wrong answer. Write feedback explaining why the new answer is wrong. Keep the existing correct answer and exercise ID.”

Try each choice in the browser and review its explanation. For multiple-selection questions, check that learners need to select all correct choices and no incorrect ones.

## Adapt a Python exercise

A Python exercise's folder contains:

- `exercise.yml`: the title and instructions.
- `starter.py`: the learner's initial code, shown as `main.py` in the browser.
- `tests.py`: the automated checks used by **Check**.
- `solution.py`: a reference solution.

When changing what a program should do, ask your agent to update these files together. The exercises use Python's standard library; a nearby exercise can serve as a working example.

For example, **Welcome card** in **Part 1, Chapter 3: Talking with a Program** currently asks learners to print `Welcome!` between two rows of asterisks. Try this prompt:

> Change the Welcome card exercise so learners write a program that prints exactly these two lines, with no asterisk border:
>
> ```text
> Welcome to the library!
> Please return books at the front desk.
> ```
>
> Keep it a beginner exercise using `print()`, with no user input. Update the instructions, starter, tests, and reference solution together, and preserve the exercise ID. Check that the new solution passes and that the original welcome card output fails.

Review whether the checks match the instructions and accept other reasonable solutions. Try the exercise yourself using **Run** and **Check**.

## Add an exercise

your agent to use an existing exercise of the same type as a starting point and place the new one in the relevant lesson. Ask it to create new IDs for new exercises and preserve existing IDs when revising them, so your saved drafts stay associated with the right exercise.

Try: “In Part 2, Chapter 2: Strings Are Sequences, add an MCQ immediately after the section Positions Start at Zero. Ask which character `word[2]` selects when `word = "planet"`. Include one correct answer and three plausible incorrect answers, including one based on counting positions from 1. Explain each answer. Follow the format of a nearby MCQ, give the new exercise its own ID, and add it to the lesson.”

## Check the result

Ask your agent to run these checks after making changes:

```sh
npm run validate
npm run test:grading
```

The first checks the content and lesson references. The second checks the Python exercises. Also review the rendered material yourself: read the instructions, try a correct answer and a plausible wrong answer, and consider whether the feedback would help your students.
