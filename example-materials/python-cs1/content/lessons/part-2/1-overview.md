---
id: part-2/1-overview
part: 2
order: 1
title: Overview
---

In Part 1, your programs asked for information, stored values in variables, performed calculations, and chose between different branches.

Many programs need to **repeat** the same kind of work for several values. You might inspect every character in a word, calculate a total from several scores, or keep asking for input until the user decides to stop.

This part begins with something you already know: strings. In Part 1, you received, cleaned up, compared, and printed text values. You will now look inside strings and see that they are **sequences** of characters. A **loop** lets you process those characters one at a time. You will then use the same ideas with lists, which are sequences of values that your program can create and change.

The reasoning habits from Part 1 continue. A loop can execute the same lines many times, which makes tracing especially important. When a loop is difficult to understand, do not try to imagine all of its repetitions at once. Follow one iteration, record what changed, and then continue to the next one.

After working through this part, you should be able to **write, trace, test, and explain programs that use strings, lists, and loops to work with several values**.

The structure of this part is as follows:

- [Strings Are Sequences](#/part-2/2-strings-as-sequences) looks more closely at strings and introduces characters, positions, indexing, length, and membership.
- [Repeating over a Sequence](#/part-2/3-repeating-over-a-sequence) introduces `for` loops using strings, then shows how `range(...)` can repeat an action a fixed number of times.
- [Lists: Remembering Several Values](#/part-2/4-lists-remembering-several-values) introduces lists and shows how they can be inspected, changed, and processed with the same `for` loop idea.
- [Processing and Changing Lists](#/part-2/5-processing-and-changing-lists) develops loop patterns for totals, counts, comparisons, and building lists, then shows how to change values by position. A checkpoint separates the two stages.
- [Repeating Until We Decide to Stop](#/part-2/6-repeating-until-we-decide-to-stop) introduces `while True` and `break` for situations where the amount of input is not known beforehand.
- [Choosing and Combining Repetition](#/part-2/7-choosing-and-combining-repetition) brings the loop forms together, introduces `.split()`, and applies indexes to corresponding and neighboring items.
- [Recap](#/part-2/8-recap-and-feedback) reviews the part and includes a rainfall-analysis exercise that reuses several earlier patterns.

## Recommended Order of Work

A useful rhythm for this part is:

1. read each chapter in order;
2. type and run the examples rather than only reading them;
3. complete the exercises as you go;
4. when an exercise asks for a prediction, make your prediction before running the program;
5. when a loop's behavior is not obvious, trace one iteration at a time;
6. finish with the recap.

In [Processing and Changing Lists](#/part-2/5-processing-and-changing-lists?anchor=pause-and-check-your-progress), use the checkpoint to check your understanding of processing values before moving on to replacing list items. Return to the examples when an exercise reveals something you do not yet understand.

The most important working habit in this part is:

> **Predict first. Follow one iteration at a time. Run and compare.**

A loop is still ordinary Python code. The important difference is that the program returns to the same block and runs it again.
